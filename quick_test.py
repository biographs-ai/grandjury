#!/usr/bin/env python3
"""
Quick package verification script for GrandJury API client.
Run this anytime to verify the package is working correctly.
"""

import sys
import os
from pathlib import Path

# Add the pypi directory to the path for testing
sys.path.insert(0, os.path.join(os.getcwd(), 'pypi'))

def test_package():
    """Quick package verification."""
    print("🧪 GrandJury Package Quick Test")
    print("=" * 40)
    
    try:
        # Test imports
        import grandjury
        from grandjury import GrandJuryClient, evaluate_model
        print("✅ Package imports successfully")
        
        # Test client initialization
        client = GrandJuryClient()
        print(f"✅ Client initialized - base URL: {client.base_url}")
        
        # Test that all methods exist
        methods = [
            'vote_histogram', 'vote_completeness', 'population_confidence',
            'majority_good_votes', 'votes_distribution', 'evaluate_model'
        ]
        
        for method in methods:
            if hasattr(client, method):
                print(f"✅ Method {method} available")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        # Test backward compatibility
        if callable(evaluate_model):
            print("✅ Backward compatibility function available")
        else:
            print("❌ Backward compatibility function missing")
            return False
        
        # Test optional dependencies detection
        try:
            import pandas
            print("✅ pandas available")
        except ImportError:
            print("⚠️ pandas not available")
        
        try:
            import polars
            print("✅ polars available")  
        except ImportError:
            print("⚠️ polars not available")
        
        try:
            import pyarrow
            print("✅ pyarrow available")
        except ImportError:
            print("⚠️ pyarrow not available")
        
        try:
            import msgspec
            print("✅ msgspec available")
        except ImportError:
            print("⚠️ msgspec not available")
        
        print("\n🎉 All tests passed! Package is ready.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = test_package()
    sys.exit(0 if success else 1)
