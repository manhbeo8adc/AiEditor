# Hướng dẫn Kiểm thử Bước 1

## Tổng quan
Hướng dẫn kiểm thử từng file code đã tạo trong bước 1 để đảm bảo hoạt động đúng.

## Yêu cầu trước khi bắt đầu
- Conda environment `ai_video_env` đã được kích hoạt
- Tất cả dependencies đã được cài đặt

## Danh sách kiểm thử

### ✅ 1. Xác minh môi trường
```bash
# Kích hoạt environment
conda activate ai_video_env

# Chạy script xác minh
python verify_setup.py
```

**Kết quả mong đợi:**
```
=== Environment Verification ===
✓ Python: 3.10.18
✓ FFmpeg: OK
✓ Node.js: OK
✓ Git: OK
✓ Directory temp: OK
✓ Directory uploads: OK
✓ Directory output: OK
✓ Directory backend: OK
✓ Directory frontend: OK

Setup complete! Ready for development.
```

### ✅ 2. Kiểm thử Backend

#### 2.1 Kiểm thử Flask App
```bash
# Khởi động backend server
python backend/app.py
```

**Kết quả mong đợi:**
```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

#### 2.2 Test API Endpoints
**Mở terminal mới (giữ server chạy):**

```bash
# Test status endpoint
curl http://localhost:5000/api/status
```

**Expected Response:**
```json
{
  "message": "AI Video Editor Backend is running",
  "status": "running",
  "version": "1.0.0"
}
```

#### 2.3 Test PyTorch GPU Compatibility
```bash
# Test PyTorch và GPU setup
python test_pytorch.py
```

**Kết quả mong đợi (GPU Blackwell - RTX 50xx):**
```
🧪 Testing PyTorch GPU Setup...
========================================
✓ PyTorch imported successfully
PyTorch Version: 2.5.1
CUDA Available: ✓
CUDA Version: 12.4
GPU Count: 1
⚠️  NVIDIA GeForce RTX 5060 Ti with CUDA capability sm_120 is not compatible
→ Falling back to CPU processing (this is expected for Blackwell GPUs)
```

**Kết quả mong đợi (GPU tương thích):**
```
🧪 Testing PyTorch GPU Setup...
✓ PyTorch imported successfully
✓ GPU Matrix multiplication: 0.0123s
🚀 GPU Speedup: 15.2x faster
🎉 PyTorch test completed successfully!
```

#### 2.4 Test Environment Detection
```bash
# Chạy script detect environment
python detect_environment.py
```

**Kết quả mong đợi:**
```
🔍 AI Video Editor - Environment Detection
==================================================
OS: Windows 10
Python: 3.10.18
Conda Available: ✓
CUDA Version: 12.9
GPU Architecture: blackwell

🚀 OPTIMAL SETUP DETECTED!
✓ Blackwell GPU with CUDA 12.4+
✓ Recommended: Use environment.yml (Blackwell optimized)
```

#### 2.5 Test Video Processor
```bash
# Test video processor với file test riêng
python test_video_processor.py
```

**Kết quả mong đợi:**
```
🎬 Testing VideoProcessor...
✅ VideoProcessor imported successfully
🚀 GPU acceleration enabled: NVIDIA GeForce RTX 5060 Ti
✅ VideoProcessor created successfully
✅ GPU info displayed during initialization
✅ Temp directory: temp
✅ Method 'extract_frames' exists
✅ Method 'merge_frames_to_video' exists
✅ Method 'process_video' exists
✅ Method 'get_video_info' exists
✅ Temp directory operations work
🎉 VideoProcessor test completed successfully!
```

#### 2.6 Test wan2GP Wrapper
```bash
# Test wan2GP wrapper với file test riêng
python test_wan2gp_wrapper.py
```

**Kết quả mong đợi:**
```
🤖 Testing Wan2GPWrapper...
✅ Wan2GPWrapper imported successfully
✅ Wan2GPWrapper created successfully
✅ Installation check result: True
✅ Method 'check_installation' exists
✅ Method 'process_video' exists
✅ Method 'get_model_info' exists
✅ Model info: {'name': 'wan2GP', 'version': '1.0.0', ...}
🎉 Wan2GPWrapper test completed successfully!
```

**💡 Tip về Python Interactive Shell:**
- **Thoát**: `exit()`, `quit()`, hoặc `Ctrl+Z` (Windows)
- **Xuống dòng**: Enter cho command mới, `...` cho multi-line code
- **Thay thế**: Dùng scripts như trên thay vì interactive shell

### ✅ 3. Frontend Testing

#### 3.1 Install Dependencies
```bash
cd frontend
npm install
```

**Expected:** No errors, dependencies installed successfully

#### 3.2 Start Development Server
```bash
npm start
```

**Expected:**
- Browser opens automatically to http://localhost:3000
- React app loads without errors
- Console shows no errors

#### 3.3 Test UI Components
**In browser:**
1. Verify page title: "AI Video Editor"
2. Verify sections: Status, Upload, Processing
3. Click "Check Backend Status" button
4. Verify status message appears

### ✅ 4. Integration Testing

#### 4.1 Full Stack Test
**Terminal 1 (Backend):**
```bash
conda activate ai_video_env
python backend/app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

