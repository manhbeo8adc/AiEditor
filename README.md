# AI Video Editor

An intelligent video processing application that leverages AI for advanced video editing and enhancement.

## 🏗️ System Architecture

### Hybrid CPU/GPU Processing Strategy

```
🎬 VIDEO INPUT
    ↓
📹 FFmpeg CUDA (Video decode) ← GPU acceleration ✅
    ↓  
🖼️ FRAMES (stored as files)
    ↓
🔄 OpenCV CPU (Basic operations) ← CPU sufficient ✅
    ↓
🧠 PyTorch CUDA (AI inference) ← GPU acceleration ✅  
    ↓
🎨 PROCESSED FRAMES
    ↓
📹 FFmpeg NVENC (Video encode) ← GPU acceleration ✅
    ↓
🎬 VIDEO OUTPUT
```

### Performance Optimization Principles

- **GPU for Heavy Lifting**: Video decode/encode, AI model inference
- **CPU for Lightweight Operations**: File I/O, basic image operations, coordination
- **Minimize GPU Memory Transfers**: Process in batches, keep tensors on GPU

## ✨ Features

- 🎬 **Video Processing**: GPU-accelerated video decode/encode with FFmpeg CUDA
- 🧠 **AI Integration**: PyTorch CUDA 12.8 for AI model inference
- 🖼️ **Frame Processing**: Efficient hybrid CPU/GPU processing pipeline
- 🚀 **High Performance**: Optimized for NVIDIA Blackwell GPUs (RTX 50xx series)
- 🔄 **Fallback Support**: Automatic CPU fallback for compatibility
- 📱 **Web Interface**: React-based frontend with real-time progress tracking

## 🚀 Quick Start

### Prerequisites

- **GPU**: NVIDIA GPU with CUDA support (RTX 5060 Ti or better recommended)
- **CUDA**: Version 12.8+ for Blackwell GPUs
- **Python**: 3.10+
- **Node.js**: 18+ for frontend development

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AiEditor
   ```

2. **Create conda environment**
   ```bash
   conda create -n ai_video_env python=3.10
   conda activate ai_video_env
   ```

3. **Install FFmpeg with CUDA support**
   ```bash
   conda install ffmpeg -c conda-forge
   ```

4. **Install PyTorch with CUDA 12.8**
   ```bash
   pip install torch==2.7.1+cu128 torchvision==0.22.1+cu128 torchaudio==2.7.1+cu128 --index-url https://download.pytorch.org/whl/cu128
   ```

5. **Install other dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

1. **Start the backend**
   ```bash
   conda activate ai_video_env
   python backend/app.py
   ```

2. **Start the frontend** (in a new terminal)
   ```bash
   cd frontend
   npm start
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 🔧 System Requirements

### Minimum Requirements
- **GPU**: GTX 1060 6GB or equivalent
- **RAM**: 8GB system memory
- **Storage**: 10GB free space
- **CUDA**: Version 11.8+

### Recommended Requirements (Blackwell GPUs)
- **GPU**: RTX 5060 Ti 16GB or better
- **RAM**: 32GB system memory
- **Storage**: 100GB NVMe SSD
- **CUDA**: Version 12.8

## 📊 Performance

### GPU Acceleration (RTX 5060 Ti Blackwell)
- **Video Decode**: 4K@60fps real-time
- **AI Inference**: 30-60 FPS depending on model
- **Video Encode**: 4K@30fps real-time with NVENC
- **Overall**: 5-10x speedup vs CPU-only

### CPU Processing (Fallback)
- **Video Decode**: 1080p@30fps
- **AI Inference**: 1-5 FPS depending on model
- **Video Encode**: 1080p@15fps with x264
- **Overall**: Functional but slower

## 🧩 Architecture Components

### Backend (Python/Flask)
- **VideoProcessor**: Hybrid CPU/GPU video processing pipeline
- **Wan2GPWrapper**: AI model integration with PyTorch CUDA
- **API Endpoints**: RESTful API for video processing operations
- **File Management**: Temporary file handling and cleanup

### Frontend (React)
- **Upload Interface**: Drag-and-drop video upload with progress tracking
- **Processing Dashboard**: Real-time processing status and progress
- **Preview Player**: Video preview and playback functionality
- **Settings Panel**: Configuration and processing options

### Processing Pipeline
1. **Video Upload**: Chunked upload with validation
2. **Frame Extraction**: FFmpeg CUDA hardware decode
3. **AI Processing**: PyTorch CUDA model inference
4. **Frame Assembly**: FFmpeg NVENC hardware encode
5. **Output Delivery**: Processed video download

## 🚨 Common Issues

### OpenCV CUDA Warning
```
WARNING: OpenCV CUDA not available
```
**This is expected and doesn't affect performance.** GPU acceleration is handled by FFmpeg and PyTorch where it matters most.

### GPU Memory Issues
If you encounter GPU memory errors:
1. Reduce batch size in processing
2. Process frames individually
3. Clear GPU cache between operations
4. Use CPU fallback for large videos

## 🔬 Testing

### Test GPU Setup
```bash
python test_pytorch.py
```

### Test Video Processing
```bash
python backend/video_processor.py
```

### Test API Endpoints
```bash
# Start backend first, then:
curl http://localhost:5000/api/status
```

## 📚 Documentation

- [Deployment Strategy](docs/deployment-strategy.md) - Cross-platform deployment guide
- [Blackwell Compatibility](docs/blackwell-compatibility.md) - GPU compatibility notes
- [OpenCV CUDA Solution](docs/opencv-cuda-solution.md) - Architecture decisions
- [Testing Guide](docs/testing/step1-testing-guide.md) - Comprehensive testing procedures

