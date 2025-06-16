from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Basic configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'output')
app.config['TEMP_FOLDER'] = os.path.join(os.getcwd(), 'temp')

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "status": "running",
        "message": "AI Video Editor Backend is running",
        "version": "1.0.0"
    })

@app.route('/api/upload', methods=['POST'])
def upload_videos():
    # TODO: Implement video upload logic
    return jsonify({"message": "Upload endpoint - to be implemented"})

@app.route('/api/extract-frames', methods=['POST'])
def extract_frames():
    # TODO: Implement frame extraction logic
    return jsonify({"message": "Extract frames endpoint - to be implemented"})

@app.route('/api/generate-transition', methods=['POST'])
def generate_transition():
    # TODO: Implement wan2GP transition generation
    return jsonify({"message": "Generate transition endpoint - to be implemented"})

@app.route('/api/merge-videos', methods=['POST'])
def merge_videos():
    # TODO: Implement video merging logic
    return jsonify({"message": "Merge videos endpoint - to be implemented"})

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 