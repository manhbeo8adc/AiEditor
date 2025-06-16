# Security & Validation Guide

## File Upload Security

### File Type Validation
```python
# Secure file validation function
import magic
import os

ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

def validate_video_file(file_path, original_filename):
    """Secure file validation using magic bytes"""
    
    # Check file extension
    _, ext = os.path.splitext(original_filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {ext} not allowed")
    
    # Check file size
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        raise ValueError("File too large")
    
    # Check magic bytes (real file type)
    file_type = magic.from_file(file_path, mime=True)
    allowed_mimes = {
        'video/mp4', 'video/x-msvideo', 'video/quicktime',
        'video/x-matroska', 'video/webm'
    }
    
    if file_type not in allowed_mimes:
        raise ValueError(f"Invalid file type: {file_type}")
    
    return True
```

### Path Traversal Prevention
```python
import os
import uuid
from werkzeug.utils import secure_filename

def secure_file_path(filename, upload_dir='uploads'):
    """Generate secure file path preventing directory traversal"""
    
    # Sanitize filename
    filename = secure_filename(filename)
    if not filename:
        filename = 'unnamed_file'
    
    # Generate unique prefix
    unique_id = str(uuid.uuid4())[:8]
    secure_name = f"{unique_id}_{filename}"
    
    # Ensure upload directory exists và is safe
    upload_dir = os.path.abspath(upload_dir)
    if not upload_dir.startswith(os.path.abspath('.')):
        raise ValueError("Invalid upload directory")
    
    os.makedirs(upload_dir, exist_ok=True)
    
    return os.path.join(upload_dir, secure_name)
```

### Input Sanitization
```python
import re
import html

def sanitize_user_input(input_string, max_length=1000):
    """Sanitize user input for prompts và filenames"""
    
    if not input_string:
        return ""
    
    # Remove potentially dangerous characters
    input_string = re.sub(r'[<>:"/\\|?*]', '', input_string)
    
    # HTML escape
    input_string = html.escape(input_string)
    
    # Limit length
    input_string = input_string[:max_length]
    
    # Remove excessive whitespace
    input_string = ' '.join(input_string.split())
    
    return input_string
```

## API Security

### Request Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/upload', methods=['POST'])
@limiter.limit("5 per minute")  # Upload limit
def upload_videos():
    pass

@app.route('/api/generate-transition', methods=['POST'])
@limiter.limit("2 per minute")  # Processing limit
def generate_transition():
    pass
```

### CORS Configuration
```python
from flask_cors import CORS

# Restrictive CORS for production
CORS(app, 
     origins=['http://localhost:3000'],  # Only allow frontend
     methods=['GET', 'POST'],           # Only needed methods
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=False)
```

### Request Validation
```python
from flask import request, jsonify
import functools

def validate_request(required_fields=None):
    """Decorator for request validation"""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Check content type
            if request.content_type and not request.content_type.startswith('multipart/form-data'):
                if not request.is_json:
                    return jsonify({'error': 'Invalid content type'}), 400
            
            # Validate required fields
            if required_fields:
                for field in required_fields:
                    if field not in request.files and field not in request.form:
                        return jsonify({'error': f'Missing field: {field}'}), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/upload', methods=['POST'])
@validate_request(['video1', 'video2'])
def upload_videos():
    pass
```

## File System Security

### Temporary File Management
```python
import tempfile
import atexit
import shutil

class SecureTempManager:
    def __init__(self):
        self.temp_dirs = []
        atexit.register(self.cleanup)
    
    def create_temp_dir(self):
        """Create secure temporary directory"""
        temp_dir = tempfile.mkdtemp(prefix='ai_video_')
        os.chmod(temp_dir, 0o700)  # Owner only
        self.temp_dirs.append(temp_dir)
        return temp_dir
    
    def cleanup(self):
        """Clean up all temporary directories"""
        for temp_dir in self.temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

temp_manager = SecureTempManager()
```

### File Permission Management
```python
import stat

def set_secure_permissions(file_path):
    """Set secure file permissions"""
    # Owner read/write only
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)

def create_secure_directory(dir_path):
    """Create directory with secure permissions"""
    os.makedirs(dir_path, mode=0o700, exist_ok=True)
```

## Process Security

### Command Injection Prevention
```python
import subprocess
import shlex

