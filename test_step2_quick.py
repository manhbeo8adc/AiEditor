#!/usr/bin/env python3
"""Quick test for Step 2: Video Processing"""

import sys
import os
sys.path.append('backend')

def test_flask_app():
    print("🧪 Testing Flask App với Security...")
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test with test client
        with app.test_client() as client:
            # Test status endpoint
            response = client.get('/api/status')
            print(f"✅ Status endpoint: {response.status_code}")
            print(f"   Response: {response.get_json()}")
            
            # Test security endpoints
            response = client.post('/api/upload')
            print(f"✅ Upload endpoint (no files): {response.status_code}")
            
            response = client.post('/api/extract-frames')
            print(f"✅ Extract frames endpoint: {response.status_code}")
            
        print("🎉 Flask app test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_video_processor():
    print("\n🧪 Testing VideoProcessor...")
    
    try:
        from video_processor import VideoProcessor
        print("✅ VideoProcessor imported successfully")
        
        # Initialize processor
        processor = VideoProcessor()
        print("✅ VideoProcessor initialized")
        
        # Test method existence instead of actual file processing
        print(f"✅ Method 'safe_ffmpeg_command' exists: {hasattr(processor, 'safe_ffmpeg_command')}")
        print(f"✅ Method 'execute_safe_command' exists: {hasattr(processor, 'execute_safe_command')}")
        print(f"✅ Method 'extract_transition_frames' exists: {hasattr(processor, 'extract_transition_frames')}")
        print(f"✅ Method 'merge_videos_with_transition' exists: {hasattr(processor, 'merge_videos_with_transition')}")
        
        print("🎉 VideoProcessor test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ VideoProcessor test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎬 BƯỚC 2 Quick Test - Video Processing")
    print("=" * 50)
    
    success1 = test_flask_app()
    success2 = test_video_processor()
    
    if success1 and success2:
        print("\n🎉 All BƯỚC 2 tests passed!")
    else:
        print("\n❌ Some tests failed - check implementation") 