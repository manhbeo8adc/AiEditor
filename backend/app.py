"""
AI Video Editor - Flask Backend Application with Security

This is the main Flask application that provides REST API endpoints
for video processing, upload, and AI transition generation.

Author: AI Video Editor Team
Version: 1.0.0
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import functools
import logging
import re
import html
import uuid
from werkzeug.utils import secure_filename
from video_processor import VideoProcessor

# Try to import magic, with fallback for Windows
try:
    import magic
    MAGIC_AVAILABLE = True
    print("✅ python-magic loaded successfully")
except ImportError:
    print("⚠️  python-magic not available, using fallback file validation")
    print("   Tip: conda activate ai_video_env && pip install python-magic")
    MAGIC_AVAILABLE = False
except Exception as e:
    print(f"⚠️  python-magic import error: {e}")
    print("   Using fallback file validation")
    MAGIC_AVAILABLE = False

# Initialize Flask application
app = Flask(__name__)

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key-change-in-production')

# Rate Limiting Configuration
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Restrictive CORS for production
CORS(app, 
     origins=['http://localhost:3000'],  # Only allow frontend
     methods=['GET', 'POST'],           # Only needed methods
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=False)

# Configuration settings for file paths
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # User uploaded videos
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'output')   # Final processed videos
app.config['TEMP_FOLDER'] = os.path.join(os.getcwd(), 'temp')       # Temporary processing files

# Security Configuration
ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# Initialize VideoProcessor
video_processor = VideoProcessor()

# Security Functions
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

def validate_video_file(file_path, original_filename):
    """Secure file validation using magic bytes (with fallback)"""
    
    # Check file extension
    _, ext = os.path.splitext(original_filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {ext} not allowed")
    
    # Check file size
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        raise ValueError("File too large")
    
    # Check magic bytes (real file type) if available
    if MAGIC_AVAILABLE:
        try:
            file_type = magic.from_file(file_path, mime=True)
            allowed_mimes = {
                'video/mp4', 'video/x-msvideo', 'video/quicktime',
                'video/x-matroska', 'video/webm'
            }
            
            if file_type not in allowed_mimes:
                raise ValueError(f"Invalid file type: {file_type}")
        except Exception as e:
            print(f"⚠️  Magic detection failed, using extension validation: {e}")
            # Fall back to extension validation only
    else:
        print("⚠️  Using extension-based validation (magic not available)")
        # Additional basic validation - check file header
        try:
            with open(file_path, 'rb') as f:
                header = f.read(12)
                # Basic MP4 signature check
                if ext == '.mp4' and not (b'ftyp' in header or b'mp4' in header):
                    raise ValueError("File does not appear to be a valid MP4")
        except Exception as e:
            print(f"⚠️  Header validation failed: {e}")
    
    return True

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

# API Endpoints
@app.route('/api/status', methods=['GET'])
def status():
    """
    Health check endpoint to verify backend is running
    
    Returns:
        JSON: Status information including version and message
    """
    return jsonify({
        "status": "running",
        "message": "AI Video Editor Backend is running",
        "version": "1.0.0"
    })

@app.route('/api/upload', methods=['POST'])
@limiter.limit("5 per minute")  # Upload limit
@validate_request(['video1', 'video2'])
def upload_videos():
    """
    Upload endpoint for video files with security validation
    
    Expected: Two video files (video1, video2) via multipart/form-data
    Returns:
        JSON: Upload status and file information
    """
    try:
        # Get uploaded files
        video1 = request.files.get('video1')
        video2 = request.files.get('video2')
        
        if not video1 or not video2:
            return SafeErrorHandler.public_error("invalid_format")
        
        # Check if files have filenames
        if video1.filename == '' or video2.filename == '':
            return SafeErrorHandler.public_error("invalid_format")
        
        upload_results = []
        
        # Process each video file
        for video_file, video_name in [(video1, 'video1'), (video2, 'video2')]:
            # Generate secure file path
            secure_path = secure_file_path(video_file.filename, app.config['UPLOAD_FOLDER'])
            
            # Save file temporarily for validation
            video_file.save(secure_path)
            
            try:
                # Validate file security
                validate_video_file(secure_path, video_file.filename)
                
                # Get file metadata using OpenCV
                import cv2
                cap = cv2.VideoCapture(secure_path)
                
                if not cap.isOpened():
                    raise ValueError("Cannot open video file")
                
                # Extract metadata
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = frame_count / fps if fps > 0 else 0
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                cap.release()
                
                upload_results.append({
                    "file_name": video_name,
                    "original_name": video_file.filename,
                    "secure_path": secure_path,
                    "size_bytes": os.path.getsize(secure_path),
                    "duration_seconds": round(duration, 2),
                    "resolution": f"{width}x{height}",
                    "fps": round(fps, 2),
                    "frame_count": frame_count
                })
                
            except Exception as e:
                # Remove file if validation fails
                if os.path.exists(secure_path):
                    os.remove(secure_path)
                
                SafeErrorHandler.log_detailed_error(e, f"File validation failed for {video_name}")
                
                if "File type" in str(e) or "not allowed" in str(e):
                    return SafeErrorHandler.public_error("invalid_format")
                elif "too large" in str(e):
                    return SafeErrorHandler.public_error("file_too_large")
                else:
                    return SafeErrorHandler.public_error("processing_failed")
        
        return jsonify({
            "message": "Files uploaded successfully",
            "status": "success",
            "files": upload_results
        })
        
    except Exception as e:
        SafeErrorHandler.log_detailed_error(e, "upload_videos")
        return SafeErrorHandler.public_error("processing_failed")

@app.route('/api/extract-frames', methods=['POST'])
@limiter.limit("10 per minute")
def extract_frames():
    """
    Extract frames from uploaded videos for transition generation
    
    Expected: JSON with video file paths
    Returns:
        JSON: Extracted frame paths and metadata
    """
    try:
        data = request.get_json()
        if not data or 'video1_path' not in data or 'video2_path' not in data:
            return SafeErrorHandler.public_error("invalid_format")
        
        video1_path = sanitize_user_input(data['video1_path'])
        video2_path = sanitize_user_input(data['video2_path'])
        
        # Extract transition frames
        last_frame, first_frame = video_processor.extract_transition_frames(
            video1_path, video2_path
        )
        
        return jsonify({
            "message": "Frames extracted successfully",
            "status": "success",
            "frames": {
                "last_frame": last_frame,
                "first_frame": first_frame
            }
        })
        
    except Exception as e:
        SafeErrorHandler.log_detailed_error(e, "extract_frames")
        return SafeErrorHandler.public_error("processing_failed")

@app.route('/api/generate-transition', methods=['POST'])
@limiter.limit("2 per minute")  # Processing limit
def generate_transition():
    """
    Generate AI transition video using wan2GP
    
    Expected: JSON with frame paths and transition parameters
    Returns:
        JSON: Generated transition video path
    """
    try:
        data = request.get_json()
        if not data or 'last_frame' not in data or 'first_frame' not in data:
            return SafeErrorHandler.public_error("invalid_format")
        
        last_frame = sanitize_user_input(data['last_frame'])
        first_frame = sanitize_user_input(data['first_frame'])
        duration = data.get('duration', 2.5)  # Default 2.5 seconds
        
        # TODO: Integrate with wan2GP for actual AI generation
        # For now, create a simple transition video
        import uuid
        transition_path = os.path.join(app.config['TEMP_FOLDER'], f"transition_{uuid.uuid4().hex[:8]}.mp4")
        
        # Create a simple crossfade transition using FFmpeg
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1', '-i', last_frame,
            '-loop', '1', '-i', first_frame,
            '-filter_complex', f'[0:v][1:v]xfade=transition=fade:duration={duration}:offset=0',
            '-t', str(duration),
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            transition_path
        ]
        
        result = video_processor.execute_safe_command(cmd, timeout=120)
        
        return jsonify({
            "message": "Transition generated successfully",
            "status": "success",
            "transition_path": transition_path,
            "duration": duration
        })
        
    except Exception as e:
        SafeErrorHandler.log_detailed_error(e, "generate_transition")
        return SafeErrorHandler.public_error("processing_failed")

@app.route('/api/merge-videos', methods=['POST'])
@limiter.limit("10 per minute")
def merge_videos():
    """
    Merge original videos with AI-generated transition
    
    Expected: JSON with video paths and merge parameters
    Returns:
        JSON: Final merged video path
    """
    try:
        data = request.get_json()
        required_fields = ['video1_path', 'video2_path', 'transition_path']
        
        for field in required_fields:
            if field not in data:
                return SafeErrorHandler.public_error("invalid_format")
        
        video1_path = sanitize_user_input(data['video1_path'])
        video2_path = sanitize_user_input(data['video2_path'])
        transition_path = sanitize_user_input(data['transition_path'])
        
        # Generate output filename
        import uuid
        output_filename = f"merged_video_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Merge videos
        final_path = video_processor.merge_videos_with_transition(
            video1_path, transition_path, video2_path, output_path
        )
        
        return jsonify({
            "message": "Videos merged successfully",
            "status": "success",
            "output_path": final_path,
            "download_url": f"/api/download/{output_filename}"
        })
        
    except Exception as e:
        SafeErrorHandler.log_detailed_error(e, "merge_videos")
        return SafeErrorHandler.public_error("processing_failed")

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Download processed video file
    
    Args:
        filename: Name of the file to download
    Returns:
        File: Video file or error message
    """
    try:
        # Sanitize filename to prevent directory traversal
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return SafeErrorHandler.public_error("file_not_found", 404)
        
        from flask import send_file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )
        
    except Exception as e:
        SafeErrorHandler.log_detailed_error(e, "download_file")
        return SafeErrorHandler.public_error("processing_failed")

# Error Handlers
@app.errorhandler(429)
def ratelimit_handler(e):
    return SafeErrorHandler.public_error("rate_limit_exceeded", 429)

@app.errorhandler(500)
def internal_error(error):
    SafeErrorHandler.log_detailed_error(error, "internal_server_error")
    return SafeErrorHandler.public_error("server_error", 500)

if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Ensure required directories exist before starting server
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
    
    # Start Flask development server
    # host='0.0.0.0' allows external connections
    # port=5000 is the default Flask port
    # debug=True enables auto-reload and detailed error messages
    app.run(debug=True, host='0.0.0.0', port=5000) 