"""
Mobile API Backend for SiteLenz Unified Monitoring System
Provides REST API endpoints for mobile app to access audio and camera features
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from audio_logger import AudioToTextLogger
from camera_classifier import CameraClassifier
import base64
import io
from PIL import Image
import numpy as np
import cv2
import json
from pathlib import Path
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app

# Initialize loggers
audio_logger = AudioToTextLogger(
    audio_dir="logs/audio",
    transcript_dir="logs/transcripts",
    engine="google"
)

camera_classifier = CameraClassifier(
    model_path="models/vit_weights.pth",
    frame_dir="logs/frames",
    classification_dir="logs/classifications",
    capture_interval=5
)

# Global state
app_state = {
    'audio_recording': False,
    'camera_recording': False,
    'current_session': None
}

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Serve mobile web app."""
    return render_template('mobile_app.html')

@app.route('/manifest.json')
def manifest():
    """PWA manifest for installable app."""
    return jsonify({
        'name': 'SiteLenz Monitor',
        'short_name': 'SiteLenz',
        'description': 'Building Defect Monitoring System',
        'start_url': '/',
        'display': 'standalone',
        'background_color': '#667eea',
        'theme_color': '#667eea',
        'orientation': 'portrait',
        'icons': [
            {
                'src': '/static/icon-192.png',
                'sizes': '192x192',
                'type': 'image/png'
            },
            {
                'src': '/static/icon-512.png',
                'sizes': '512x512',
                'type': 'image/png'
            }
        ]
    })

# ==================== AUDIO ENDPOINTS ====================

