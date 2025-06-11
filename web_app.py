#!/usr/bin/env python3
"""
Web interface for Image Quality Assessment Tool
"""

from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from image_quality_assessor import ImageQualityAssessor
import tempfile

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp',
    # Raw formats
    'arw', 'cr2', 'cr3', 'nef', 'dng', 'raf', 'orf', 'rw2',
    'pef', 'srw', 'x3f', '3fr', 'fff', 'iiq', 'k25', 'kdc',
    'mef', 'mos', 'mrw', 'nrw', 'ptx', 'r3d', 'raw', 'rwl',
    'rwz', 'sr2', 'srf'
}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and assessment"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Assess image quality
            assessor = ImageQualityAssessor()
            results = assessor.assess_image(filepath)
            
            if 'error' in results:
                return jsonify({'error': results['error']}), 500
            
            # Generate natural language report
            report = assessor.generate_report(results)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'results': results,
                'report': report
            })
            
        except Exception as e:
            # Clean up uploaded file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/demo')
def demo():
    """Demo page with sample images"""
    return render_template('demo.html')

if __name__ == '__main__':
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    print("Starting Image Quality Assessment Web Server...")
    print("Access the application at: http://localhost:12000")
    app.run(host='0.0.0.0', port=12000, debug=True)