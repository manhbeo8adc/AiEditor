# Hướng dẫn Kiểm thử Bước 2 - Video Processing

## Tổng quan
Hướng dẫn kiểm thử các tính năng video processing đã implement trong bước 2, bao gồm secure API endpoints, file upload security, và video processing functions.

## Yêu cầu trước khi bắt đầu
- BƯỚC 1 đã hoàn thành thành công
- Conda environment `ai_video_env` đã được kích hoạt
- Dependencies mới đã được cài đặt

## Danh sách kiểm thử

### ✅ 1. Cài đặt Dependencies mới
```bash
# Kích hoạt environment
conda activate ai_video_env

# Cài đặt dependencies mới
pip install flask-limiter python-magic python-magic-bin pytest-flask imageio imageio-ffmpeg ffmpeg-python pathlib2
```

**Kết quả mong đợi:**
```
Successfully installed flask-limiter-3.5.0 python-magic-0.4.27 ...
```

### ✅ 2. Kiểm thử Backend Security Features

#### 2.1 Test Flask App với Security
```bash
# Khởi động backend server
python backend/app.py
```

**Kết quả mong đợi:**
```
🚀 GPU acceleration enabled: NVIDIA GeForce RTX 5060 Ti
   CUDA version: 12.4
   PyTorch version: 2.7.1+cu128
⚠️  Using CPU processing  # (for Blackwell compatibility)
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

#### 2.2 Test Rate Limiting
**Mở terminal mới (giữ server chạy):**

```bash
# Test status endpoint (should work)
curl http://localhost:5000/api/status

# Test rate limiting - run multiple times quickly
for i in {1..6}; do
  curl -X POST http://localhost:5000/api/upload
  echo "Request $i"
done
```

**Expected Response (Rate limiting after 5 requests):**
```json
{
  "error": "An error occurred",
  "code": 429
}
```

#### 2.3 Test CORS Configuration
```bash
# Test CORS với allowed origin
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS http://localhost:5000/api/upload

# Test CORS với disallowed origin
curl -H "Origin: http://malicious-site.com" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS http://localhost:5000/api/upload
```

### ✅ 3. Kiểm thử Secure File Upload

#### 3.1 Tạo Test Videos
```bash
# Tạo test videos bằng FFmpeg
mkdir test_videos

# Tạo video1 (3 giây, màu đỏ)
ffmpeg -f lavfi -i testsrc=duration=3:size=320x240:rate=25 -c:v libx264 test_videos/video1.mp4

# Tạo video2 (3 giây, màu xanh)  
ffmpeg -f lavfi -i testsrc2=duration=3:size=320x240:rate=25 -c:v libx264 test_videos/video2.mp4

# Verify videos được tạo
ls -la test_videos/
```

#### 3.2 Test Valid File Upload
```bash
# Test upload với valid video files
curl -X POST http://localhost:5000/api/upload \
  -F "video1=@test_videos/video1.mp4" \
  -F "video2=@test_videos/video2.mp4"
```

**Kết quả mong đợi:**
```json
{
  "message": "Files uploaded successfully",
  "status": "success",
  "files": [
    {
      "file_name": "video1",
      "original_name": "video1.mp4",
      "secure_path": "uploads/a1b2c3d4_video1.mp4",
      "size_bytes": 45123,
      "duration_seconds": 3.0,
      "resolution": "320x240",
      "fps": 25.0,
      "frame_count": 75
    },
    ...
  ]
}
```

#### 3.3 Test File Security Validation
```bash
# Test invalid file type
echo "fake video content" > test_videos/fake.txt
curl -X POST http://localhost:5000/api/upload \
  -F "video1=@test_videos/fake.txt" \
  -F "video2=@test_videos/video2.mp4"

# Test missing files
curl -X POST http://localhost:5000/api/upload \
  -F "video1=@test_videos/video1.mp4"

# Test too large file (create if needed)
# dd if=/dev/zero of=test_videos/large.mp4 bs=1M count=600  # 600MB
```

**Expected Responses:**
```json
{"error": "File format not supported", "code": 400}
{"error": "Missing field: video2", "code": 400}
{"error": "File size exceeds limit", "code": 400}
```

### ✅ 4. Kiểm thử Video Processing Functions

#### 4.1 Test Frame Extraction
```bash
# Tạo test data từ upload response
curl -X POST http://localhost:5000/api/extract-frames \
  -H "Content-Type: application/json" \
  -d '{
    "video1_path": "uploads/a1b2c3d4_video1.mp4",
    "video2_path": "uploads/a1b2c3d4_video2.mp4"
  }'
```

**Kết quả mong đợi:**
```json
{
  "message": "Frames extracted successfully",
  "status": "success", 
  "frames": {
    "last_frame": "temp/transition_frames/last_frame.jpg",
    "first_frame": "temp/transition_frames/first_frame.jpg"
  }
}
```

#### 4.2 Test Transition Generation
```bash
# Test AI transition generation
curl -X POST http://localhost:5000/api/generate-transition \
  -H "Content-Type: application/json" \
  -d '{
    "last_frame": "temp/transition_frames/last_frame.jpg",
    "first_frame": "temp/transition_frames/first_frame.jpg",
    "duration": 2.0
  }'
