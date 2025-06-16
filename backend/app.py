"""
AI Video Editor - Flask Backend Application

This is the main Flask application that provides REST API endpoints
for video processing, upload, and AI transition generation.

Author: AI Video Editor Team
Version: 1.0.0
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for frontend communication
CORS(app)

# Configuration settings for file paths
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # User uploaded videos
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'output')   # Final processed videos
app.config['TEMP_FOLDER'] = os.path.join(os.getcwd(), 'temp')       # Temporary processing files

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
def upload_videos():
    """
    Upload endpoint for video files
    
    Expected: Two video files (video1, video2) via multipart/form-data
    Returns:
        JSON: Upload status and file information
    
    TODO: Implement secure file upload with validation
    """
    # TODO: Implement video upload logic
    return jsonify({"message": "Upload endpoint - to be implemented"})

@app.route('/api/extract-frames', methods=['POST'])
def extract_frames():
    """
    Extract frames from uploaded videos for transition generation
    
    Expected: JSON with video file paths
    Returns:
        JSON: Extracted frame paths and metadata
    
    TODO: Implement frame extraction using OpenCV
    """
    # TODO: Implement frame extraction logic
    return jsonify({"message": "Extract frames endpoint - to be implemented"})

@app.route('/api/generate-transition', methods=['POST'])
def generate_transition():
    """
    Generate AI transition video using wan2GP
    
    Expected: JSON with frame paths and transition parameters
    Returns:
        JSON: Generated transition video path
    
    TODO: Integrate with wan2GP for AI transition generation
    """
    # TODO: Implement wan2GP transition generation
    return jsonify({"message": "Generate transition endpoint - to be implemented"})

@app.route('/api/merge-videos', methods=['POST'])
def merge_videos():
    """
    Merge original videos with AI-generated transition
    
    Expected: JSON with video paths and merge parameters
    Returns:
        JSON: Final merged video path
    
    TODO: Implement video merging using FFmpeg
    """
    # TODO: Implement video merging logic
    return jsonify({"message": "Merge videos endpoint - to be implemented"})

if __name__ == '__main__':
    # Ensure required directories exist before starting server
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
    
    # Start Flask development server
    # host='0.0.0.0' allows external connections
    # port=5000 is the default Flask port
    # debug=True enables auto-reload and detailed error messages
    app.run(debug=True, host='0.0.0.0', port=5000) 