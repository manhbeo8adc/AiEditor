# VideoProcessor Class Documentation

## Overview
Class `VideoProcessor` trong file `backend/video_processor.py` chịu trách nhiệm xử lý video, extract frames và merge videos.

## Class Definition
```python
class VideoProcessor:
    def __init__(self):
        """Initialize VideoProcessor"""
```

## Attributes (Thuộc tính)

### `self.temp_dir`
- **Type:** `str`
- **Purpose:** Đường dẫn đến thư mục temporary để lưu files tạm thời
- **Created by:** `tempfile.mkdtemp()`
- **Usage:** Lưu frames extracted và files trung gian

## Methods (Phương thức)

### `__init__(self)`
**Purpose:** Khởi tạo VideoProcessor instance

**Parameters:** Không có

**Returns:** Không có

**Functionality:**
- Tạo temporary directory cho việc xử lý
- Initialize các settings cần thiết

**Example:**
```python
processor = VideoProcessor()
```

---

### `extract_frames(self, video1_path: str, video2_path: str) -> Tuple[Optional[str], Optional[str]]`
**Purpose:** Extract frame cuối từ video1 và frame đầu từ video2 để tạo transition

**Parameters:**
- `video1_path` (str): Đường dẫn đến video thứ nhất
- `video2_path` (str): Đường dẫn đến video thứ hai

**Returns:**
- `Tuple[Optional[str], Optional[str]]`: (last_frame_path, first_frame_path)
- Trả về `(None, None)` nếu có lỗi

**Functionality:**
- Extract frame cuối cùng từ video1
- Extract frame đầu tiên từ video2
- Save frames dưới dạng image files
- Return paths đến 2 frames

**Current Status:** TODO - chưa implement

**Example:**
```python
last_frame, first_frame = processor.extract_frames("video1.mp4", "video2.mp4")
```

---

### `get_video_info(self, video_path: str) -> dict`
**Purpose:** Lấy metadata của video file

**Parameters:**
- `video_path` (str): Đường dẫn đến video file

**Returns:**
- `dict`: Dictionary chứa video metadata
  - `width` (int): Chiều rộng video
  - `height` (int): Chiều cao video
  - `fps` (float): Frames per second
  - `frame_count` (int): Tổng số frames
  - `duration` (float): Thời lượng video (seconds)
  - `error` (str): Error message nếu có lỗi

**Functionality:**
- Sử dụng OpenCV để đọc video
- Extract các thông số kỹ thuật
- Calculate duration từ frame_count và fps
- Handle errors gracefully

**Example:**
```python
info = processor.get_video_info("sample.mp4")
print(f"Duration: {info['duration']} seconds")
print(f"Resolution: {info['width']}x{info['height']}")
```

---

### `merge_videos(self, video1_path: str, video2_path: str, transition_path: str, output_path: str) -> bool`
**Purpose:** Merge 2 videos với transition video ở giữa

**Parameters:**
- `video1_path` (str): Đường dẫn video thứ nhất
- `video2_path` (str): Đường dẫn video thứ hai
- `transition_path` (str): Đường dẫn transition video (từ wan2GP)
- `output_path` (str): Đường dẫn output file

**Returns:**
- `bool`: `True` nếu merge thành công, `False` nếu có lỗi

**Functionality:**
- Concatenate 3 videos: video1 + transition + video2
- Sử dụng FFmpeg để merge
- Ensure audio sync
- Handle different resolutions/framerates

**Current Status:** TODO - chưa implement

**Example:**
```python
success = processor.merge_videos(
    "video1.mp4", 
    "video2.mp4", 
    "transition.mp4", 
    "final_output.mp4"
)
```

---

### `cleanup(self)`
**Purpose:** Dọn dẹp temporary files và directories

**Parameters:** Không có

**Returns:** Không có

**Functionality:**
- Xóa temporary directory và tất cả files bên trong
- Handle errors nếu không thể xóa
- Should be called khi hoàn thành processing

**Example:**
```python
processor.cleanup()
```

## Dependencies

### Required Imports
```python
import cv2          # OpenCV cho video processing
import os           # File system operations
import subprocess   # Running external commands (FFmpeg)
import tempfile     # Temporary file management
from typing import Tuple, Optional  # Type hints
```

### External Tools
- **OpenCV:** Video reading và metadata extraction
- **FFmpeg:** Video merging và conversion
- **Python tempfile:** Temporary directory management

## Usage Example

```python
# Initialize processor
processor = VideoProcessor()

try:
    # Get video information
    info1 = processor.get_video_info("video1.mp4")
    info2 = processor.get_video_info("video2.mp4")
    
    # Extract frames for transition
    last_frame, first_frame = processor.extract_frames("video1.mp4", "video2.mp4")
    
    # After getting transition from wan2GP
    success = processor.merge_videos(
        "video1.mp4",
        "video2.mp4", 
        "transition.mp4",
        "final_output.mp4"
    )
    
    if success:
        print("Video merge completed successfully!")
    
finally:
    # Always cleanup
    processor.cleanup()
```

## Error Handling
- Tất cả methods có try-catch blocks
- Return None hoặc False khi có lỗi
- Print error messages để debugging
- Graceful degradation khi possible

## Future Enhancements
- Add progress callbacks
- Support multiple video formats
- Batch processing capabilities
- Advanced transition effects
- GPU acceleration support 