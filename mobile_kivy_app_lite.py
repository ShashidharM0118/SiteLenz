"""
SiteLenz Mobile App - Lightweight Version
Uses server API for ML inference instead of local processing
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import requests
import base64
import json
from datetime import datetime
from io import BytesIO
from PIL import Image as PILImage

# Request Android permissions
try:
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.CAMERA,
        Permission.RECORD_AUDIO,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])
except ImportError:
    print("Not running on Android, skipping permissions")

# Try to import camera
try:
    from kivy.uix.camera import Camera
    CAMERA_AVAILABLE = True
except ImportError:
    print("Camera not available")
    CAMERA_AVAILABLE = False


class SiteLenzApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server_url = "http://10.211.181.132:5000"  # Update with your server IP
        self.monitoring = False
        self.session_logs = []
        
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='🏗️ SiteLenz Monitor',
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(title)
        
        # Server status
        self.status_label = Label(
            text='📡 Checking server...',
            size_hint=(1, 0.08),
            font_size='14sp',
            color=(0.4, 0.4, 0.4, 1)
        )
        layout.add_widget(self.status_label)
        
        # Camera preview
        if CAMERA_AVAILABLE:
            self.camera = Camera(
                resolution=(640, 480),
                play=True,
                size_hint=(1, 0.4)
            )
            layout.add_widget(self.camera)
        else:
            placeholder = Label(
                text='📷 Camera not available\n(Check permissions)',
                size_hint=(1, 0.4),
                font_size='16sp'
            )
            layout.add_widget(placeholder)
        
        # Control buttons
        btn_layout = BoxLayout(size_hint=(1, 0.12), spacing=5)
        
        self.start_btn = Button(
            text='🎙️ Start Monitoring',
            background_color=(0.2, 0.6, 0.9, 1),
            bold=True
        )
        self.start_btn.bind(on_press=self.start_monitoring)
        
        self.stop_btn = Button(
            text='⏹ Stop',
            background_color=(0.9, 0.3, 0.3, 1),
            disabled=True,
            bold=True
        )
        self.stop_btn.bind(on_press=self.stop_monitoring)
        
        btn_layout.add_widget(self.start_btn)
        btn_layout.add_widget(self.stop_btn)
        layout.add_widget(btn_layout)
        
        # Results area
        results_label = Label(
            text='📋 Results:',
            size_hint=(1, 0.05),
            font_size='16sp',
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(results_label)
        
        # Scrollable results
        scroll = ScrollView(size_hint=(1, 0.25))
        self.results_layout = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None,
            padding=5
        )
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll.add_widget(self.results_layout)
        layout.add_widget(scroll)
        
        # Check server status
        Clock.schedule_once(lambda dt: self.check_server(), 1)
        
        return layout
    
    def check_server(self):
        """Check if server is accessible"""
        try:
            response = requests.get(f"{self.server_url}/api/health", timeout=5)
            if response.status_code == 200:
                self.status_label.text = f"✅ Server connected: {self.server_url}"
                self.status_label.color = (0.2, 0.7, 0.2, 1)
            else:
                self.status_label.text = f"⚠️ Server error: {response.status_code}"
                self.status_label.color = (0.9, 0.5, 0.1, 1)
        except Exception as e:
            self.status_label.text = f"❌ Server offline: {str(e)[:40]}"
            self.status_label.color = (0.9, 0.2, 0.2, 1)
    
    def start_monitoring(self, instance):
        """Start monitoring mode"""
        try:
            # Start unified monitoring on server
            response = requests.post(f"{self.server_url}/api/unified/start", timeout=10)
            data = response.json()
            
            if data.get('success'):
                self.monitoring = True
                self.start_btn.disabled = True
                self.stop_btn.disabled = False
                self.status_label.text = "🎙️ Monitoring active - Speak to capture!"
                self.status_label.color = (0.2, 0.7, 0.2, 1)
                
                # Start checking for new logs
                Clock.schedule_interval(self.check_for_updates, 3)
            else:
                self.show_error(f"Failed to start: {data.get('error', 'Unknown error')}")
        except Exception as e:
            self.show_error(f"Connection error: {str(e)}")
    
    def stop_monitoring(self, instance):
        """Stop monitoring mode"""
        try:
            response = requests.post(f"{self.server_url}/api/unified/stop", timeout=10)
            data = response.json()
            
            if data.get('success'):
                self.monitoring = False
                self.start_btn.disabled = False
                self.stop_btn.disabled = True
                self.status_label.text = "⏹ Monitoring stopped"
                self.status_label.color = (0.4, 0.4, 0.4, 1)
                
                # Unschedule updates
                Clock.unschedule(self.check_for_updates)
                
                # Load final results
                self.load_unified_logs()
            else:
                self.show_error(f"Failed to stop: {data.get('error', 'Unknown error')}")
        except Exception as e:
            self.show_error(f"Connection error: {str(e)}")
    
    def check_for_updates(self, dt):
        """Check for new transcripts and trigger capture if needed"""
        if not self.monitoring:
            return
        
        try:
            # Check transcripts
            response = requests.get(f"{self.server_url}/api/audio/transcripts", timeout=5)
            data = response.json()
            
            if data.get('success'):
                transcripts = data.get('transcripts', [])
                
                # Check if there are new transcripts
                if len(transcripts) > len(self.session_logs):
                    new_transcripts = transcripts[len(self.session_logs):]
                    
                    for transcript in new_transcripts:
                        # Capture and classify
                        self.capture_and_send(transcript)
                        self.session_logs.append(transcript)
        except Exception as e:
            print(f"Update check error: {e}")
    
    def capture_and_send(self, transcript):
        """Capture camera frame and send to server"""
        if not CAMERA_AVAILABLE or not self.camera:
            return
        
        try:
            # Get camera texture
            texture = self.camera.texture
            if not texture:
                return
            
            # Convert to PIL Image
            size = texture.size
            pixels = texture.pixels
            pil_image = PILImage.frombytes('RGBA', size, bytes(pixels))
            pil_image = pil_image.convert('RGB')
            
            # Convert to base64
            buffered = BytesIO()
            pil_image.save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Send to server
            response = requests.post(
                f"{self.server_url}/api/unified/capture",
                json={
                    'image': f"data:image/jpeg;base64,{img_str}",
                    'transcript': transcript.get('text', ''),
                    'timestamp': transcript.get('timestamp', datetime.now().isoformat())
                },
                timeout=15
            )
            
            data = response.json()
            if data.get('success'):
                entry = data.get('entry', {})
                self.add_result(entry)
        except Exception as e:
            print(f"Capture error: {e}")
    
    def add_result(self, entry):
        """Add result to UI"""
        classification = entry.get('classification', {})
        transcript = entry.get('transcript', 'No audio')
        
        result_text = f"🎤 {transcript}\n📸 {classification.get('prediction', 'Unknown')} ({classification.get('confidence', 0):.1f}%)"
        
        result_label = Label(
            text=result_text,
            size_hint_y=None,
            height=60,
            font_size='12sp',
            color=(0.2, 0.2, 0.2, 1),
            halign='left',
            valign='top'
        )
        result_label.bind(size=result_label.setter('text_size'))
        
        self.results_layout.add_widget(result_label)
    
    def load_unified_logs(self):
        """Load all unified logs from server"""
        try:
            response = requests.get(f"{self.server_url}/api/unified/logs", timeout=10)
            data = response.json()
            
            if data.get('success'):
                logs = data.get('logs', [])
                self.results_layout.clear_widgets()
                
                for log in logs:
                    self.add_result(log)
        except Exception as e:
            print(f"Load logs error: {e}")
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.text = f"❌ {message}"
        self.status_label.color = (0.9, 0.2, 0.2, 1)
    
    def on_stop(self):
        """Clean up when app closes"""
        if self.monitoring:
            try:
                requests.post(f"{self.server_url}/api/unified/stop", timeout=5)
            except:
                pass
        return True


if __name__ == '__main__':
    SiteLenzApp().run()