def safe_ffmpeg_command(input_files, output_file):
    """Build safe FFmpeg command preventing injection"""
    
    # Validate input files exist và are in allowed directory
    for file_path in input_files:
        if not os.path.exists(file_path):
            raise ValueError(f"Input file not found: {file_path}")
        
        abs_path = os.path.abspath(file_path)
        allowed_dirs = [os.path.abspath('uploads'), os.path.abspath('temp')]
        
        if not any(abs_path.startswith(d) for d in allowed_dirs):
            raise ValueError(f"File not in allowed directory: {file_path}")
    
    # Build command with proper escaping
    cmd = ['ffmpeg', '-y']  # Always use list format
    for input_file in input_files:
        cmd.extend(['-i', input_file])
    
    cmd.extend(['-c:v', 'libx264', '-c:a', 'aac', output_file])
    
    return cmd

def execute_safe_command(cmd, timeout=300):
    """Execute command safely with timeout"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        return result
    except subprocess.TimeoutExpired:
        raise RuntimeError("Command timeout")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e.stderr}")
```

## Data Security

### Sensitive Data Handling
```python
import os
from cryptography.fernet import Fernet

class ConfigManager:
    def __init__(self):
        self.key = os.environ.get('ENCRYPTION_KEY')
        if not self.key:
            self.key = Fernet.generate_key()
            print("Warning: Generated new encryption key")
        
        self.cipher = Fernet(self.key)
    
    def encrypt_config(self, data):
        """Encrypt sensitive configuration data"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_config(self, encrypted_data):
        """Decrypt configuration data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

### Log Security
```python
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_secure_logging():
    """Setup secure logging configuration"""
    
    # Create logs directory
    log_dir = 'logs'
    os.makedirs(log_dir, mode=0o700, exist_ok=True)
    
    # Configure handler
    handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Set secure permissions on log files
    os.chmod(os.path.join(log_dir, 'app.log'), 0o600)
    
    # Configure formatter (avoid sensitive data)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Setup logger
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger

def safe_log_message(message, user_input=None):
    """Log message safely, sanitizing user input"""
    if user_input:
        # Remove sensitive patterns
        user_input = re.sub(r'[<>:"/\\|?*]', '[FILTERED]', str(user_input))
        user_input = user_input[:100]  # Limit length
        return f"{message} - User input: {user_input}"
    return message
```

## Error Handling Security

### Safe Error Messages
```python
class SafeErrorHandler:
    @staticmethod
    def public_error(message, error_code=400):
        """Return safe error message for users"""
        safe_messages = {
            'file_too_large': 'File size exceeds limit',
            'invalid_format': 'File format not supported',
            'processing_failed': 'Processing failed, please try again',
            'server_error': 'Internal server error'
        }
        
        return jsonify({
            'error': safe_messages.get(message, 'An error occurred'),
            'code': error_code
        }), error_code
    
    @staticmethod
    def log_detailed_error(error, context=None):
        """Log detailed error for debugging"""
        logger = logging.getLogger(__name__)
        error_msg = f"Error: {str(error)}"
        if context:
            error_msg += f" Context: {context}"
        logger.error(error_msg, exc_info=True)
```

## Security Checklist

### Pre-deployment Security Check
```python
def security_audit():
    """Run security audit checks"""
    checks = []
    
    # Check file permissions
    sensitive_dirs = ['uploads', 'temp', 'output', 'logs']
    for dir_name in sensitive_dirs:
        if os.path.exists(dir_name):
            stat_info = os.stat(dir_name)
            if stat_info.st_mode & 0o077:  # Check if group/other have access
                checks.append(f"❌ {dir_name} has insecure permissions")
            else:
                checks.append(f"✓ {dir_name} permissions OK")
    
    # Check environment variables
    required_env = ['FLASK_SECRET_KEY', 'ENCRYPTION_KEY']
    for env_var in required_env:
        if os.environ.get(env_var):
            checks.append(f"✓ {env_var} is set")
        else:
            checks.append(f"❌ {env_var} not set")
    
    # Check debug mode
    if os.environ.get('FLASK_ENV') == 'production':
        checks.append("✓ Production mode enabled")
    else:
        checks.append("❌ Debug mode detected in production")
    
    return checks
```

### Runtime Security Monitoring
```python
import psutil
import time

class SecurityMonitor:
    def __init__(self):
        self.max_memory = 2 * 1024 * 1024 * 1024  # 2GB
        self.max_cpu_time = 300  # 5 minutes
    
    def monitor_process(self, pid):
        """Monitor process for resource abuse"""
        try:
            process = psutil.Process(pid)
            
            # Check memory usage
            memory_info = process.memory_info()
            if memory_info.rss > self.max_memory:
                return False, "Memory limit exceeded"
            
            # Check CPU time
            cpu_times = process.cpu_times()
            total_cpu_time = cpu_times.user + cpu_times.system
            if total_cpu_time > self.max_cpu_time:
                return False, "CPU time limit exceeded"
            
            return True, "OK"
            
        except psutil.NoSuchProcess:
            return False, "Process not found"
``` 