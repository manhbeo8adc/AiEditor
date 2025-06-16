# Bước 1 Testing Guide

## Overview
Hướng dẫn test từng file code đã tạo trong bước 1 để đảm bảo hoạt động đúng.

## Prerequisites
- Conda environment `ai_video_env` đã được activate
- Tất cả dependencies đã được install

## Testing Checklist

### ✅ 1. Environment Verification
```bash
# Activate environment
conda activate ai_video_env

# Run verification script
python verify_setup.py
```

**Expected Output:**
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

### ✅ 2. Backend Testing

#### 2.1 Test Flask App
```bash
# Start backend server
python backend/app.py
```

**Expected Output:**
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

#### 2.3 Test Video Processor
```bash
# Open Python interactive shell
python

# Test video processor
>>> from backend.video_processor import VideoProcessor
>>> processor = VideoProcessor()
>>> print("VideoProcessor created successfully")
>>> processor.cleanup()
>>> exit()
```

#### 2.4 Test wan2GP Wrapper
```bash
# Test wan2GP wrapper
python

>>> from backend.wan2gp_wrapper import Wan2GPWrapper
>>> wrapper = Wan2GPWrapper()
>>> print("Wrapper created:", wrapper.check_installation())
>>> exit()
```

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

## Success Criteria

### ✅ All Tests Pass When:
1. `verify_setup.py` shows all ✓ marks
2. Backend starts without errors
3. API endpoints respond correctly
4. Frontend loads and connects to backend
5. No console errors in browser
6. All Python imports work correctly

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
│   └── testing/step1-testing-guide.md ✓
├── requirements.txt ✓
├── verify_setup.py ✓
└── test_deps.py ✓
``` 