@app.route('/api/audio/start', methods=['POST'])
def start_audio():
    """Start audio recording session."""
    try:
        if app_state['audio_recording']:
            return jsonify({
                'success': False,
                'error': 'Audio recording already in progress'
            }), 400
        
        session_id = audio_logger.start_recording()
        app_state['audio_recording'] = True
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Audio recording started'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/audio/stop', methods=['POST'])
def stop_audio():
    """Stop audio recording session."""
    try:
        if not app_state['audio_recording']:
            return jsonify({
                'success': False,
                'error': 'No audio recording in progress'
            }), 400
        
        summary = audio_logger.stop_recording()
        app_state['audio_recording'] = False
        
        return jsonify({
            'success': True,
            'summary': summary,
            'message': 'Audio recording stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/audio/status', methods=['GET'])
def audio_status():
    """Get audio recording status."""
    try:
        info = audio_logger.get_session_info()
        return jsonify({
            'success': True,
            'is_recording': app_state['audio_recording'],
            'info': info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/audio/transcripts', methods=['GET'])
def get_transcripts():
    """Get audio transcripts."""
    try:
        session_id = request.args.get('session_id', None)
        transcripts = audio_logger.get_transcripts(session_id)
        
        return jsonify({
            'success': True,
            'transcripts': transcripts,
            'count': len(transcripts)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/audio/search', methods=['POST'])
def search_audio():
    """Search keywords in transcripts."""
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        session_id = data.get('session_id', None)
        
        matches = audio_logger.search_keywords(keywords, session_id)
        
        return jsonify({
            'success': True,
            'matches': matches,
            'count': len(matches)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== CAMERA ENDPOINTS ====================

@app.route('/api/camera/start', methods=['POST'])
def start_camera():
    """Start camera recording session."""
    try:
        if app_state['camera_recording']:
            return jsonify({
                'success': False,
                'error': 'Camera recording already in progress'
            }), 400
        
        session_id = camera_classifier.start_recording()
        app_state['camera_recording'] = True
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Camera recording started'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/camera/stop', methods=['POST'])
def stop_camera():
    """Stop camera recording session."""
    try:
        if not app_state['camera_recording']:
            return jsonify({
                'success': False,
                'error': 'No camera recording in progress'
            }), 400
        
        summary = camera_classifier.stop_recording()
        app_state['camera_recording'] = False
        
        return jsonify({
            'success': True,
            'summary': summary,
            'message': 'Camera recording stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/camera/status', methods=['GET'])
def camera_status():
    """Get camera recording status."""
    try:
        info = camera_classifier.get_session_info()
        return jsonify({
            'success': True,
            'is_recording': app_state['camera_recording'],
            'info': info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/camera/classify', methods=['POST'])
def classify_image():
    """Classify an uploaded image."""
    try:
        if 'image' not in request.files:
            # Check if base64 image in JSON
            data = request.get_json()
            if data and 'image' in data:
                # Decode base64 image
                image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
            else:
                return jsonify({
                    'success': False,
                    'error': 'No image provided'
                }), 400
        else:
            # Handle file upload
            file = request.files['image']
            image = Image.open(file.stream)
        
        # Convert PIL to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Classify
        result = camera_classifier._classify_frame(image_cv)
        
        if result:
            return jsonify({
                'success': True,
                'classification': result
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Classification failed'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/camera/classifications', methods=['GET'])
def get_classifications():
    """Get camera classifications."""
    try:
        session_id = request.args.get('session_id', None)
        classifications = camera_classifier.get_classifications(session_id)
        
        return jsonify({
            'success': True,
            'classifications': classifications,
            'count': len(classifications)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/camera/search', methods=['POST'])
def search_defects():
    """Search for specific defects."""
    try:
        data = request.get_json()
        defect_types = data.get('defect_types', [])
        session_id = data.get('session_id', None)
        min_confidence = data.get('min_confidence', 0.0)
        
        matches = camera_classifier.search_defects(
            defect_types, session_id, min_confidence
        )
        
        return jsonify({
            'success': True,
            'matches': matches,
            'count': len(matches)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== UNIFIED ENDPOINTS ====================

@app.route('/api/unified/start', methods=['POST'])
def start_both():
    """Start both audio and camera recording."""
    try:
        audio_session = audio_logger.start_recording()
        app_state['audio_recording'] = True
        
        camera_session = camera_classifier.start_recording()
        app_state['camera_recording'] = True
        
        return jsonify({
            'success': True,
            'audio_session': audio_session,
            'camera_session': camera_session,
            'message': 'Both systems started'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/unified/stop', methods=['POST'])
def stop_both():
    """Stop both audio and camera recording."""
    try:
        audio_summary = None
        camera_summary = None
        
        if app_state['audio_recording']:
            audio_summary = audio_logger.stop_recording()
            app_state['audio_recording'] = False
        
        if app_state['camera_recording']:
            camera_summary = camera_classifier.stop_recording()
            app_state['camera_recording'] = False
        
        return jsonify({
            'success': True,
            'audio_summary': audio_summary,
            'camera_summary': camera_summary,
            'message': 'Both systems stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/unified/status', methods=['GET'])
def unified_status():
    """Get status of both systems."""
    try:
        audio_info = audio_logger.get_session_info()
        camera_info = camera_classifier.get_session_info()
        
        return jsonify({
            'success': True,
            'audio': {
                'is_recording': app_state['audio_recording'],
                'info': audio_info
            },
            'camera': {
                'is_recording': app_state['camera_recording'],
                'info': camera_info
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/unified/capture', methods=['POST'])
def capture_with_voice():
    """Capture and classify image when voice is detected, return synchronized data."""
    try:
        data = request.get_json()
        
        # Get the image data
        if 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'No image provided'
            }), 400
        
        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Get transcript if provided (from latest voice capture)
        transcript = data.get('transcript', '')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Classify the image
        classification = camera_classifier._classify_frame(image_cv)
        
        if not classification:
            return jsonify({
                'success': False,
                'error': 'Image classification failed'
            }), 500
        
        # Save the synchronized log entry
        log_entry = {
            'timestamp': timestamp,
            'transcript': transcript,
            'classification': classification,
            'image_data': data['image']  # Keep base64 for display
        }
        
        # Save to a unified log file
        log_dir = Path("logs/unified")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        session_id = audio_logger.session_id if audio_logger.session_id else datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"session_{session_id}.json"
        
        # Append to existing log or create new
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return jsonify({
            'success': True,
            'entry': log_entry,
            'message': 'Synchronized capture saved'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/unified/logs', methods=['GET'])
def get_unified_logs():
    """Get all synchronized voice+image logs."""
    try:
        session_id = request.args.get('session_id', None)
        log_dir = Path("logs/unified")
        
        if not log_dir.exists():
            return jsonify({
                'success': True,
                'logs': [],
                'count': 0
            })
        
        logs = []
        
        if session_id:
            log_file = log_dir / f"session_{session_id}.json"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
        else:
            # Get all logs from all sessions
            for log_file in sorted(log_dir.glob("session_*.json"), reverse=True):
                with open(log_file, 'r') as f:
                    session_logs = json.load(f)
                    logs.extend(session_logs)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'count': len(logs)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== SESSION MANAGEMENT ====================

@app.route('/api/sessions/list', methods=['GET'])
def list_sessions():
    """List all recording sessions."""
    try:
        audio_sessions = audio_logger.list_sessions()
        camera_sessions = camera_classifier.list_sessions()
        
        # Combine and deduplicate sessions
        all_sessions = list(set(audio_sessions + camera_sessions))
        all_sessions.sort(reverse=True)
        
        return jsonify({
            'success': True,
            'sessions': all_sessions,
            'audio_sessions': audio_sessions,
            'camera_sessions': camera_sessions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session_details(session_id):
    """Get details for a specific session."""
    try:
        transcripts = audio_logger.get_transcripts(session_id)
        classifications = camera_classifier.get_classifications(session_id)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'transcripts': transcripts,
            'classifications': classifications
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'audio_available': audio_logger.model is not None if hasattr(audio_logger, 'model') else True,
        'camera_available': camera_classifier.model is not None,
        'version': '1.0.0'
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ==================== RUN SERVER ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🏗️ SiteLenz Mobile API Server")
    print("=" * 60)
    print("\nStarting server...")
    print("Mobile App: http://localhost:5000")
    print("API Docs: http://localhost:5000/api/health")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    
    # Run on all interfaces to allow mobile device access
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=True,
        threaded=True
    )