**Browser Test:**
1. Open http://localhost:3000
2. Click "Check Backend Status"
3. Should show: "Backend Status: AI Video Editor Backend is running"

## Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check Python environment
python --version  # Should be 3.10.x

# Check dependencies
pip list | grep flask

# Check if environment is activated
echo $CONDA_DEFAULT_ENV  # Should show: ai_video_env
```

#### GPU/PyTorch Issues

##### Blackwell GPU (RTX 50xx) - Expected Behavior
```
⚠️  CUDA capability sm_120 is not compatible with current PyTorch
→ This is EXPECTED for RTX 50xx series
→ System will automatically fallback to CPU processing
→ See docs/blackwell-compatibility.md for details
```

##### OpenMP Warning Fix
**Automatic Fix**: Scripts `test_pytorch.py` và `detect_environment.py` đã tự động fix OpenMP warning.

**Manual Fix (nếu cần):**
```bash
# Windows PowerShell
$env:KMP_DUPLICATE_LIB_OK="TRUE"

# Linux/Mac
export KMP_DUPLICATE_LIB_OK=TRUE
```

##### PyTorch Not Found
```bash
# Verify environment activation
conda activate ai_video_env

# Reinstall PyTorch if needed
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
```

#### Frontend Won't Start
```bash
# Check Node.js
node --version  # Should be 16+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### API Connection Failed
1. Verify backend is running on port 5000
2. Check firewall settings
3. Try: `curl http://127.0.0.1:5000/api/status`

#### CORS Errors
- Verify flask-cors is installed
- Check browser console for specific errors

#### Environment Detection Issues
```bash
# Run environment detection for diagnosis
python detect_environment.py

# Check CUDA installation
nvidia-smi

# Check conda environments
conda env list
```

## Success Criteria

### ✅ All Tests Pass When:
1. `verify_setup.py` shows all ✓ marks
2. `detect_environment.py` detects setup correctly
3. `test_pytorch.py` runs without critical errors (GPU fallback OK)
4. Backend starts without errors
5. API endpoints respond correctly
6. Frontend loads and connects to backend
7. No console errors in browser
8. All Python imports work correctly

### ✅ GPU Blackwell Specific Success:
- PyTorch detects GPU but shows compatibility warning ✓
- System falls back to CPU processing automatically ✓
- FFmpeg still provides GPU acceleration for video ✓
- All functionality works despite PyTorch CPU-only ✓

## Next Steps
Sau khi tất cả tests pass, bạn có thể:
1. Commit changes: `git add . && git commit -m "Add documentation and testing"`
2. Proceed to Bước 2: Video Processing
3. Reference docs/backend/README.md và docs/frontend/README.md cho chi tiết

## File Structure Verification
```
AiEditor/
├── backend/
│   ├── app.py ✓
│   ├── video_processor.py ✓
│   └── wan2gp_wrapper.py ✓
├── frontend/
│   ├── src/
│   │   ├── App.js ✓
│   │   ├── index.js ✓
│   │   ├── App.css ✓
│   │   └── index.css ✓
│   ├── public/
│   │   └── index.html ✓
│   └── package.json ✓
├── docs/
│   ├── backend/README.md ✓
│   ├── frontend/README.md ✓
│   ├── testing/step1-testing-guide.md ✓
│   ├── deployment-strategy.md ✓
│   └── blackwell-compatibility.md ✓
├── requirements.txt ✓
├── requirements-cpu.txt ✓
├── environment.yml ✓
├── detect_environment.py ✓
├── test_pytorch.py ✓
├── test_video_processor.py ✓
├── test_wan2gp_wrapper.py ✓
├── verify_setup.py ✓
└── test_deps.py ✓
```

## Quick Test Sequence

### Chạy tất cả tests nhanh:
```bash
# 1. Verify environment
python verify_setup.py

# 2. Detect environment compatibility  
python detect_environment.py

# 3. Test PyTorch setup
python test_pytorch.py

# 4. Test backend components
python test_video_processor.py
python test_wan2gp_wrapper.py

# 5. Start backend (in background)
python backend/app.py &

# 6. Test API
curl http://localhost:5000/api/status

# 7. Test frontend (new terminal)
cd frontend && npm start
```

### Expected Timeline:
- **Environment setup**: 2-3 minutes
- **All tests**: 1-2 minutes  
- **Full stack running**: 30 seconds

**🎯 Nếu tất cả tests pass, Step 1 hoàn tất thành công!** 