```

**Kết quả mong đợi:**
```json
{
  "message": "Transition generated successfully",
  "status": "success",
  "transition_path": "temp/transition_a1b2c3d4.mp4",
  "duration": 2.0
}
```

#### 4.3 Test Video Merging
```bash
# Test video merging
curl -X POST http://localhost:5000/api/merge-videos \
  -H "Content-Type: application/json" \
  -d '{
    "video1_path": "uploads/a1b2c3d4_video1.mp4",
    "video2_path": "uploads/a1b2c3d4_video2.mp4", 
    "transition_path": "temp/transition_a1b2c3d4.mp4"
  }'
```

**Kết quả mong đợi:**
```json
{
  "message": "Videos merged successfully",
  "status": "success",
  "output_path": "output/merged_video_a1b2c3d4.mp4",
  "download_url": "/api/download/merged_video_a1b2c3d4.mp4"
}
```

#### 4.4 Test File Download
```bash
# Test download endpoint
curl -X GET http://localhost:5000/api/download/merged_video_a1b2c3d4.mp4 \
  --output downloaded_video.mp4

# Verify downloaded file
file downloaded_video.mp4
```

### ✅ 5. Kiểm thử VideoProcessor Class Trực tiếp

#### 5.1 Test VideoProcessor Security Functions
```bash
# Tạo test script
cat > test_video_processor_step2.py << 'EOF'
#!/usr/bin/env python3
"""Test VideoProcessor security và processing functions"""

import sys
import os
sys.path.append('backend')

from video_processor import VideoProcessor

def test_video_processor_security():
    print("🧪 Testing VideoProcessor Security Functions...")
    
    try:
        # Initialize processor
        processor = VideoProcessor()
        print("✅ VideoProcessor initialized")
        
        # Test safe_ffmpeg_command
        cmd = processor.safe_ffmpeg_command(
            ['test_videos/video1.mp4'], 
            'output/test_output.mp4'
        )
        print(f"✅ Safe FFmpeg command: {' '.join(cmd[:5])}...")
        
        # Test extract_transition_frames
        last_frame, first_frame = processor.extract_transition_frames(
            'test_videos/video1.mp4',
            'test_videos/video2.mp4'
        )
        print(f"✅ Transition frames extracted:")
        print(f"   Last frame: {last_frame}")
        print(f"   First frame: {first_frame}")
        
        print("🎉 VideoProcessor security test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ VideoProcessor test failed: {e}")
        return False

if __name__ == "__main__":
    test_video_processor_security()
EOF

# Chạy test
python test_video_processor_step2.py
```

**Kết quả mong đợi:**
```
🧪 Testing VideoProcessor Security Functions...
✅ VideoProcessor initialized
🚀 GPU acceleration enabled: NVIDIA GeForce RTX 5060 Ti
✅ Safe FFmpeg command: ffmpeg -y -hwaccel...
🎬 Extracting last frame from video1...
🎬 Extracting first frame from video2...
✅ Transition frames extracted:
   Last frame: temp/transition_frames/last_frame.jpg
   First frame: temp/transition_frames/first_frame.jpg
