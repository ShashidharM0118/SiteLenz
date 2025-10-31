import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from audio_logger import AudioToTextLogger
from camera_classifier import CameraClassifier
import threading
import cv2
from PIL import Image, ImageTk
import numpy as np

class UnifiedMonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SiteLenz - Audio & Visual Monitoring System")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize loggers
        self.audio_logger = AudioToTextLogger(engine="google")
        self.camera_classifier = CameraClassifier(
            model_path="models/vit_weights.pth",
            capture_interval=5
        )
        
        # State variables
        self.is_audio_recording = False
        self.is_camera_recording = False
        self.camera_preview_running = False
        
        # UI Elements
        self.create_widgets()
        
        # Start camera preview
        self.start_camera_preview()
        
        # Update loops
        self.update_status()
        self.update_transcripts()
        self.update_classifications()
    
    def create_widgets(self):
        # ==================== HEADER ====================
        header_frame = tk.Frame(self.root, bg="#667eea", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="🏗️ SiteLenz Monitoring System", 
                        font=("Arial", 28, "bold"),
                        bg="#667eea", fg="white")
        title.pack(pady=25)
        
        # ==================== MAIN CONTAINER ====================
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # ==================== TOP SECTION: CAMERA & AUDIO CONTROLS ====================
        top_frame = tk.Frame(main_frame, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Camera Preview (Left)
        camera_frame = tk.LabelFrame(top_frame, text="📹 Camera Feed", 
                                     font=("Arial", 12, "bold"),
                                     bg="white", relief=tk.RIDGE, bd=2)
        camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.camera_label = tk.Label(camera_frame, bg="black")
        self.camera_label.pack(padx=10, pady=10)
        
        # Latest Classification
        self.latest_class_label = tk.Label(camera_frame, 
                                          text="Classification: Waiting...",
                                          font=("Arial", 11, "bold"),
                                          bg="white", fg="#333")
        self.latest_class_label.pack(pady=5)
        
        # Controls (Right)
        control_frame = tk.LabelFrame(top_frame, text="🎛️ Control Panel", 
                                      font=("Arial", 12, "bold"),
                                      bg="white", relief=tk.RIDGE, bd=2)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Audio Controls
        audio_section = tk.Frame(control_frame, bg="white")
        audio_section.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(audio_section, text="🎤 Audio Recording", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor=tk.W, pady=5)
        
        audio_btn_frame = tk.Frame(audio_section, bg="white")
        audio_btn_frame.pack(pady=5)
        
        self.audio_start_btn = tk.Button(audio_btn_frame, text="▶ Start Audio",
                                         command=self.start_audio_recording,
                                         bg="#4CAF50", fg="white",
                                         font=("Arial", 10, "bold"),
                                         padx=20, pady=8, cursor="hand2")
        self.audio_start_btn.grid(row=0, column=0, padx=5)
        
        self.audio_stop_btn = tk.Button(audio_btn_frame, text="⏹ Stop Audio",
                                        command=self.stop_audio_recording,
                                        bg="#f44336", fg="white",
                                        font=("Arial", 10, "bold"),
                                        padx=20, pady=8,
                                        state=tk.DISABLED, cursor="hand2")
        self.audio_stop_btn.grid(row=0, column=1, padx=5)
        
        # Camera Controls
        camera_section = tk.Frame(control_frame, bg="white")
        camera_section.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(camera_section, text="📸 Visual Monitoring", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor=tk.W, pady=5)
        
        camera_btn_frame = tk.Frame(camera_section, bg="white")
        camera_btn_frame.pack(pady=5)
        
        self.camera_start_btn = tk.Button(camera_btn_frame, text="▶ Start Camera",
                                          command=self.start_camera_recording,
                                          bg="#2196F3", fg="white",
                                          font=("Arial", 10, "bold"),
                                          padx=20, pady=8, cursor="hand2")
        self.camera_start_btn.grid(row=0, column=0, padx=5)
        
        self.camera_stop_btn = tk.Button(camera_btn_frame, text="⏹ Stop Camera",
                                         command=self.stop_camera_recording,
                                         bg="#FF9800", fg="white",
                                         font=("Arial", 10, "bold"),
                                         padx=20, pady=8,
                                         state=tk.DISABLED, cursor="hand2")
        self.camera_stop_btn.grid(row=0, column=1, padx=5)
        
        # Unified Control
        unified_section = tk.Frame(control_frame, bg="#e8f5e9", relief=tk.RIDGE, bd=2)
        unified_section.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(unified_section, text="⚡ Quick Actions", 
                font=("Arial", 11, "bold"), bg="#e8f5e9").pack(pady=5)
        
        self.start_all_btn = tk.Button(unified_section, text="🚀 Start Both",
                                       command=self.start_all,
                                       bg="#9C27B0", fg="white",
                                       font=("Arial", 11, "bold"),
                                       padx=30, pady=10, cursor="hand2")
        self.start_all_btn.pack(pady=5)
        
        self.stop_all_btn = tk.Button(unified_section, text="⏹ Stop Both",
                                      command=self.stop_all,
                                      bg="#795548", fg="white",
                                      font=("Arial", 11, "bold"),
                                      padx=30, pady=10,
                                      state=tk.DISABLED, cursor="hand2")
        self.stop_all_btn.pack(pady=5)
        
        # Status Display
        status_frame = tk.Frame(control_frame, bg="white")
        status_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.audio_status = tk.Label(status_frame, text="🎤 Audio: Idle",
                                     font=("Arial", 9), bg="white", fg="#666",
                                     anchor=tk.W)
        self.audio_status.pack(fill=tk.X, pady=2)
        
        self.camera_status = tk.Label(status_frame, text="📸 Camera: Idle",
                                      font=("Arial", 9), bg="white", fg="#666",
                                      anchor=tk.W)
        self.camera_status.pack(fill=tk.X, pady=2)
        
        self.audio_count_label = tk.Label(status_frame, text="Transcripts: 0",
                                          font=("Arial", 9), bg="white", fg="#666",
                                          anchor=tk.W)
        self.audio_count_label.pack(fill=tk.X, pady=2)
        
        self.camera_count_label = tk.Label(status_frame, text="Classifications: 0",
                                           font=("Arial", 9), bg="white", fg="#666",
                                           anchor=tk.W)
        self.camera_count_label.pack(fill=tk.X, pady=2)
        
        # ==================== BOTTOM SECTION: LOGS ====================
        bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Transcripts (Left)
        transcript_frame = tk.LabelFrame(bottom_frame, text="📝 Audio Transcripts", 
                                        font=("Arial", 11, "bold"),
                                        bg="white", relief=tk.RIDGE, bd=2)
        transcript_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.transcript_text = scrolledtext.ScrolledText(
            transcript_frame, width=45, height=20, 
            font=("Consolas", 9),
            bg="white", fg="#333", relief=tk.FLAT)
        self.transcript_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Classifications (Right)
        classification_frame = tk.LabelFrame(bottom_frame, text="🔍 Visual Classifications", 
                                            font=("Arial", 11, "bold"),
                                            bg="white", relief=tk.RIDGE, bd=2)
        classification_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.classification_text = scrolledtext.ScrolledText(
            classification_frame, width=45, height=20, 
            font=("Consolas", 9),
            bg="white", fg="#333", relief=tk.FLAT)
        self.classification_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initial messages
        self.transcript_text.insert(tk.END, 
            "No audio transcripts yet.\n"
            "Click 'Start Audio' to begin recording.\n\n")
        
        self.classification_text.insert(tk.END, 
            "No classifications yet.\n"
            "Click 'Start Camera' to begin monitoring.\n\n")
    
    def start_camera_preview(self):
        """Start camera preview in background."""
        self.camera_preview_running = True
        threading.Thread(target=self._update_camera_preview, daemon=True).start()
    
    def _update_camera_preview(self):
        """Update camera preview continuously."""
        while self.camera_preview_running:
            try:
                frame = self.camera_classifier.get_latest_frame()
                if frame is not None:
                    # Resize for display
                    frame = cv2.resize(frame, (480, 360))
                    # Convert BGR to RGB
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # Convert to PIL Image
                    img = Image.fromarray(rgb_frame)
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    # Update label
                    self.camera_label.configure(image=photo)
                    self.camera_label.image = photo
                else:
                    # Show placeholder when camera is off
                    placeholder = np.zeros((360, 480, 3), dtype=np.uint8)
                    cv2.putText(placeholder, "Camera Off", (150, 180),
                              cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 100, 100), 2)
                    img = Image.fromarray(placeholder)
                    photo = ImageTk.PhotoImage(img)
                    self.camera_label.configure(image=photo)
                    self.camera_label.image = photo
                
                self.root.after(100)  # Update every 100ms
            except Exception as e:
                pass
            
            threading.Event().wait(0.1)
    
    def start_audio_recording(self):
        """Start audio recording."""
        try:
            session_id = self.audio_logger.start_recording()
            self.is_audio_recording = True
            
            self.audio_start_btn.config(state=tk.DISABLED)
            self.audio_stop_btn.config(state=tk.NORMAL)
            self.update_control_buttons()
            
            self.transcript_text.delete(1.0, tk.END)
            self.transcript_text.insert(tk.END, f"🎤 Recording started - Session: {session_id}\n\n")
            
            messagebox.showinfo("Audio Started", 
                              f"Audio recording started!\nSession: {session_id}\n\nSpeak into your microphone.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start audio:\n{e}")
    
    def stop_audio_recording(self):
        """Stop audio recording."""
        try:
            summary = self.audio_logger.stop_recording()
            self.is_audio_recording = False
            
            self.audio_start_btn.config(state=tk.NORMAL)
            self.audio_stop_btn.config(state=tk.DISABLED)
            self.update_control_buttons()
            
            messagebox.showinfo("Audio Stopped", 
                              f"Audio recording stopped!\n\n"
                              f"Transcripts: {summary['transcript_count']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop audio:\n{e}")
    
    def start_camera_recording(self):
        """Start camera recording."""
        try:
            session_id = self.camera_classifier.start_recording()
            self.is_camera_recording = True
            
            self.camera_start_btn.config(state=tk.DISABLED)
            self.camera_stop_btn.config(state=tk.NORMAL)
            self.update_control_buttons()
            
            self.classification_text.delete(1.0, tk.END)
            self.classification_text.insert(tk.END, 
                f"📸 Camera recording started - Session: {session_id}\n\n")
            
            messagebox.showinfo("Camera Started", 
                              f"Camera monitoring started!\nSession: {session_id}\n\n"
                              f"Capturing frames every 5 seconds.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera:\n{e}")
    
    def stop_camera_recording(self):
        """Stop camera recording."""
        try:
            summary = self.camera_classifier.stop_recording()
            self.is_camera_recording = False
            
            self.camera_start_btn.config(state=tk.NORMAL)
            self.camera_stop_btn.config(state=tk.DISABLED)
            self.update_control_buttons()
            
            messagebox.showinfo("Camera Stopped", 
                              f"Camera monitoring stopped!\n\n"
                              f"Classifications: {summary['classification_count']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop camera:\n{e}")
    
    def start_all(self):
        """Start both audio and camera."""
        self.start_audio_recording()
        self.start_camera_recording()
    
    def stop_all(self):
        """Stop both audio and camera."""
        if self.is_audio_recording:
            self.stop_audio_recording()
        if self.is_camera_recording:
            self.stop_camera_recording()
    
    def update_control_buttons(self):
        """Update unified control buttons."""
        if self.is_audio_recording or self.is_camera_recording:
            self.start_all_btn.config(state=tk.DISABLED)
            self.stop_all_btn.config(state=tk.NORMAL)
        else:
            self.start_all_btn.config(state=tk.NORMAL)
            self.stop_all_btn.config(state=tk.DISABLED)
    
    def update_status(self):
        """Update status labels."""
        # Audio status
        if self.is_audio_recording:
            self.audio_status.config(text="🎤 Audio: 🔴 Recording...", fg="red")
        else:
            self.audio_status.config(text="🎤 Audio: Idle", fg="#666")
        
        # Camera status
        if self.is_camera_recording:
            self.camera_status.config(text="📸 Camera: 🔴 Recording...", fg="red")
        else:
            self.camera_status.config(text="📸 Camera: Idle", fg="#666")
        
        # Counts
        audio_info = self.audio_logger.get_session_info()
        camera_info = self.camera_classifier.get_session_info()
        
        self.audio_count_label.config(text=f"Transcripts: {audio_info['transcript_count']}")
        self.camera_count_label.config(text=f"Classifications: {camera_info['classification_count']}")
        
        # Schedule next update
        self.root.after(2000, self.update_status)
    
    def update_transcripts(self):
        """Update transcript display."""
        if self.is_audio_recording or self.audio_logger.get_transcripts():
            transcripts = self.audio_logger.get_transcripts()
            
            if transcripts:
                self.transcript_text.delete(1.0, tk.END)
                for i, t in enumerate(transcripts, 1):
                    timestamp = t['timestamp'].split('T')[1].split('.')[0]
                    self.transcript_text.insert(tk.END, f"[{i}] {timestamp}\n", "timestamp")
                    self.transcript_text.insert(tk.END, f"{t['text']}\n\n", "text")
                
                self.transcript_text.tag_config("timestamp", foreground="#667eea", font=("Arial", 9, "bold"))
                self.transcript_text.tag_config("text", foreground="#333")
                self.transcript_text.see(tk.END)
        
        if self.is_audio_recording:
            self.root.after(3000, self.update_transcripts)
        else:
            self.root.after(5000, self.update_transcripts)
    
    def update_classifications(self):
        """Update classification display."""
        if self.is_camera_recording or self.camera_classifier.get_classifications():
            classifications = self.camera_classifier.get_classifications()
            
            if classifications:
                self.classification_text.delete(1.0, tk.END)
                for i, c in enumerate(classifications, 1):
                    timestamp = c['timestamp'].split('T')[1].split('.')[0]
                    self.classification_text.insert(tk.END, f"[{i}] {timestamp}\n", "timestamp")
                    self.classification_text.insert(tk.END, 
                        f"🏗️ {c['prediction']} ({c['confidence']:.1f}%)\n", "prediction")
                    
                    # Show top 3 probabilities
                    sorted_probs = sorted(c['probabilities'].items(), 
                                         key=lambda x: x[1], reverse=True)[:3]
                    for cls, prob in sorted_probs:
                        self.classification_text.insert(tk.END, 
                            f"   • {cls}: {prob:.1f}%\n", "prob")
                    self.classification_text.insert(tk.END, "\n")
                
                # Update latest classification label
                if classifications:
                    latest = classifications[-1]
                    self.latest_class_label.config(
                        text=f"Latest: {latest['prediction']} ({latest['confidence']:.1f}%)",
                        fg=self._get_color_for_class(latest['prediction'])
                    )
                
                self.classification_text.tag_config("timestamp", foreground="#2196F3", font=("Arial", 9, "bold"))
                self.classification_text.tag_config("prediction", foreground="#333", font=("Arial", 10, "bold"))
                self.classification_text.tag_config("prob", foreground="#666", font=("Arial", 8))
                self.classification_text.see(tk.END)
        
        if self.is_camera_recording:
            self.root.after(3000, self.update_classifications)
        else:
            self.root.after(5000, self.update_classifications)
    
    def _get_color_for_class(self, class_name):
        """Get color coding for different classes."""
        colors = {
            'Plain (Normal)': '#4CAF50',  # Green
            'Minor Crack': '#FF9800',     # Orange
            'Major Crack': '#f44336',     # Red
            'Algae': '#00BCD4',           # Cyan
            'Stain': '#9C27B0',           # Purple
            'Peeling': '#FF5722',         # Deep Orange
            'Spalling': '#E91E63'         # Pink
        }
        return colors.get(class_name, '#333')
    
    def on_closing(self):
        """Handle window closing."""
        if self.is_audio_recording or self.is_camera_recording:
            if messagebox.askokcancel("Quit", 
                "Recording in progress. Stop and quit?"):
                self.stop_all()
                self.camera_preview_running = False
                self.root.destroy()
        else:
            self.camera_preview_running = False
            self.root.destroy()


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedMonitoringApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()
