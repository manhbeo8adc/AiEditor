# Wan2GPWrapper Class Documentation

## Overview
Class `Wan2GPWrapper` trong file `backend/wan2gp_wrapper.py` chịu trách nhiệm tích hợp với wan2GP AI model để generate transition videos.

## Class Definition
```python
class Wan2GPWrapper:
    def __init__(self, wan2gp_path: str = "./wan2gp"):
        """Initialize wan2GP wrapper"""
```

## Attributes (Thuộc tính)

### `self.wan2gp_path`
- **Type:** `str`
- **Purpose:** Đường dẫn đến thư mục wan2gp project
- **Default:** `"./wan2gp"`
- **Usage:** Locate wan2GP installation và scripts

### `self.env_activated`
- **Type:** `bool`
- **Purpose:** Track trạng thái activation của wan2GP environment
- **Default:** `False`
- **Usage:** Ensure environment được activate trước khi run inference

## Methods (Phương thức)

### `__init__(self, wan2gp_path: str = "./wan2gp")`
**Purpose:** Khởi tạo Wan2GPWrapper instance

**Parameters:**
- `wan2gp_path` (str, optional): Đường dẫn đến wan2gp directory. Default: `"./wan2gp"`

**Returns:** Không có

**Functionality:**
- Set path đến wan2GP installation
- Initialize environment activation status
- Prepare wrapper cho subsequent operations

**Example:**
```python
# Default path
wrapper = Wan2GPWrapper()

# Custom path
wrapper = Wan2GPWrapper("/path/to/wan2gp")
```

---

### `check_installation(self) -> bool`
**Purpose:** Kiểm tra xem wan2GP có được install đúng cách không

**Parameters:** Không có

**Returns:**
- `bool`: `True` nếu installation OK, `False` nếu có vấn đề

**Functionality:**
- Check xem wan2gp directory có tồn tại không
- Verify required files và dependencies
- Validate installation integrity

**Current Status:** Partially implemented - chỉ check directory existence

**Example:**
```python
wrapper = Wan2GPWrapper()
if wrapper.check_installation():
    print("wan2GP is properly installed")
else:
    print("wan2GP installation issues detected")
```

---

### `activate_environment(self) -> bool`
**Purpose:** Activate wan2GP conda environment

**Parameters:** Không có

**Returns:**
- `bool`: `True` nếu activation thành công, `False` nếu có lỗi

**Functionality:**
- Activate conda environment cho wan2GP
- Set up environment variables
- Prepare Python path và dependencies
- Update `self.env_activated` status

**Current Status:** TODO - chưa implement

**Example:**
```python
wrapper = Wan2GPWrapper()
if wrapper.activate_environment():
    print("Environment activated successfully")
```

---

### `generate_transition(self, frame1_path: str, frame2_path: str, output_path: str, duration: float = 2.0) -> Optional[str]`
**Purpose:** Generate transition video giữa 2 frames sử dụng wan2GP AI

**Parameters:**
- `frame1_path` (str): Đường dẫn đến frame đầu tiên (end frame của video1)
- `frame2_path` (str): Đường dẫn đến frame thứ hai (start frame của video2)
- `output_path` (str): Đường dẫn cho output transition video
- `duration` (float, optional): Thời lượng transition (seconds). Default: 2.0

**Returns:**
- `Optional[str]`: Path đến generated transition video, hoặc `None` nếu failed

**Functionality:**
- Ensure environment được activated
- Prepare input frames cho wan2GP
- Run wan2GP inference với specified parameters
- Generate smooth transition video
- Return path đến output file

**Current Status:** TODO - chưa implement

**Example:**
```python
wrapper = Wan2GPWrapper()
transition_path = wrapper.generate_transition(
    "last_frame.jpg",
    "first_frame.jpg", 
    "transition.mp4",
    duration=3.0
)
if transition_path:
    print(f"Transition generated: {transition_path}")
```

---

### `test_generation(self) -> bool`
**Purpose:** Test wan2GP generation với sample frames

**Parameters:** Không có

**Returns:**
- `bool`: `True` nếu test thành công, `False` nếu có lỗi

**Functionality:**
- Create sample test frames
- Run basic generation test
- Verify output quality
- Validate wan2GP functionality

**Current Status:** TODO - chưa implement

**Example:**
```python
wrapper = Wan2GPWrapper()
if wrapper.test_generation():
    print("wan2GP is working correctly")
else:
    print("wan2GP test failed")
```

## Dependencies

### Required Imports
```python
import os           # File system operations
import subprocess   # Running external commands
import tempfile     # Temporary file management
from typing import Optional  # Type hints
```

### External Dependencies
- **wan2GP:** AI model cho video generation
- **Conda:** Environment management
- **PyTorch:** Deep learning framework (via wan2GP)
- **CUDA:** GPU acceleration (optional)

## Usage Example

```python
# Initialize wrapper
wrapper = Wan2GPWrapper("./wan2gp")

try:
    # Check installation
    if not wrapper.check_installation():
        print("Please install wan2GP first")
        return
    
    # Activate environment
    if not wrapper.activate_environment():
        print("Failed to activate wan2GP environment")
        return
    
    # Test functionality
    if not wrapper.test_generation():
        print("wan2GP test failed")
        return
    
    # Generate actual transition
    transition_path = wrapper.generate_transition(
        "frame1.jpg",
        "frame2.jpg",
        "output_transition.mp4",
        duration=2.5
    )
    
    if transition_path:
        print(f"Success! Transition saved to: {transition_path}")
    else:
        print("Failed to generate transition")

except Exception as e:
    print(f"Error: {e}")
```

## Integration với VideoProcessor

```python
from backend.video_processor import VideoProcessor
from backend.wan2gp_wrapper import Wan2GPWrapper

# Initialize both components
processor = VideoProcessor()
wrapper = Wan2GPWrapper()

try:
    # Extract frames
    last_frame, first_frame = processor.extract_frames("video1.mp4", "video2.mp4")
    
    # Generate transition
    transition_path = wrapper.generate_transition(
        last_frame, 
        first_frame, 
        "transition.mp4"
    )
    
    # Merge final video
    success = processor.merge_videos(
        "video1.mp4",
        "video2.mp4",
        transition_path,
        "final_output.mp4"
    )

finally:
    processor.cleanup()
```

## Error Handling
- Check installation trước khi run
- Validate environment activation
- Handle subprocess errors
- Graceful fallback khi generation fails
- Detailed error logging

## Performance Considerations
- GPU acceleration khi available
- Memory management cho large videos
- Batch processing capabilities
- Caching cho repeated operations

## Future Enhancements
- Multiple transition styles
- Custom duration controls
- Quality settings
- Progress callbacks
- Async generation support 