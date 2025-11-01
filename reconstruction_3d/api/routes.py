"""
Flask API Routes for 3D Reconstruction
Handles session management, image uploads, reconstruction, and model retrieval
"""

from flask import Blueprint, request, jsonify, send_file
import os
import time
import json
import base64
from pathlib import Path
from typing import Dict, List
import logging
import threading

# Import reconstruction modules
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import SESSIONS_DIR, OUTPUT_DIR, API_CONFIG, COLMAP_CONFIG, MODEL_CONFIG
from colmap.colmap_wrapper import COLMAPWrapper
from processing.model_processor import ModelProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
reconstruction_bp = Blueprint('reconstruction_3d', __name__, url_prefix='/api/3d')

# Active sessions storage
active_sessions = {}
reconstruction_status = {}


@reconstruction_bp.route('/start-session', methods=['POST'])
def start_session():
    """
    Start a new 3D reconstruction session
    
    Request JSON:
        {
            "project_name": "room_scan_1",
            "room_type": "bedroom" (optional)
        }
    
    Returns:
        {
            "success": True,
            "session_id": "session_1234567890",
            "message": "Session started successfully"
        }
    """
    try:
        data = request.get_json() or {}
        project_name = data.get('project_name', f'project_{int(time.time())}')
        
        # Create session ID
        session_id = f"session_{int(time.time())}"
        
        # Create session folder
        session_folder = SESSIONS_DIR / session_id
        session_folder.mkdir(parents=True, exist_ok=True)
        
        # Initialize session
        active_sessions[session_id] = {
            'project_name': project_name,
            'room_type': data.get('room_type', 'unknown'),
            'folder': str(session_folder),
            'images': [],
            'annotations': [],
            'created_at': time.time(),
            'status': 'active'
        }
        
        logger.info(f"Started session: {session_id}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Session started successfully. Begin uploading images!'
        })
    
    except Exception as e:
        logger.error(f"Failed to start session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@reconstruction_bp.route('/upload-image', methods=['POST'])
def upload_image():
    """
    Upload an image with metadata to a session
    
    Request JSON:
        {
            "session_id": "session_1234567890",
            "image": "base64_encoded_image",
            "camera_pose": {
                "position": [x, y, z],
                "rotation": [qx, qy, qz, qw]
            },
            "transcript": "Voice note about this capture",
            "classification": "Major Crack" (from classification API)
        }
    
    Returns:
        {
            "success": True,
            "image_count": 15,
            "message": "Image uploaded successfully"
        }
    """
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        if not session_id or session_id not in active_sessions:
            return jsonify({'success': False, 'error': 'Invalid session ID'}), 400
        
        session = active_sessions[session_id]
        
        # Check session limits
        if len(session['images']) >= API_CONFIG['max_images_per_session']:
            return jsonify({
                'success': False,
                'error': f"Maximum {API_CONFIG['max_images_per_session']} images per session"
            }), 400
        
        # Decode and save image
        img_base64 = data.get('image')
        if not img_base64:
            return jsonify({'success': False, 'error': 'No image data provided'}), 400
        
        img_bytes = base64.b64decode(img_base64)
        img_num = len(session['images'])
        img_filename = f"img_{img_num:04d}.jpg"
        img_path = Path(session['folder']) / img_filename
        
        with open(img_path, 'wb') as f:
            f.write(img_bytes)
        
        # Store image metadata
        image_info = {
            'filename': img_filename,
            'path': str(img_path),
            'camera_pose': data.get('camera_pose', {}),
            'transcript': data.get('transcript', ''),
            'classification': data.get('classification', 'Unknown'),
            'confidence': data.get('confidence', 0.0),
            'timestamp': time.time()
        }
        
        session['images'].append(image_info)
        
        # If there's a crack, add annotation
        classification = image_info['classification']
        if classification and classification.lower() not in ['plain', 'normal', 'unknown']:
            position = data.get('camera_pose', {}).get('position', [0, 0, 0])
            session['annotations'].append({
                'position': position,
                'classification': classification,
                'transcript': image_info['transcript'],
                'image_index': img_num
            })
        
        logger.info(f"Session {session_id}: Uploaded image {img_num} ({classification})")
        
        return jsonify({
            'success': True,
            'image_count': len(session['images']),
            'annotation_count': len(session['annotations']),
            'message': f'Image {img_num} uploaded successfully'
        })
    
    except Exception as e:
        logger.error(f"Failed to upload image: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@reconstruction_bp.route('/reconstruct', methods=['POST'])
def start_reconstruction():
    """
    Start 3D reconstruction for a session
    
    Request JSON:
        {
            "session_id": "session_1234567890",
            "quality": "high" | "medium" | "low" (optional, default: medium)
        }
    
    Returns:
        {
            "success": True,
            "reconstruction_id": "recon_1234567890",
            "message": "Reconstruction started",
            "estimated_time_minutes": 5
        }
    """
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        if not session_id or session_id not in active_sessions:
            return jsonify({'success': False, 'error': 'Invalid session ID'}), 400
        
        session = active_sessions[session_id]
        
        # Check minimum images
        if len(session['images']) < API_CONFIG['min_images_for_reconstruction']:
            return jsonify({
                'success': False,
                'error': f"Need at least {API_CONFIG['min_images_for_reconstruction']} images"
            }), 400
        
        # Create reconstruction ID
        recon_id = f"recon_{int(time.time())}"
        
        # Adjust quality settings
        quality = data.get('quality', 'medium')
        config = COLMAP_CONFIG.copy()
        
        if quality == 'high':
            config['feature_extractor']['SiftExtraction.max_num_features'] = 16384
            config['dense']['max_image_size'] = 3200
        elif quality == 'low':
            config['feature_extractor']['SiftExtraction.max_num_features'] = 4096
            config['dense']['max_image_size'] = 1600
        
        # Initialize reconstruction status
        reconstruction_status[recon_id] = {
            'session_id': session_id,
            'status': 'queued',
            'progress': 0,
            'message': 'Initializing reconstruction...',
            'started_at': time.time(),
            'current_step': None,
            'errors': []
        }
        
        # Start reconstruction in background thread
        thread = threading.Thread(
            target=run_reconstruction,
            args=(recon_id, session, config)
        )
        thread.daemon = True
        thread.start()
        
        # Estimate time based on image count and quality
        base_time = len(session['images']) * 0.5  # 30 seconds per image
        quality_multiplier = {'high': 2.0, 'medium': 1.0, 'low': 0.5}
        estimated_time = base_time * quality_multiplier.get(quality, 1.0)
        
        logger.info(f"Started reconstruction {recon_id} for session {session_id}")
        
        return jsonify({
            'success': True,
            'reconstruction_id': recon_id,
            'message': 'Reconstruction started in background',
            'estimated_time_minutes': int(estimated_time / 60)
        })
    
    except Exception as e:
        logger.error(f"Failed to start reconstruction: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


def run_reconstruction(recon_id: str, session: Dict, config: Dict):
    """
    Run the actual reconstruction (in background thread)
    
    Args:
        recon_id: Reconstruction ID
        session: Session data
        config: COLMAP configuration
    """
    status = reconstruction_status[recon_id]
    
    try:
        session_folder = Path(session['folder'])
        output_folder = OUTPUT_DIR / recon_id
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Step 1: COLMAP reconstruction
        status['status'] = 'running'
        status['current_step'] = 'colmap'
        status['message'] = 'Running COLMAP reconstruction...'
        status['progress'] = 10
        
        colmap = COLMAPWrapper(
            workspace_path=str(session_folder),
            colmap_exe="colmap"  # Assumes COLMAP is in PATH
        )
        
        colmap_result = colmap.full_reconstruction(config)
        
        if not colmap_result['success']:
            raise Exception(f"COLMAP failed: {colmap_result['errors']}")
        
        status['progress'] = 60
        status['message'] = 'COLMAP reconstruction completed'
        
        # Step 2: Model processing
        status['current_step'] = 'processing'
        status['message'] = 'Processing 3D model...'
        status['progress'] = 70
        
        # Find the dense model
        dense_model = session_folder / "dense" / "fused.ply"
        if not dense_model.exists():
            # Fall back to sparse model
            sparse_model = session_folder / "sparse" / "0"
            logger.warning("No dense model found, using sparse")
        
        processor = ModelProcessor(str(dense_model))
        process_result = processor.process_full_pipeline(MODEL_CONFIG)
        
        if not process_result['success']:
            raise Exception(f"Processing failed: {process_result['errors']}")
        
        status['progress'] = 85
        
        # Step 3: Add crack markers
        if session['annotations']:
            status['message'] = 'Adding crack markers...'
            processor.add_crack_markers(session['annotations'])
        
        status['progress'] = 90
        
        # Step 4: Save final model
        status['message'] = 'Saving final model...'
        
        output_ply = output_folder / "model.ply"
        output_obj = output_folder / "model.obj"
        output_glb = output_folder / "model.glb"
        
        processor.save_mesh(str(output_ply), file_type='ply')
        processor.save_mesh(str(output_obj), file_type='obj')
        processor.save_mesh(str(output_glb), file_type='glb')
        
        status['progress'] = 95
        
        # Save metadata
        metadata = {
            'reconstruction_id': recon_id,
            'session_id': session['session_id'],
            'project_name': session['project_name'],
            'num_images': len(session['images']),
            'num_annotations': len(session['annotations']),
            'model_info': process_result['model_info'],
            'colmap_stats': colmap.get_reconstruction_stats(),
            'created_at': time.time()
        }
        
        with open(output_folder / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Success!
        status['status'] = 'completed'
        status['progress'] = 100
        status['message'] = '3D reconstruction completed successfully!'
        status['output_files'] = {
            'ply': str(output_ply),
            'obj': str(output_obj),
            'glb': str(output_glb),
            'metadata': str(output_folder / 'metadata.json')
        }
        status['completed_at'] = time.time()
        
        logger.info(f"Reconstruction {recon_id} completed successfully")
    
    except Exception as e:
        logger.error(f"Reconstruction {recon_id} failed: {e}")
        status['status'] = 'failed'
        status['message'] = f'Reconstruction failed: {str(e)}'
        status['errors'].append(str(e))


@reconstruction_bp.route('/status/<recon_id>', methods=['GET'])
def get_status(recon_id: str):
    """
    Get reconstruction status
    
    Returns:
        {
            "success": True,
            "status": "running" | "completed" | "failed",
            "progress": 75,
            "message": "Processing 3D model...",
            "output_files": {...} (if completed)
        }
    """
    if recon_id not in reconstruction_status:
        return jsonify({'success': False, 'error': 'Invalid reconstruction ID'}), 404
    
    status = reconstruction_status[recon_id]
    
    return jsonify({
        'success': True,
        **status
    })


@reconstruction_bp.route('/download/<recon_id>/<file_type>', methods=['GET'])
def download_model(recon_id: str, file_type: str):
    """
    Download reconstructed model
    
    Args:
        recon_id: Reconstruction ID
        file_type: 'ply', 'obj', or 'glb'
    
    Returns:
        File download
    """
    if recon_id not in reconstruction_status:
        return jsonify({'success': False, 'error': 'Invalid reconstruction ID'}), 404
    
    status = reconstruction_status[recon_id]
    
    if status['status'] != 'completed':
        return jsonify({'success': False, 'error': 'Reconstruction not completed'}), 400
    
    if file_type not in ['ply', 'obj', 'glb']:
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400
    
    file_path = status['output_files'].get(file_type)
    if not file_path or not Path(file_path).exists():
        return jsonify({'success': False, 'error': 'File not found'}), 404
    
    return send_file(file_path, as_attachment=True)


@reconstruction_bp.route('/sessions', methods=['GET'])
def list_sessions():
    """
    List all active sessions
    
    Returns:
        {
            "success": True,
            "sessions": [...]
        }
    """
    sessions_list = []
    
    for session_id, session in active_sessions.items():
        sessions_list.append({
            'session_id': session_id,
            'project_name': session['project_name'],
            'image_count': len(session['images']),
            'annotation_count': len(session['annotations']),
            'created_at': session['created_at'],
            'status': session['status']
        })
    
    return jsonify({
        'success': True,
        'sessions': sessions_list
    })


@reconstruction_bp.route('/session/<session_id>', methods=['DELETE'])
def delete_session(session_id: str):
    """
    Delete a session and its data
    
    Returns:
        {
            "success": True,
            "message": "Session deleted"
        }
    """
    if session_id not in active_sessions:
        return jsonify({'success': False, 'error': 'Invalid session ID'}), 404
    
    try:
        session = active_sessions[session_id]
        
        # Delete session folder
        import shutil
        shutil.rmtree(session['folder'], ignore_errors=True)
        
        # Remove from active sessions
        del active_sessions[session_id]
        
        logger.info(f"Deleted session {session_id}")
        
        return jsonify({
            'success': True,
            'message': 'Session deleted successfully'
        })
    
    except Exception as e:
        logger.error(f"Failed to delete session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# Export blueprint
__all__ = ['reconstruction_bp']
