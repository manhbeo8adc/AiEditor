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