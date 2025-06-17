# Tests Folder

Thư mục chứa các test scripts cho AI Video Editor project.

## 📁 Test Scripts

### Step 2 Security Tests
- **`test_rate_limiting.py`** - Test Rate Limiting (Step 2.2)
  - Kiểm tra rate limiting hoạt động đúng
  - Blocks requests sau 5 lần thử trong thời gian ngắn
  
- **`test_cors.py`** - Test CORS Configuration (Step 2.3)  
  - Kiểm tra CORS allow/block origins đúng
  - localhost:3000 được phép, malicious sites bị chặn

## 🚀 Cách sử dụng

### Test từng bước riêng lẻ
```bash
# Bước 1: Khởi động server (Terminal 1)
conda activate ai_video_env
python backend/app.py

# Bước 2: Test Rate Limiting (Terminal 2)
python tests/test_rate_limiting.py

# Bước 3: Test CORS
python tests/test_cors.py
```

### Test tất cả security features
```bash
# Chạy tất cả tests security
python tests/test_rate_limiting.py && python tests/test_cors.py
```

## ✅ Kết quả mong đợi

### Rate Limiting Test
```
🔥 Testing Rate Limiting (Step 2.2)
✅ Status: 200
✅ Rate limiting triggered at request 6
✅ Rate limiting test PASSED
```

### CORS Test  
```
🌐 Testing CORS Configuration (Step 2.3)
✅ CORS allowed for localhost:3000
✅ CORS correctly blocked malicious origin
✅ CORS test PASSED
```

## 📋 Yêu cầu

- Backend server phải đang chạy: `python backend/app.py`
- Dependencies đã cài: `pip install requests`
- Server chạy trên: `http://localhost:5000`

## 🔧 Troubleshooting

### Server không chạy
```bash
# Kiểm tra server
curl http://localhost:5000/api/status
# Nếu error, khởi động lại server
python backend/app.py
```

### Import errors
```bash
# Cài đặt dependencies
pip install requests
```

### Connection errors
- Đảm bảo server đang chạy trên port 5000
- Kiểm tra firewall không block localhost 