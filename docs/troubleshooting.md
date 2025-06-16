# Troubleshooting Guide

## Environment Setup Issues

### FFmpeg Not Found
**Error:** `ffmpeg: command not found` hoặc `FileNotFoundError: ffmpeg`

**Solutions:**
- **Windows:** Download từ https://ffmpeg.org/download.html, add to PATH
- **macOS:** `brew install ffmpeg`
- **Ubuntu:** `sudo apt install ffmpeg`
- **Verify:** `ffmpeg -version` should return version info

### wan2GP CUDA Errors
**Error:** `CUDA out of memory` hoặc `No CUDA devices available`

**Solutions:**
1. **GPU Memory Issues:**
   ```python
   # Reduce batch size in wan2gp_config.yaml
   batch_size: 1
   # Enable gradient checkpointing
   gradient_checkpointing: true
   ```

2. **No GPU Available:**
   ```python
   # Force CPU mode in wan2gp_wrapper.py
   device = torch.device('cpu')
   ```

3. **CUDA Version Mismatch:**
   - Check: `nvidia-smi` và `nvcc --version`
   - Install compatible PyTorch: `pip install torch==2.0.1+cu118`

### Python Dependencies Issues
**Error:** `ModuleNotFoundError` hoặc version conflicts

**Solutions:**
```bash
# Create clean virtual environment
python -m venv venv_clean
source venv_clean/bin/activate  # Linux/Mac
venv_clean\Scripts\activate     # Windows

# Install exact versions
pip install -r requirements_exact.txt
```

## Runtime Issues

### Memory Overflow
**Error:** `RuntimeError: CUDA out of memory` during processing

**Solutions:**
1. **Reduce video resolution:**
   ```python
   # In video_processor.py
   target_resolution = (720, 480)  # Instead of (1024, 576)
   ```

2. **Process in chunks:**
   ```python
   # Enable frame batching
   batch_size = 4  # Reduce from 8
   ```

### Port Conflicts
**Error:** `Address already in use: Port 5000`

**Solutions:**
```python
# In app.py, change port
app.run(host='0.0.0.0', port=5001, debug=True)
```

```javascript
// In frontend api.js, update base URL
const BASE_URL = 'http://localhost:5001';
```

### File Permission Errors
**Error:** `PermissionError: [Errno 13] Permission denied`

**Solutions:**
```bash
# Create directories with proper permissions
mkdir -p uploads temp output
chmod 755 uploads temp output

# Fix file permissions
sudo chown -R $USER:$USER ai-video-editor/
```

## Processing Issues

### Video Format Compatibility
**Error:** `Unsupported format` hoặc codec errors

**Solutions:**
1. **Convert to supported format:**
   ```bash
   ffmpeg -i input.mov -c:v libx264 -c:a aac output.mp4
   ```

2. **Update format validation:**
   ```python
   SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
   ```

### Audio Sync Issues
**Error:** Audio và video out of sync sau merge

**Solutions:**
```python
# In video_processor.py merge function
ffmpeg_cmd = [
    'ffmpeg', '-i', 'input.mp4',
    '-c:v', 'copy', '-c:a', 'aac',
    '-avoid_negative_ts', 'make_zero',
    'output.mp4'
]
```

## Network & API Issues

### CORS Errors
**Error:** `Access-Control-Allow-Origin` errors

**Solutions:**
```python
# In app.py
from flask_cors import CORS
CORS(app, origins=['http://localhost:3000'])
```

### Request Timeout
**Error:** `Request timeout` during large file upload

**Solutions:**
```javascript
// In api.js
const api = axios.create({
  timeout: 300000, // 5 minutes
  maxContentLength: 500 * 1024 * 1024 // 500MB
});
```

## Development Issues

### React Build Errors
**Error:** `Module not found` hoặc build failures

**Solutions:**
```bash
# Clear cache và reinstall
rm -rf node_modules package-lock.json
npm install

# Update dependencies
npm audit fix
```

### Hot Reload Not Working
**Issue:** Changes không reflect trong development

**Solutions:**
```json
// In package.json
"scripts": {
  "start": "WATCHPACK_POLLING=true react-scripts start"
}
```

## Performance Issues

### Slow Processing
**Issue:** Video generation takes too long

**Solutions:**
1. **Optimize wan2GP settings:**
   ```yaml
   # wan2gp_config.yaml
   inference_steps: 25  # Reduce from 50
   guidance_scale: 7.5  # Reduce from 15
   ```

2. **Enable GPU acceleration:**
   ```python
   # Verify GPU usage
   print(torch.cuda.is_available())
   print(torch.cuda.get_device_name(0))
   ```

## Quick Diagnostic Commands

```bash
# Check system resources
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().percent}%')"
nvidia-smi  # GPU status

# Test dependencies
python -c "import cv2, torch, flask; print('All deps OK')"

# Check file permissions
ls -la uploads/ temp/ output/

# Test FFmpeg
ffmpeg -f lavfi -i testsrc=duration=1:size=320x240:rate=1 test.mp4
```

## Emergency Recovery

### Complete Reset
```bash
# Backup important files
cp -r uploads/ uploads_backup/
cp -r output/ output_backup/

# Clean restart
rm -rf temp/* venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Rollback Changes
```bash
# Git rollback to last working version
git stash
git checkout [last_working_commit]
``` 