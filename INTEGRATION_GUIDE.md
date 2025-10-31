# Quick Integration Guide

## Simple Button Click Integration

### Option 1: Standalone Desktop App (Tkinter)

```python
import tkinter as tk
from tkinter import scrolledtext, messagebox
from audio_logger import AudioToTextLogger
import threading

class AudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")
        self.root.geometry("600x500")
        
        # Initialize logger
        self.logger = AudioToTextLogger(engine="google")
        self.is_recording = False
        
        # UI Elements
        self.create_widgets()
        
        # Update thread
        self.update_transcripts()
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="🎤 Audio Recorder", 
                        font=("Arial", 20, "bold"))
        title.pack(pady=10)
        
        # Buttons Frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Start Button
        self.start_btn = tk.Button(btn_frame, text="▶ Start Recording",
                                   command=self.start_recording,
                                   bg="#4CAF50", fg="white",
                                   font=("Arial", 12, "bold"),
                                   padx=20, pady=10)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        # Stop Button
        self.stop_btn = tk.Button(btn_frame, text="⏹ Stop Recording",
                                  command=self.stop_recording,
                                  bg="#f44336", fg="white",
                                  font=("Arial", 12, "bold"),
                                  padx=20, pady=10,
                                  state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Status Label
        self.status_label = tk.Label(self.root, text="Status: Idle",
                                     font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Transcripts Display
        tk.Label(self.root, text="Transcripts:", font=("Arial", 12, "bold")).pack()
        
        self.transcript_text = scrolledtext.ScrolledText(
            self.root, width=70, height=20, font=("Arial", 10))
        self.transcript_text.pack(padx=10, pady=10)
    
    def start_recording(self):
        """Start recording on button click."""
        try:
            self.logger.start_recording()
            self.is_recording = True
            
            # Update UI
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Status: 🔴 Recording...", fg="red")
            
            messagebox.showinfo("Recording", "Recording started! Speak into microphone.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {e}")
    
    def stop_recording(self):
        """Stop recording on button click."""
        try:
            summary = self.logger.stop_recording()
            self.is_recording = False
            
            # Update UI
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Idle", fg="black")
            
            # Show transcripts
            self.update_transcripts()
            
            messagebox.showinfo("Stopped", 
                              f"Recording stopped!\n\n"
                              f"Transcripts: {summary['transcript_count']}\n"
                              f"Session: {summary['session_id']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop recording: {e}")
    
    def update_transcripts(self):
        """Update transcript display."""
        if self.is_recording:
            transcripts = self.logger.get_transcripts()
            
            self.transcript_text.delete(1.0, tk.END)
            for i, t in enumerate(transcripts, 1):
                self.transcript_text.insert(tk.END, 
                    f"[{i}] {t['timestamp']}\n{t['text']}\n\n")
            
            # Auto-scroll to bottom
            self.transcript_text.see(tk.END)
        
        # Schedule next update
        self.root.after(3000, self.update_transcripts)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorderApp(root)
    root.mainloop()
```

**Save as:** `audio_desktop_app.py`

**Run with:** `python audio_desktop_app.py`

---

### Option 2: Web App Integration (Flask)

Already created! Just run:

```bash
python audio_web_api.py
```

Then open: `http://localhost:5000`

The HTML template (`templates/audio_interface.html`) has:
- Start Recording button
- Stop Recording button
- Real-time transcript display
- Keyword search functionality

---

### Option 3: PyQt5 Integration

