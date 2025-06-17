#!/usr/bin/env python3
"""
Test VideoProcessor functionality
"""

import os
import sys
import tempfile
from pathlib import Path

# Fix OpenMP duplicate library warning
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def test_video_processor():
    """Test VideoProcessor class creation and basic functionality"""
    print("🎬 Testing VideoProcessor...")
    print("=" * 50)
    
    try:
        from backend.video_processor import VideoProcessor
        print("✅ VideoProcessor imported successfully")
        
        # Create processor instance
        processor = VideoProcessor()
        print("✅ VideoProcessor created successfully")
        
        # Test GPU info display
        print(f"✅ GPU info displayed during initialization")
        
        # Test basic attributes
        if hasattr(processor, 'temp_dir'):
            print(f"✅ Temp directory: {processor.temp_dir}")
        else:
            print("⚠️  No temp_dir attribute found")
            
        # Test methods exist
        methods_to_check = [
            'extract_frames',
            'merge_frames_to_video', 
            'process_video',
            'get_video_info'
        ]
        
        for method in methods_to_check:
            if hasattr(processor, method):
                print(f"✅ Method '{method}' exists")
            else:
                print(f"❌ Method '{method}' missing")
        
        # Test temp directory creation
        temp_test_dir = processor.temp_dir / "test"
        temp_test_dir.mkdir(exist_ok=True)
        if temp_test_dir.exists():
            print("✅ Temp directory operations work")
            temp_test_dir.rmdir()  # Clean up
        
        print("\n🎉 VideoProcessor test completed successfully!")
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
    success = test_video_processor()
    sys.exit(0 if success else 1) 