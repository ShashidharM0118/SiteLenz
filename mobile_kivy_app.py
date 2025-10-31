"""
SiteLenz Mobile App - Kivy Version for Android APK
This version can be packaged into an Android APK using Buildozer
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.audio import SoundLoader
from kivy.logger import Logger
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image as PILImage
import timm
import json
import os
from datetime import datetime
from threading import Thread
import queue

try:
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.CAMERA,
        Permission.RECORD_AUDIO,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
    ])
    ANDROID = True
except ImportError:
    ANDROID = False
    Logger.info("Not running on Android")


class CameraWidget(Image):
    """Camera widget for real-time video feed"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = None
        self.is_running = False
        
    def start(self):
        """Start camera capture"""
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)
        self.is_running = True
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        
    def stop(self):
        """Stop camera capture"""
        self.is_running = False
        Clock.unschedule(self.update)
        if self.capture:
            self.capture.release()
            self.capture = None
            
    def update(self, dt):
        """Update camera frame"""
        if not self.is_running or self.capture is None:
            return
            
        ret, frame = self.capture.read()
        if ret:
            # Convert to texture
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture
            
    def get_frame(self):
        """Get current frame for classification"""
        if self.capture is not None:
            ret, frame = self.capture.read()
            if ret:
                return frame
        return None


class WallClassifier:
    """Wall defect classifier using ViT model"""
    def __init__(self, model_path='models/vit_weights.pth'):
        self.device = torch.device('cpu')  # Use CPU on mobile
        self.classes = ['Algae', 'Major Crack', 'Minor Crack', 'Peeling', 'Plain', 'Spalling', 'Stain']
        self.model = None
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Load model in background
        Thread(target=self._load_model, args=(model_path,), daemon=True).start()
        
    def _load_model(self, model_path):
        """Load model in background thread"""
        try:
            Logger.info(f"Loading model from {model_path}")
            self.model = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=len(self.classes))
            
            if os.path.exists(model_path):
                state_dict = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                self.model.to(self.device)
                self.model.eval()
                Logger.info("Model loaded successfully")
            else:
                Logger.error(f"Model file not found: {model_path}")
        except Exception as e:
            Logger.error(f"Error loading model: {e}")
            
    def classify(self, frame):
        """Classify a frame"""
        if self.model is None:
            return None, []
            
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = PILImage.fromarray(rgb_frame)
            
            # Transform and classify
            input_tensor = self.transform(pil_image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                
            # Get top 3 predictions
            top3_prob, top3_idx = torch.topk(probabilities, 3)
            results = [(self.classes[idx], prob.item() * 100) for idx, prob in zip(top3_idx, top3_prob)]
            
            return results[0][0], results
        except Exception as e:
            Logger.error(f"Classification error: {e}")
            return None, []


class SiteLenzApp(App):
    """Main Kivy application"""
    
    def build(self):
        self.title = 'SiteLenz - Wall Inspector'
        
        # Initialize components
        self.classifier = WallClassifier()
        self.is_monitoring = False
        self.classification_results = []
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='🏗️ SiteLenz Mobile',
            size_hint=(1, 0.08),
            font_size='24sp',
            bold=True,
            color=(0.2, 0.6, 1, 1)
        )
        main_layout.add_widget(title)
        
        # Camera widget
        self.camera = CameraWidget(size_hint=(1, 0.5))
        main_layout.add_widget(self.camera)
        
        # Status label
        self.status_label = Label(
            text='Status: Ready',
            size_hint=(1, 0.06),
            font_size='16sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Classification result
        self.result_label = Label(
            text='Point camera at wall...',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1)
        )
        main_layout.add_widget(self.result_label)
        
        # Control buttons
        button_layout = BoxLayout(size_hint=(1, 0.12), spacing=10)
        
        self.start_btn = Button(
            text='▶️ Start',
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='18sp',
            bold=True
        )
        self.start_btn.bind(on_press=self.start_monitoring)
        button_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text='⏹️ Stop',
            background_color=(0.9, 0.3, 0.3, 1),
            font_size='18sp',
            bold=True,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_monitoring)
        button_layout.add_widget(self.stop_btn)
        
        main_layout.add_widget(button_layout)
        
        # Results log (scrollable)
        scroll = ScrollView(size_hint=(1, 0.24))
        self.log_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        scroll.add_widget(self.log_layout)
        main_layout.add_widget(scroll)
        
        return main_layout
        
    def start_monitoring(self, instance):
        """Start camera monitoring"""
        self.camera.start()
        self.is_monitoring = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.status_label.text = 'Status: Monitoring...'
        
        # Schedule classification every 5 seconds
        Clock.schedule_interval(self.classify_frame, 5.0)
        
    def stop_monitoring(self, instance):
        """Stop camera monitoring"""
        self.camera.stop()
        self.is_monitoring = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = 'Status: Stopped'
        
        Clock.unschedule(self.classify_frame)
        
    def classify_frame(self, dt):
        """Classify current frame"""
        if not self.is_monitoring:
            return
            
        frame = self.camera.get_frame()
        if frame is None:
            return
            
        # Classify in background thread
        Thread(target=self._classify_thread, args=(frame,), daemon=True).start()
        
    def _classify_thread(self, frame):
        """Background classification thread"""
        predicted_class, results = self.classifier.classify(frame)
        
        if predicted_class:
            # Update UI on main thread
            Clock.schedule_once(lambda dt: self._update_results(predicted_class, results), 0)
            
    def _update_results(self, predicted_class, results):
        """Update UI with classification results"""
        # Update main result
        confidence = results[0][1]
        self.result_label.text = f'🏗️ {predicted_class} ({confidence:.1f}%)'
        
        # Color code based on defect severity
        if predicted_class == 'Plain':
            self.result_label.color = (0.2, 0.8, 0.2, 1)  # Green
        elif 'Major' in predicted_class:
            self.result_label.color = (0.9, 0.1, 0.1, 1)  # Red
        elif 'Minor' in predicted_class or 'Crack' in predicted_class:
            self.result_label.color = (1, 0.6, 0, 1)  # Orange
        else:
            self.result_label.color = (0.9, 0.9, 0, 1)  # Yellow
            
        # Add to log
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = Label(
            text=f'[{timestamp}] {predicted_class} - {confidence:.1f}%',
            size_hint_y=None,
            height=40,
            font_size='14sp',
            color=(0.2, 0.2, 0.2, 1)
        )
        self.log_layout.add_widget(log_entry)
        
        # Save result
        self.classification_results.append({
            'timestamp': timestamp,
            'class': predicted_class,
            'confidence': confidence,
            'top3': results
        })
        
        # Auto-scroll to bottom
        if len(self.log_layout.children) > 20:
            self.log_layout.remove_widget(self.log_layout.children[-1])
            
    def on_stop(self):
        """Cleanup on app close"""
        self.camera.stop()
        
        # Save results
        if self.classification_results:
            output_dir = 'logs/classifications'
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(output_dir, f'mobile_session_{timestamp}.json')
            
            with open(output_file, 'w') as f:
                json.dump(self.classification_results, f, indent=2)
            
            Logger.info(f"Saved {len(self.classification_results)} classifications to {output_file}")


if __name__ == '__main__':
    SiteLenzApp().run()
