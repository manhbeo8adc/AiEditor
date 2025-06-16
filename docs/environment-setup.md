# Environment Setup Guide

## System Requirements

### Minimum Requirements
- **OS:** Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **RAM:** 8GB (12GB với wan2GP)
- **Storage:** 10GB free space
- **CPU:** Quad-core Intel i5 hoặc AMD equivalent
- **GPU:** Optional, CUDA-compatible recommended

### Recommended Requirements
- **RAM:** 16GB+ 
- **Storage:** 50GB+ SSD
- **GPU:** NVIDIA RTX 3060+ with 8GB VRAM
- **CPU:** 8-core Intel i7/AMD Ryzen 7

## Software Dependencies

### Python Environment
```bash
# Required Python version
Python 3.8, 3.9, 3.10, or 3.11
# NOTE: Python 3.12 có compatibility issues với PyTorch

# Check version
python --version
```

### Node.js Environment
```bash
# Required Node.js version
Node.js 16+ (Recommended: 18 LTS)

# Check version
node --version
npm --version
```

### FFmpeg Installation

**Windows:**
1. Download từ: https://www.gyan.dev/ffmpeg/builds/
2. Extract to C:\ffmpeg
3. Add C:\ffmpeg\bin to PATH
4. Verify: `ffmpeg -version`

**macOS:**
```bash
# Using Homebrew
brew install ffmpeg

# Verify
ffmpeg -version
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg

# For additional codecs
sudo apt install ubuntu-restricted-extras
```

### CUDA Setup (For GPU Acceleration)

**Check GPU Compatibility:**
```bash
nvidia-smi
```

**Install CUDA Toolkit:**
1. Download CUDA 11.8 từ NVIDIA developer site
2. Install theo hướng dẫn cho OS của bạn
3. Verify: `nvcc --version`

**Install cuDNN:**
1. Download cuDNN 8.x compatible với CUDA 11.8
2. Extract và copy files to CUDA directory
3. Update environment variables

## Virtual Environment Setup

### Conda Environment (Recommended)
```bash
# Create conda environment with Python 3.10
conda create -n ai_video_env python=3.10 -y

# Activate environment
conda activate ai_video_env

# Install FFmpeg via conda
conda install ffmpeg -c conda-forge -y

# Verify activation
python --version  # Should show Python 3.10.x
ffmpeg -version   # Should show FFmpeg version
```

### Python Virtual Environment (Alternative)
```bash
# Create virtual environment
python -m venv ai_video_env

# Activate
# Windows:
ai_video_env\Scripts\activate
# Linux/Mac:
source ai_video_env/bin/activate

# Verify activation
which python  # Should point to venv
```

### Environment Variables
```bash
# Windows (.env file)
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="6.0;6.1;7.0;7.5;8.0;8.6"
PYTHONPATH=%PYTHONPATH%;.\backend

# Linux/Mac (.bashrc)
export CUDA_VISIBLE_DEVICES=0
export TORCH_CUDA_ARCH_LIST="6.0;6.1;7.0;7.5;8.0;8.6"
export PYTHONPATH=$PYTHONPATH:./backend
```

## Exact Dependencies

### requirements_exact.txt
```txt
flask==2.3.3
flask-cors==4.0.0
opencv-python==4.8.1.78
torch==2.0.1+cu118
torchvision==0.15.2+cu118
torchaudio==2.0.2+cu118
numpy==1.24.3
pillow==10.0.0
ffmpeg-python==0.2.0
psutil==5.9.5
pyyaml==6.0.1
python-multipart==0.0.6
werkzeug==2.3.7
```

### package.json (exact versions)
```json
{
  "dependencies": {
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "axios": "1.5.0",
    "react-dropzone": "14.2.3",
    "react-scripts": "5.0.1"
  },
  "devDependencies": {
    "electron": "25.6.0",
    "electron-builder": "24.6.3",
    "concurrently": "8.2.0"
  }
}
```

## Installation Verification

### Python Dependencies Test
```python
# test_deps.py
import cv2
import torch
import flask
import numpy as np
from PIL import Image

print("✓ OpenCV version:", cv2.__version__)
print("✓ PyTorch version:", torch.__version__)
print("✓ CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("✓ GPU device:", torch.cuda.get_device_name(0))
print("✓ Flask version:", flask.__version__)
print("✓ NumPy version:", np.__version__)
print("All dependencies OK!")
```

### FFmpeg Test
```bash
# Test basic FFmpeg functionality
ffmpeg -f lavfi -i testsrc=duration=5:size=320x240:rate=30 test_output.mp4

# Test H.264 codec
ffmpeg -encoders | grep h264
```

### Node.js Dependencies Test
```bash
cd frontend
npm install
npm run build  # Should complete without errors
```

## Performance Optimization

### GPU Memory Optimization
```python
# Add to wan2gp_wrapper.py
import torch
torch.backends.cudnn.benchmark = True
torch.backends.cuda.matmul.allow_tf32 = True
```

### System Optimization
```bash
# Linux: Increase file limits
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# Windows: Increase virtual memory
# System > Advanced > Performance > Settings > Advanced > Virtual Memory
```

## Development Tools Setup

### Recommended IDE Extensions
**VS Code:**
- Python Extension Pack
- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- GitLens

### Git Configuration
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.autocrlf input  # Linux/Mac
git config --global core.autocrlf true   # Windows
```

## Project Structure Setup
```bash
# Create project directory
mkdir ai-video-editor
cd ai-video-editor

# Initialize git
git init

# Create basic structure
mkdir -p backend/{api,models,utils}
mkdir -p frontend/{src,public}
mkdir -p {temp,uploads,output,docs}
mkdir -p wan2gp

# Set permissions (Linux/Mac)
chmod 755 temp uploads output
```

## Final Verification Script
```python
# verify_setup.py
import subprocess
import sys
import os

def check_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

print("=== Environment Verification ===")
print("✓ Python:", sys.version.split()[0] if sys.version_info >= (3, 8) else "❌ Version too old")
print("✓ FFmpeg:", "OK" if check_command("ffmpeg -version") else "❌ Not installed")
print("✓ Node.js:", "OK" if check_command("node --version") else "❌ Not installed")
print("✓ Git:", "OK" if check_command("git --version") else "❌ Not installed")

# Check directories
dirs = ['temp', 'uploads', 'output', 'backend', 'frontend']
for d in dirs:
    print(f"✓ Directory {d}:", "OK" if os.path.exists(d) else "❌ Missing")

print("\nSetup complete! Ready for development.")
``` 