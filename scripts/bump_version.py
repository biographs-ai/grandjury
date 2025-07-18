#!/usr/bin/env python3
"""
Version bumping script for grandjury package.
Usage: python scripts/bump_version.py [major|minor|patch]
"""

import re
import sys
import subprocess
from pathlib import Path

def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    
    return match.group(1)

def bump_version(current_version, bump_type):
    """Bump version based on semantic versioning"""
    major, minor, patch = map(int, current_version.split('.'))
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError("bump_type must be 'major', 'minor', or 'patch'")
    
    return f"{major}.{minor}.{patch}"

def update_pyproject_version(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    updated_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content
    )
    
    pyproject_path.write_text(updated_content)
    print(f"✅ Updated pyproject.toml to version {new_version}")

def create_git_tag(version):
    """Create git commit and tag"""
    try:
        # Add changes
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        
        # Commit
        subprocess.run([
            "git", "commit", "-m", f"Bump version to {version}"
        ], check=True)
        
        # Create tag
        tag = f"v{version}"
        subprocess.run([
            "git", "tag", "-a", tag, "-m", f"Release version {version}"
        ], check=True)
        
        print(f"✅ Created git commit and tag {tag}")
        print(f"🚀 To trigger release, run: git push origin main --tags")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    
    return True

def main():
    if len(sys.argv) != 2 or sys.argv[1] in ['-h', '--help']:
        print("Usage: python scripts/bump_version.py [major|minor|patch]")
        print("Example: python scripts/bump_version.py patch")
        print("\nBump types:")
        print("  patch  - Bug fixes (1.0.0 → 1.0.1)")
        print("  minor  - New features (1.0.0 → 1.1.0)")
        print("  major  - Breaking changes (1.0.0 → 2.0.0)")
        sys.exit(0 if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help'] else 1)
    
    bump_type = sys.argv[1]
    if bump_type not in ['major', 'minor', 'patch']:
        print("❌ bump_type must be 'major', 'minor', or 'patch'")
        print("Run with --help for usage information")
        sys.exit(1)
    
    try:
        # Get current version
        current_version = get_current_version()
        print(f"📦 Current version: {current_version}")
        
        # Calculate new version
        new_version = bump_version(current_version, bump_type)
        print(f"🎯 New version: {new_version}")
        
        # Confirm with user
        response = input(f"Update version from {current_version} to {new_version}? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cancelled")
            sys.exit(1)
        
        # Update pyproject.toml
        update_pyproject_version(new_version)
        
        # Create git commit and tag
        if create_git_tag(new_version):
            print("\n🎉 Version bump complete!")
            print(f"📝 Next steps:")
            print(f"   1. git push origin main --tags")
            print(f"   2. Create GitHub release at: https://github.com/grandjury/grandjury-python/releases/new")
            print(f"   3. GitHub Actions will automatically publish to PyPI")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
