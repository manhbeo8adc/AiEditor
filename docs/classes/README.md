# Classes Documentation Index

## Overview
Đây là documentation chi tiết cho tất cả classes và components trong AI Video Editor project.

## Backend Classes

### VideoProcessor Class
**File:** `backend/video_processor.py`  
**Documentation:** [VideoProcessor.md](../backend/classes/VideoProcessor.md)

**Purpose:** Xử lý video, extract frames và merge videos

**Key Methods:**
- `extract_frames()` - Extract frames từ videos
- `get_video_info()` - Lấy video metadata
- `merge_videos()` - Merge videos với transition
- `cleanup()` - Dọn dẹp temporary files

**Usage:**
```python
from backend.video_processor import VideoProcessor
processor = VideoProcessor()
```

---

### Wan2GPWrapper Class
**File:** `backend/wan2gp_wrapper.py`  
**Documentation:** [Wan2GPWrapper.md](../backend/classes/Wan2GPWrapper.md)

**Purpose:** Tích hợp với wan2GP AI model để generate transitions

**Key Methods:**
- `check_installation()` - Kiểm tra wan2GP installation
- `activate_environment()` - Activate conda environment
- `generate_transition()` - Generate AI transition video
- `test_generation()` - Test wan2GP functionality

**Usage:**
```python
from backend.wan2gp_wrapper import Wan2GPWrapper
wrapper = Wan2GPWrapper()
```

## Frontend Components

### App Component
**File:** `frontend/src/App.js`  
**Documentation:** [App.md](../frontend/components/App.md)

**Purpose:** Main React component với UI logic

**Key Features:**
- Backend status checking
- Video upload interface (placeholder)
- Processing controls (placeholder)
- API integration với Axios

**Usage:**
```javascript
import App from './App';
// Used as main component in index.js
```

## Class Relationships

### Backend Integration Flow
```
VideoProcessor ←→ Wan2GPWrapper
     ↓
Flask App (app.py)
     ↓
REST API Endpoints
     ↓
Frontend App Component
```

### Data Flow
1. **Upload:** User uploads videos via Frontend
2. **Extract:** VideoProcessor extracts frames
3. **Generate:** Wan2GPWrapper creates transition
4. **Merge:** VideoProcessor merges final video
5. **Download:** User downloads result

## Quick Reference

### Import Statements
```python
# Backend
from backend.video_processor import VideoProcessor
from backend.wan2gp_wrapper import Wan2GPWrapper

# Frontend
import App from './App';
import axios from 'axios';
```

### Common Usage Patterns

#### Full Video Processing Pipeline
```python
# Initialize components
processor = VideoProcessor()
wrapper = Wan2GPWrapper()

try:
    # Extract frames
    last_frame, first_frame = processor.extract_frames("video1.mp4", "video2.mp4")
    
    # Generate transition
    transition = wrapper.generate_transition(last_frame, first_frame, "transition.mp4")
    
    # Merge final video
    success = processor.merge_videos("video1.mp4", "video2.mp4", transition, "output.mp4")
    
finally:
    processor.cleanup()
```

#### Frontend API Integration
```javascript
// Check backend status
const checkStatus = async () => {
    try {
        const response = await axios.get('http://localhost:5000/api/status');
        console.log(response.data.message);
    } catch (error) {
        console.error('Backend connection failed');
    }
};
```

## Testing Each Class

### VideoProcessor Testing
```bash
python
>>> from backend.video_processor import VideoProcessor
>>> processor = VideoProcessor()
>>> print("VideoProcessor created successfully")
>>> processor.cleanup()
```

### Wan2GPWrapper Testing
```bash
python
>>> from backend.wan2gp_wrapper import Wan2GPWrapper
>>> wrapper = Wan2GPWrapper()
>>> print("Installation check:", wrapper.check_installation())
```

### App Component Testing
```bash
cd frontend
npm start
# Open http://localhost:3000
# Click "Check Backend Status" button
```

## Documentation Structure

```
docs/
├── classes/
│   └── README.md (this file)
├── backend/
│   ├── README.md
│   └── classes/
│       ├── VideoProcessor.md
│       └── Wan2GPWrapper.md
├── frontend/
│   ├── README.md
│   └── components/
│       └── App.md
└── testing/
    └── step1-testing-guide.md
```

## Next Steps

1. **Read specific class documentation** cho detailed information
2. **Follow testing guides** để verify functionality
3. **Check troubleshooting docs** nếu có issues
4. **Proceed to next development steps** sau khi testing pass

## Related Documentation

- [Backend Overview](../backend/README.md)
- [Frontend Overview](../frontend/README.md)
- [Step 1 Testing Guide](../testing/step1-testing-guide.md)
- [Environment Setup](../environment-setup.md)
- [Troubleshooting](../troubleshooting.md) 