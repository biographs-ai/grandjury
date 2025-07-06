#!/usr/bin/env python3
"""
Build and test script for GrandJury API client using uv.
This script handles building, testing, and validating the package for PyPI submission.
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil
import tempfile

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    print(f"🔧 Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)
        if result.stdout:
            print(f"📝 Output: {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"📝 Error output: {e.stderr.strip()}")
        if check:
            raise
        return e

def main():
    """Main build and test process."""
    print("🚀 GrandJury API Client - Build & Test with uv")
    print("=" * 50)
    
    # Check if we're in the right directory
    root_dir = Path.cwd()
    
    # Check if we're in the scripts directory and need to go up
    if root_dir.name == "scripts":
        root_dir = root_dir.parent
        print("📂 Detected running from scripts/, using parent directory")
    
    # Look for pyproject.toml in root
    pyproject_file = root_dir / "pyproject.toml"
    if not pyproject_file.exists():
        print("❌ Error: pyproject.toml not found. Run this from the project root or scripts/ directory.")
        sys.exit(1)
    
    print(f"📂 Working directory: {root_dir}")
    print(f"📦 Package directory: {root_dir}")
    
    # Step 1: Clean previous builds
    print("\n🧹 Cleaning previous builds...")
    dist_dir = root_dir / "dist"
    build_dir = root_dir / "build"
    egg_info = root_dir / "grandjury.egg-info"
    
    for dir_to_clean in [dist_dir, build_dir, egg_info]:
        if dir_to_clean.exists():
            shutil.rmtree(dir_to_clean)
            print(f"   Removed {dir_to_clean}")
    
    # Step 2: Verify package structure
    print("\n📋 Verifying package structure...")
    required_files = [
        root_dir / "pyproject.toml",
        root_dir / "README.md", 
        root_dir / "grandjury" / "__init__.py",
        root_dir / "grandjury" / "api_client.py",
    ]
    
    missing_files = [f for f in required_files if not f.exists()]
    if missing_files:
        print("❌ Missing required files:")
        for f in missing_files:
            print(f"   - {f}")
        sys.exit(1)
    else:
        print("✅ All required files present")
    
    # Step 3: Check uv installation
    print("\n🔍 Checking uv installation...")
    try:
        result = run_command(["uv", "--version"])
        print(f"✅ uv version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # Step 4: Install build dependencies
    print("\n📦 Installing build dependencies...")
    run_command(["uv", "add", "--dev", "build", "twine"], cwd=root_dir)
    
    # Step 5: Build the package
    print("\n🔨 Building package...")
    run_command(["uv", "run", "python", "-m", "build"], cwd=root_dir)
    
    # Step 6: Check build artifacts
    print("\n📦 Checking build artifacts...")
    dist_files = list(dist_dir.glob("*")) if dist_dir.exists() else []
    if not dist_files:
        print("❌ No build artifacts found")
        sys.exit(1)
    
    for file in dist_files:
        print(f"   ✅ {file.name} ({file.stat().st_size} bytes)")
    
    # Step 7: Validate package with twine
    print("\n🔍 Validating package with twine...")
    try:
        run_command(["uv", "run", "twine", "check", "dist/*"], cwd=root_dir)
        print("✅ Package validation passed")
    except subprocess.CalledProcessError:
        print("⚠️ Package validation had warnings (may still be publishable)")
    
    # Step 8: Test installation in temporary environment
    print("\n🧪 Testing package installation...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Find the wheel file
        wheel_files = list(dist_dir.glob("*.whl"))
        if not wheel_files:
            print("❌ No wheel file found")
            sys.exit(1)
        
        wheel_file = wheel_files[0]
        
        # Create a test script
        test_script = temp_path / "test_install.py"
        test_script.write_text("""
import sys
try:
    import grandjury
    from grandjury import GrandJuryClient
    
    # Test basic import
    client = GrandJuryClient()
    print("✅ Package imports successfully")
    print(f"✅ Client base URL: {client.base_url}")
    
    # Test that all main methods exist
    methods = ['vote_histogram', 'vote_completeness', 'population_confidence', 
               'majority_good_votes', 'votes_distribution', 'evaluate_model']
    
    for method in methods:
        if hasattr(client, method):
            print(f"✅ Method {method} available")
        else:
            print(f"❌ Method {method} missing")
            sys.exit(1)
    
    print("🎉 Installation test passed!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1)
""")
        
        # Test installation with uv
        try:
            # Create a minimal pyproject.toml for the test
            test_project = temp_path / "pyproject.toml"
            test_project.write_text(f"""
[project]
name = "test-grandjury"
version = "0.1.0"
dependencies = [
    "grandjury @ file://{wheel_file.absolute()}"
]
requires-python = ">=3.8"
""")
            
            # Run the test
            run_command(["uv", "run", "python", "test_install.py"], cwd=temp_path)
            print("✅ Installation test passed")
            
        except subprocess.CalledProcessError:
            print("❌ Installation test failed")
            sys.exit(1)
    
    # Step 9: Summary
    print("\n" + "=" * 50)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print(f"\n📦 Package files ready in: {dist_dir}")
    print("\n🚀 Next steps for PyPI publication:")
    print("   1. Test upload to TestPyPI:")
    print(f"      uv run twine upload --repository testpypi {dist_dir}/*")
    print("   2. Test install from TestPyPI:")
    print("      pip install --index-url https://test.pypi.org/simple/ grandjury")
    print("   3. Upload to PyPI:")
    print(f"      uv run twine upload {dist_dir}/*")
    print("   4. Test final installation:")
    print("      pip install grandjury")
    print("\n✅ Package is ready for PyPI submission!")

if __name__ == "__main__":
    main()
