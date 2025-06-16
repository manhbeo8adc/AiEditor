# Backend Documentation

## Overview
Backend của AI Video Editor được xây dựng bằng Flask, cung cấp REST API cho việc xử lý video và tích hợp với wan2GP.

## Structure
```
backend/
├── app.py              # Main Flask application
├── video_processor.py  # Video processing utilities
├── wan2gp_wrapper.py   # wan2GP integration wrapper
├── api/               # API route modules (future)
├── models/            # Data models (future)
└── utils/             # Utility functions (future)
```

## Files Documentation

### app.py
**Purpose:** Main Flask application với REST API endpoints

**Key Features:**
- Health check endpoint (`/api/status`)
- Video upload endpoint (`/api/upload`)
- Frame extraction endpoint (`/api/extract-frames`)
- AI transition generation (`/api/generate-transition`)
- Video merging endpoint (`/api/merge-videos`)

**Testing:**
```bash
# Start server
python backend/app.py

# Test status endpoint
curl http://localhost:5000/api/status
```

### video_processor.py
**Purpose:** Video processing utilities using OpenCV and FFmpeg

**Key Features:**
- Frame extraction from videos
- Video metadata extraction
- Video merging with transitions
- Temporary file management

**Testing:**
```python
from backend.video_processor import VideoProcessor
processor = VideoProcessor()
# Test with sample video files
```

### wan2gp_wrapper.py
**Purpose:** Integration wrapper for wan2GP AI model

**Key Features:**
- Environment management
- Transition generation
- Installation verification
- Test generation

**Testing:**
```python
from backend.wan2gp_wrapper import Wan2GPWrapper
wrapper = Wan2GPWrapper()
print(wrapper.check_installation())
```

## API Endpoints

### GET /api/status
**Purpose:** Health check
**Response:**
```json
{
  "status": "running",
  "message": "AI Video Editor Backend is running",
  "version": "1.0.0"
}
```

### POST /api/upload
**Purpose:** Upload video files
**Expected:** Multipart form with video1, video2 files
**Response:** Upload status and file paths

### POST /api/extract-frames
**Purpose:** Extract frames for transition
**Expected:** JSON with video paths
**Response:** Frame paths and metadata

### POST /api/generate-transition
**Purpose:** Generate AI transition
**Expected:** JSON with frame paths
**Response:** Transition video path

### POST /api/merge-videos
**Purpose:** Merge videos with transition
**Expected:** JSON with video and transition paths
**Response:** Final video path

## Configuration

### Environment Variables
- `UPLOAD_FOLDER`: Directory for uploaded videos
- `OUTPUT_FOLDER`: Directory for final videos
- `TEMP_FOLDER`: Directory for temporary files

### Dependencies
See `requirements.txt` for exact versions:
- Flask 2.3.3
- OpenCV 4.8.1.78
- PyTorch 2.0.1+cu118
- FFmpeg-python 0.2.0

## Error Handling
Tất cả endpoints sử dụng JSON response format và HTTP status codes chuẩn.

## Security
- CORS enabled cho frontend communication
- File upload validation (to be implemented)
- Path traversal prevention (to be implemented) 