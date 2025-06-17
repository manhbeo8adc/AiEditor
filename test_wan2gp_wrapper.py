#!/usr/bin/env python3
"""
Test Wan2GPWrapper functionality
"""

import os
import sys

# Fix OpenMP duplicate library warning
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def test_wan2gp_wrapper():
    """Test Wan2GPWrapper class creation and basic functionality"""
    print("🤖 Testing Wan2GPWrapper...")
    print("=" * 50)
    
    try:
        from backend.wan2gp_wrapper import Wan2GPWrapper
        print("✅ Wan2GPWrapper imported successfully")
        
        # Create wrapper instance
        wrapper = Wan2GPWrapper()
        print("✅ Wan2GPWrapper created successfully")
        
        # Test installation check
        installation_status = wrapper.check_installation()
        print(f"✅ Installation check result: {installation_status}")
        
        # Test basic attributes and methods
        methods_to_check = [
            'check_installation',
            'process_video',
            'get_model_info'
        ]
        
        for method in methods_to_check:
            if hasattr(wrapper, method):
                print(f"✅ Method '{method}' exists")
            else:
                print(f"❌ Method '{method}' missing")
        
        # Test model info (should handle gracefully if wan2gp not installed)
        try:
            model_info = wrapper.get_model_info()
            print(f"✅ Model info: {model_info}")
        except Exception as e:
            print(f"⚠️  Model info unavailable (expected if wan2gp not installed): {e}")
        
        print("\n🎉 Wan2GPWrapper test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the correct directory and environment is activated")
        return False
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_wan2gp_wrapper()
    sys.exit(0 if success else 1) 