```python
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                            QTextEdit, QVBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import QTimer
from audio_logger import AudioToTextLogger

class AudioWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = AudioToTextLogger()
        self.init_ui()
        
        # Timer for updating transcripts
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_transcripts)
        
    def init_ui(self):
        self.setWindowTitle('Audio Recorder')
        self.setGeometry(100, 100, 600, 500)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Status label
        self.status = QLabel('Status: Idle')
        layout.addWidget(self.status)
        
        # Start button
        self.start_btn = QPushButton('🎤 Start Recording')
        self.start_btn.clicked.connect(self.start_recording)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.start_btn)
        
        # Stop button
        self.stop_btn = QPushButton('⏹ Stop Recording')
        self.stop_btn.clicked.connect(self.stop_recording)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        layout.addWidget(self.stop_btn)
        
        # Transcripts display
        self.transcripts = QTextEdit()
        self.transcripts.setReadOnly(True)
        layout.addWidget(self.transcripts)
    
    def start_recording(self):
        """Start recording."""
        self.logger.start_recording()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status.setText('Status: 🔴 Recording...')
        self.timer.start(3000)  # Update every 3 seconds
    
    def stop_recording(self):
        """Stop recording."""
        summary = self.logger.stop_recording()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status.setText('Status: Idle')
        self.timer.stop()
        self.update_transcripts()
    
    def update_transcripts(self):
        """Update transcript display."""
        transcripts = self.logger.get_transcripts()
        text = ""
        for i, t in enumerate(transcripts, 1):
            text += f"[{i}] {t['timestamp']}\n{t['text']}\n\n"
        self.transcripts.setText(text)

# Run app
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = AudioWindow()
    window.show()
    sys.exit(app.exec_())
```

**Save as:** `audio_pyqt_app.py`

**Install PyQt5:** `pip install PyQt5`

**Run with:** `python audio_pyqt_app.py`

---

## Integration into Existing App

### Add to Your Existing Code

```python
from audio_logger import AudioToTextLogger

# Initialize once (e.g., in __init__ or setup)
self.audio_logger = AudioToTextLogger(
    audio_dir="logs/audio",
    transcript_dir="logs/transcripts",
    process_interval=5,
    engine="google"  # or "whisper" for offline
)

# In your "Start" button click handler:
def on_start_button_click(self):
    session_id = self.audio_logger.start_recording()
    print(f"Recording started: {session_id}")
    # Update UI to show recording status

# In your "Stop" button click handler:
def on_stop_button_click(self):
    summary = self.audio_logger.stop_recording()
    print(f"Recording stopped: {summary['transcript_count']} transcripts")
    # Update UI to show stopped status
    # Display transcripts

# Get transcripts anytime:
def show_transcripts(self):
    transcripts = self.audio_logger.get_transcripts()
    for t in transcripts:
        print(f"{t['timestamp']}: {t['text']}")

# Search for keywords:
def check_suspicious_words(self):
    keywords = ["password", "confidential", "secret"]
    matches = self.audio_logger.search_keywords(keywords)
    if matches:
        print(f"⚠️ Found {len(matches)} suspicious mentions!")
```

---

## Quick Test

Run the interactive example:

```bash
python audio_integration.py
```

Then select option 1 (Interactive mode) and type:
- `start` - Start recording
- (speak into microphone for 10-15 seconds)
- `stop` - Stop recording
- `view` - View transcripts

---

## Troubleshooting

### No microphone detected
- Check microphone is connected
- Grant microphone permissions
- Windows: Settings > Privacy > Microphone

### "Could not understand audio"
- Speak clearly and close to microphone
- Reduce background noise
- Try increasing `process_interval` to 10 seconds

### Import errors
```bash
pip install -r requirements_audio.txt
```

### Web interface not loading
```bash
# Check Flask is installed
pip install flask

# Run on different port
python audio_web_api.py
# Then open: http://localhost:5000
```

---

## Performance Tips

1. **Adjust process_interval:**
   - 3 seconds: Very responsive, but may miss words
   - 5 seconds: Good balance (recommended)
   - 10 seconds: Best accuracy, slower feedback

2. **Choose right engine:**
   - Google: Fast, accurate, requires internet
   - Whisper: Offline, good accuracy, slower

3. **For long recordings:**
   - Transcripts are saved incrementally
   - Safe to stop/restart anytime
   - Each session gets unique ID

4. **Memory management:**
   - Audio files are saved to disk immediately
   - Transcripts auto-saved every 5 seconds
   - Old sessions don't affect new recordings
