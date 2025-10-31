"""
Example: Integrating Audio Logger with Flask Web Interface
This demonstrates how to add audio recording to your existing web application
"""

from flask import Flask, render_template, jsonify, request
from audio_logger import AudioToTextLogger
import os

app = Flask(__name__)

# Initialize audio logger
audio_logger = AudioToTextLogger(
    audio_dir="logs/audio",
    transcript_dir="logs/transcripts",
    process_interval=5,
    engine="google"  # Change to "whisper" for offline mode
)


@app.route('/')
def index():
    """Render main page with audio controls."""
    return render_template('audio_interface.html')


@app.route('/api/audio/start', methods=['POST'])
def start_recording():
    """Start audio recording session."""
    try:
        session_id = audio_logger.start_recording()
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Recording started'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/audio/stop', methods=['POST'])
def stop_recording():
    """Stop audio recording session."""
    try:
        summary = audio_logger.stop_recording()
        return jsonify({
            'success': True,
            'summary': summary,
            'message': 'Recording stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/audio/status', methods=['GET'])
def get_status():
    """Get current recording status."""
    try:
        info = audio_logger.get_session_info()
        return jsonify({
            'success': True,
            'status': info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/audio/transcripts', methods=['GET'])
def get_transcripts():
    """Get transcripts for current or specified session."""
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
def search_keywords():
    """Search for keywords in transcripts."""
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        session_id = data.get('session_id', None)
        case_sensitive = data.get('case_sensitive', False)
        
        matches = audio_logger.search_keywords(
            keywords, 
            session_id, 
            case_sensitive
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


@app.route('/api/audio/sessions', methods=['GET'])
def list_sessions():
    """List all available recording sessions."""
    try:
        sessions = audio_logger.list_sessions()
        return jsonify({
            'success': True,
            'sessions': sessions,
            'count': len(sessions)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Audio Logger Web Interface")
    print("=" * 60)
    print("\nStarting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    # Ensure logger is stopped on exit
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        if audio_logger.is_recording:
            print("\nStopping recording before exit...")
            audio_logger.stop_recording()
