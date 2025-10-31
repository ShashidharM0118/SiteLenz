"""
Camera-based Wall Classification Logger
Captures camera frames and classifies wall defects using ViT model
"""

import cv2
import torch
import timm
from torchvision import transforms
from PIL import Image
import threading
import queue
import json
import os
from datetime import datetime
from pathlib import Path
import logging
import time
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CameraClassifier:
    """
    Real-time camera capture and wall defect classification.
    Captures frames at specified intervals and classifies using ViT model.
    """
    
    def __init__(self, model_path="models/vit_weights.pth", 
                 frame_dir="logs/frames", 
                 classification_dir="logs/classifications",
                 capture_interval=5,
                 camera_id=0):
        """
        Initialize the camera classifier.
        
        Args:
            model_path: Path to ViT model weights
            frame_dir: Directory to save captured frames
            classification_dir: Directory to save classification logs
            capture_interval: Seconds between frame captures
            camera_id: Camera device ID (0 for default)
        """
        # Model configuration
        self.model_path = model_path
        self.num_classes = 7
        self.class_names = ['Algae', 'Major Crack', 'Minor Crack', 'Peeling', 
                           'Plain (Normal)', 'Spalling', 'Stain']
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        # Camera configuration
        self.camera_id = camera_id
        self.capture_interval = capture_interval
        
        # Directories
        self.frame_dir = Path(frame_dir)
        self.classification_dir = Path(classification_dir)
        self.frame_dir.mkdir(parents=True, exist_ok=True)
        self.classification_dir.mkdir(parents=True, exist_ok=True)
        
        # Session management
        self.session_id = None
        self.classifications = []
        
        # Recording state
        self.is_recording = False
        self.camera = None
        self.capture_thread = None
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        # Load model
        self.model = None
        self._load_model()
        
        logger.info("CameraClassifier initialized")
    
    def _load_model(self):
        """Load the ViT model."""
        try:
            logger.info(f"Loading model from {self.model_path}")
            self.model = timm.create_model('vit_base_patch16_224', 
                                          pretrained=False, 
                                          num_classes=self.num_classes)
            self.model.load_state_dict(torch.load(self.model_path, 
                                                  map_location=self.device))
            self.model = self.model.to(self.device)
            self.model.eval()
            logger.info(f"✅ Model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def _generate_session_id(self):
        """Generate unique session ID based on timestamp."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _get_frame_filename(self, timestamp):
        """Generate frame filename for a given timestamp."""
        return f"session_{self.session_id}_{timestamp}.jpg"
    
    def _get_classification_filename(self):
        """Generate classification filename for current session."""
        return f"session_{self.session_id}.json"
    
    def _save_frame(self, frame, timestamp):
        """Save camera frame to file."""
        try:
            filename = self._get_frame_filename(timestamp)
            filepath = self.frame_dir / filename
            cv2.imwrite(str(filepath), frame)
            logger.info(f"Saved frame: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving frame: {e}")
            return None
    
    def _save_classification(self):
        """Save classifications to JSON file."""
        try:
            with self.lock:
                filepath = self.classification_dir / self._get_classification_filename()
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'session_id': self.session_id,
                        'started_at': self.classifications[0]['timestamp'] if self.classifications else None,
                        'classifications': self.classifications
                    }, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved classification: {filepath.name}")
        except Exception as e:
            logger.error(f"Error saving classification: {e}")
    
    def _classify_frame(self, frame):
        """
        Classify a frame using the ViT model.
        
        Args:
            frame: OpenCV BGR image
            
        Returns:
            dict: Classification results with class, confidence, and probabilities
        """
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            
            # Preprocess
            img_tensor = self.transform(pil_image).unsqueeze(0).to(self.device)
            
            # Predict
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
            
            # Prepare results
            prediction = self.class_names[predicted.item()]
            confidence_score = confidence.item() * 100
            
            # Get all class probabilities
            all_probabilities = {}
            for i, prob in enumerate(probabilities[0]):
                all_probabilities[self.class_names[i]] = float(prob.item() * 100)
            
            return {
                'prediction': prediction,
                'confidence': round(confidence_score, 2),
                'probabilities': all_probabilities
            }
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return None
    
    def _capture_and_classify(self):
        """Capture frames and classify in background thread."""
        logger.info("Capture thread started")
        
        last_capture_time = time.time()
        
        while not self.stop_event.is_set():
            try:
                current_time = time.time()
                
                # Capture frame every N seconds
                if current_time - last_capture_time >= self.capture_interval:
                    ret, frame = self.camera.read()
                    
                    if ret:
                        logger.info("Captured frame, classifying...")
                        
                        # Generate timestamp
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                        
                        # Save frame
                        frame_filename = self._save_frame(frame, timestamp)
                        
                        # Classify
                        classification = self._classify_frame(frame)
                        
                        if classification and frame_filename:
                            classification_entry = {
                                'timestamp': datetime.now().isoformat(),
                                'frame_file': frame_filename,
                                'prediction': classification['prediction'],
                                'confidence': classification['confidence'],
                                'probabilities': classification['probabilities']
                            }
                            
                            with self.lock:
                                self.classifications.append(classification_entry)
                            
                            logger.info(f"Classified: {classification['prediction']} "
                                      f"({classification['confidence']:.2f}%)")
                            
                            # Save incrementally
                            self._save_classification()
                        
                        last_capture_time = current_time
                    else:
                        logger.warning("Failed to capture frame")
                
                # Small sleep to prevent busy waiting
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Capture thread error: {e}")
        
        logger.info("Capture thread stopped")
    
    def start_recording(self):
        """
        Start camera recording and classification session.
        
        Returns:
            str: Session ID for this recording session
        """
        if self.is_recording:
            logger.warning("Recording already in progress")
            return self.session_id
        
        # Initialize camera
        try:
            self.camera = cv2.VideoCapture(self.camera_id)
            if not self.camera.isOpened():
                raise Exception("Failed to open camera")
            
            # Set camera properties for better quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            logger.info("Camera opened successfully")
        except Exception as e:
            logger.error(f"Failed to open camera: {e}")
            raise
        
        # Initialize session
        self.session_id = self._generate_session_id()
        self.classifications = []
        self.is_recording = True
        self.stop_event.clear()
        
        # Start capture thread
        self.capture_thread = threading.Thread(target=self._capture_and_classify, daemon=True)
        self.capture_thread.start()
        
        logger.info(f"Recording started - Session ID: {self.session_id}")
        return self.session_id
    
    def stop_recording(self):
        """
        Stop camera recording and classification session.
        
        Returns:
            dict: Session summary with classification count and files
        """
        if not self.is_recording:
            logger.warning("No recording in progress")
            return None
        
        logger.info("Stopping recording...")
        
        # Signal thread to stop
        self.stop_event.set()
        
        # Wait for thread to finish
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=5)
        
        # Release camera
        if self.camera:
            self.camera.release()
            self.camera = None
        
        self.is_recording = False
        
        # Final save
        self._save_classification()
        
        summary = {
            'session_id': self.session_id,
            'classification_count': len(self.classifications),
            'classification_file': str(self.classification_dir / self._get_classification_filename()),
            'frame_dir': str(self.frame_dir)
        }
        
        logger.info(f"Recording stopped - {len(self.classifications)} classifications saved")
        return summary
    
    def get_classifications(self, session_id=None):
        """
        Get classifications for a session.
        
        Args:
            session_id: Session ID to retrieve (default: current session)
            
        Returns:
            list: List of classification dictionaries
        """
        if session_id is None:
            # Return current session classifications
            with self.lock:
                return self.classifications.copy()
        else:
            # Load from file
            try:
                filepath = self.classification_dir / f"session_{session_id}.json"
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('classifications', [])
            except FileNotFoundError:
                logger.error(f"Session not found: {session_id}")
                return []
            except Exception as e:
                logger.error(f"Error loading classifications: {e}")
                return []
    
    def search_defects(self, defect_types, session_id=None, min_confidence=0.0):
        """
        Search for specific defect types in classifications.
        
        Args:
            defect_types: List of defect types to search for
            session_id: Session ID to search (default: current session)
            min_confidence: Minimum confidence threshold (0-100)
            
        Returns:
            list: List of matching classification entries
        """
        classifications = self.get_classifications(session_id)
        matches = []
        
        for classification in classifications:
            prediction = classification['prediction']
            confidence = classification['confidence']
            
            if prediction in defect_types and confidence >= min_confidence:
                matches.append(classification)
        
        logger.info(f"Found {len(matches)} matches for defects: {defect_types}")
        return matches
    
    def get_session_info(self):
        """
        Get information about current recording session.
        
        Returns:
            dict: Session information
        """
        return {
            'session_id': self.session_id,
            'is_recording': self.is_recording,
            'classification_count': len(self.classifications),
            'device': str(self.device),
            'model_loaded': self.model is not None,
            'capture_interval': self.capture_interval
        }
    
    def list_sessions(self):
        """
        List all available recording sessions.
        
        Returns:
            list: List of session IDs
        """
        try:
            session_files = list(self.classification_dir.glob("session_*.json"))
            sessions = []
            for file in session_files:
                session_id = file.stem.replace("session_", "")
                sessions.append(session_id)
            return sorted(sessions, reverse=True)
        except Exception as e:
            logger.error(f"Error listing sessions: {e}")
            return []
    
    def get_latest_frame(self):
        """
        Get the latest captured frame.
        
        Returns:
            numpy.ndarray: Latest frame or None
        """
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None