## 🛠️ Development

### Project Structure
```
AiEditor/
├── backend/                 # Python Flask backend
│   ├── app.py              # Main Flask application
│   ├── video_processor.py  # Video processing pipeline
│   └── wan2gp_wrapper.py   # AI model wrapper
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   └── components/    # UI components
│   └── public/            # Static assets
├── docs/                  # Documentation
├── temp/                  # Temporary processing files
├── uploads/               # Video upload directory
├── output/                # Processed video output
└── requirements.txt       # Python dependencies
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 TODO

See [TODO.md](TODO.md) for detailed development roadmap and current tasks.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **NVIDIA**: For CUDA toolkit and GPU acceleration
- **FFmpeg**: For excellent video processing capabilities
- **PyTorch**: For AI model inference framework
- **OpenCV**: For computer vision operations
- **React**: For modern frontend framework

## ⚠️ Cài đặt PyTorch theo GPU

**Quan trọng**: PyTorch cần được cài đặt riêng theo loại GPU của bạn. Không dùng `pip install -r requirements.txt` mà chưa cài PyTorch trước.

### 🔥 RTX 50xx Series (Blackwell Architecture)

Cho GPU RTX 5060 Ti, 5070, 5070 Ti, 5080, 5090:

```bash
# Kích hoạt environment
conda activate ai_video_env

# Cài PyTorch với CUDA 12.8 (Blackwell compatible)
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128

# Hoặc dùng version stable (nếu có)
pip install torch==2.7.1+cu128 torchvision==0.22.1+cu128 torchaudio==2.7.1+cu128 --index-url https://download.pytorch.org/whl/cu128
```

**Lưu ý RTX 50xx:**
- Blackwell GPUs yêu cầu CUDA 12.8+
- Một số features có thể cần nightly builds
- Tham khảo: [Nvidia Blackwell Installation Guide](https://github.com/deepbeepmeep/Wan2GP/blob/main/docs/INSTALLATION.md)

### ⚡ RTX 40xx Series (Ada Lovelace) 

Cho GPU RTX 4060, 4060 Ti, 4070, 4070 Ti, 4080, 4090:

```bash
# Kích hoạt environment
conda activate ai_video_env

# Cài PyTorch với CUDA 12.4 (tương thích tốt với RTX 40xx)
pip install torch==2.4.1+cu124 torchvision==0.19.1+cu124 torchaudio==2.4.1+cu124 --index-url https://download.pytorch.org/whl/cu124

# Hoặc CUDA 12.1 (ổn định hơn)
pip install torch==2.4.1+cu121 torchvision==0.19.1+cu121 torchaudio==2.4.1+cu121 --index-url https://download.pytorch.org/whl/cu121
```

### 🖥️ CPU Only (Không có GPU)

```bash
# Kích hoạt environment
conda activate ai_video_env

# Cài PyTorch CPU-only
pip install torch==2.4.1+cpu torchvision==0.19.1+cpu torchaudio==2.4.1+cpu --index-url https://download.pytorch.org/whl/cpu
```

### 📦 Cài đặt các dependencies khác

Sau khi cài PyTorch, cài các dependencies còn lại:

```bash
# Cài các dependencies khác
pip install -r requirements.txt
```

## 🚀 Hướng dẫn cài đặt đầy đủ

### Bước 1: Tạo Conda Environment
```bash
# Tạo environment mới
conda create -n ai_video_env python=3.10

# Kích hoạt environment
conda activate ai_video_env
```

### Bước 2: Cài đặt PyTorch (theo GPU)
**Chọn 1 trong 3 cách ở phần trên**

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Tạo thư mục
```bash
mkdir temp uploads output
```

### Bước 5: Kiểm tra cài đặt
```bash
# Test PyTorch
python test_pytorch.py

# Test backend
python backend/app.py
```

## 🧪 Testing

### Test Security Features (Step 2)
```bash
# Test Rate Limiting (Step 2.2)
python tests/test_rate_limiting.py

# Test CORS (Step 2.3) 
python tests/test_cors.py
```

### Test Video Processing
```bash
python test_video_processor.py
python test_wan2gp_wrapper.py
```

## 📁 Cấu trúc thư mục

```
AiEditor/
├── backend/           # Flask backend
├── frontend/          # React frontend  
├── tests/            # Test scripts
├── docs/             # Documentation
├── temp/             # Temporary files
├── uploads/          # Uploaded videos
├── output/           # Processed outputs
├── requirements.txt  # Dependencies (without PyTorch)
└── README.md         # This file
```

## 🔧 Troubleshooting

### GPU không được nhận diện
1. Kiểm tra NVIDIA driver: `nvidia-smi`
2. Kiểm tra CUDA: `nvcc --version`
3. Test PyTorch GPU: `python -c "import torch; print(torch.cuda.is_available())"`

### RTX 50xx issues
- Dùng nightly builds nếu stable không hoạt động
- Một số features có thể cần CPU fallback
- Tham khảo [Blackwell Compatibility Guide](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/)

### Dependencies conflicts
- Xóa environment và tạo lại: `conda env remove -n ai_video_env`
- Cài đúng thứ tự: PyTorch trước, requirements.txt sau

## 📋 Yêu cầu hệ thống

- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.10+
- **CUDA**: 12.1+ (cho GPU)
- **Memory**: 16GB RAM (khuyến nghị)
- **Storage**: 5GB free space

## 🤝 Đóng góp

1. Fork repo
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request

## 📄 License

MIT License - xem LICENSE file để biết thêm chi tiết. 