🎉 VideoProcessor security test completed successfully!
```

### ✅ 6. End-to-End Workflow Test

#### 6.1 Complete Video Processing Pipeline
```bash
# Complete workflow test script
cat > test_complete_workflow.py << 'EOF'
#!/usr/bin/env python3
"""Complete video processing workflow test"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_complete_workflow():
    print("🎬 Testing Complete Video Processing Workflow...")
    
    try:
        # Step 1: Upload videos
        print("\n1. Uploading videos...")
        with open('test_videos/video1.mp4', 'rb') as f1, \
             open('test_videos/video2.mp4', 'rb') as f2:
            
            files = {
                'video1': ('video1.mp4', f1, 'video/mp4'),
                'video2': ('video2.mp4', f2, 'video/mp4')
            }
            
            response = requests.post(f"{BASE_URL}/api/upload", files=files)
            upload_result = response.json()
            print(f"✅ Upload: {upload_result['status']}")
        
        # Extract paths
        video1_path = upload_result['files'][0]['secure_path']
        video2_path = upload_result['files'][1]['secure_path']
        
        # Step 2: Extract frames
        print("\n2. Extracting transition frames...")
        response = requests.post(f"{BASE_URL}/api/extract-frames", 
                               json={
                                   'video1_path': video1_path,
                                   'video2_path': video2_path
                               })
        frames_result = response.json()
        print(f"✅ Frame extraction: {frames_result['status']}")
        
        # Step 3: Generate transition
        print("\n3. Generating AI transition...")
        response = requests.post(f"{BASE_URL}/api/generate-transition",
                               json={
                                   'last_frame': frames_result['frames']['last_frame'],
                                   'first_frame': frames_result['frames']['first_frame'],
                                   'duration': 1.5
                               })
        transition_result = response.json()
        print(f"✅ Transition generation: {transition_result['status']}")
        
        # Step 4: Merge videos
        print("\n4. Merging videos...")
        response = requests.post(f"{BASE_URL}/api/merge-videos",
                               json={
                                   'video1_path': video1_path,
                                   'video2_path': video2_path,
                                   'transition_path': transition_result['transition_path']
                               })
        merge_result = response.json()
        print(f"✅ Video merging: {merge_result['status']}")
        
        # Step 5: Download result
        print("\n5. Testing download...")
        download_url = merge_result['download_url']
        response = requests.get(f"{BASE_URL}{download_url}")
        
        if response.status_code == 200:
            with open('final_merged_video.mp4', 'wb') as f:
                f.write(response.content)
            print(f"✅ Download successful: final_merged_video.mp4")
        
        print("\n🎉 Complete workflow test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

if __name__ == "__main__":
    test_complete_workflow()
EOF

# Chạy complete workflow test
python test_complete_workflow.py
```

## Troubleshooting

### Common Issues

#### Dependencies Installation Errors
```bash
# If python-magic fails on Windows
pip install python-magic-bin

# If rate limiting issues
pip install flask-limiter --upgrade

# If FFmpeg not found
# Download FFmpeg từ https://ffmpeg.org/download.html
# Thêm vào PATH environment variable
```

#### GPU Processing Issues
```bash
# Check GPU detection
python -c "
import torch
print(f'CUDA Available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name()}')
"

# If GPU not working, CPU fallback sẽ được sử dụng automatically
```

#### File Upload Errors
```bash
# Check file permissions
ls -la uploads/ temp/ output/

# Check disk space
df -h .

# Check file magic detection
python -c "
import magic
print(magic.from_file('test_videos/video1.mp4', mime=True))
"
```

#### Rate Limiting Issues
```bash
# Wait 1 minute for rate limit reset
# Or restart server to reset rate limits
```

#### FFmpeg Processing Errors
```bash
# Test FFmpeg installation
ffmpeg -version

# Test basic FFmpeg operation
ffmpeg -f lavfi -i testsrc=duration=1:size=320x240:rate=1 test_ffmpeg.mp4
```

## Success Criteria

### ✅ All Tests Pass When:
1. All dependencies install successfully
2. Backend starts với security features enabled
3. Rate limiting works correctly (blocks after limits)
4. CORS correctly allows/denies origins
5. File upload validates security properly
6. Frame extraction produces valid image files
7. Transition generation creates valid video
8. Video merging produces final output
9. Download endpoint serves files correctly
10. Complete workflow runs end-to-end

### ✅ Security Features Working:
- Rate limiting blocks excessive requests ✓
- File type validation rejects invalid files ✓
- Path traversal prevention works ✓
- FFmpeg command injection prevention ✓
- Error messages don't leak sensitive info ✓

### ✅ Video Processing Working:
- Frame extraction from both videos ✓
- Basic transition generation (crossfade) ✓
- Video concatenation with audio sync ✓
- GPU acceleration enabled (where available) ✓
- CPU fallback works correctly ✓

## Next Steps
Sau khi tất cả tests pass, bạn có thể:
1. Commit changes: `git add . && git commit -m "Implement Step 2: Secure Video Processing"`
2. Proceed to BƯỚC 3: wan2GP Integration
3. Document any issues trong `docs/troubleshooting.md`

## File Structure Verification
```
AiEditor/
├── backend/
│   ├── app.py ✓ (Updated với security)
│   ├── video_processor.py ✓ (Updated với safe processing)
│   └── wan2gp_wrapper.py ✓
├── uploads/ ✓ (Contains test videos)
├── temp/ ✓ (Contains transition frames)
├── output/ ✓ (Contains merged videos)
├── test_videos/ ✓ (Test input videos)
├── requirements.txt ✓ (Updated với new deps)
├── test_video_processor_step2.py ✓
├── test_complete_workflow.py ✓
└── final_merged_video.mp4 ✓
```

## Quick Test Sequence

### Chạy tất cả tests nhanh:
```bash
# 1. Install dependencies
pip install flask-limiter python-magic python-magic-bin pytest-flask

# 2. Create test videos
mkdir test_videos
ffmpeg -f lavfi -i testsrc=duration=3:size=320x240:rate=25 -c:v libx264 test_videos/video1.mp4
ffmpeg -f lavfi -i testsrc2=duration=3:size=320x240:rate=25 -c:v libx264 test_videos/video2.mp4

# 3. Start backend (in background)
python backend/app.py &

# 4. Wait for startup
sleep 3

# 5. Run complete workflow test
python test_complete_workflow.py

# 6. Check output
ls -la final_merged_video.mp4
```

### Expected Timeline:
- **Dependencies setup**: 2-3 minutes
- **All tests**: 3-5 minutes  
- **Complete workflow**: 1-2 minutes

**🎯 Nếu tất cả tests pass, BƯỚC 2 hoàn tất thành công!** 