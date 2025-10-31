# 🏗️ SiteLenz - Unified Monitoring System

**Real-time Audio & Visual Monitoring for Building Inspection**

Combines audio-to-text transcription with AI-powered wall defect classification using Vision Transformer (ViT).

---

## ✨ Features

### 🎤 Audio Monitoring
- ✅ Continuous audio recording from microphone
- ✅ Real-time speech-to-text conversion (every 5 seconds)
- ✅ Timestamped transcripts saved to JSON
- ✅ Keyword search for suspicious words
- ✅ Session-based logging

### 📸 Visual Monitoring
- ✅ Real-time camera feed with preview
- ✅ AI-powered wall defect classification (every 5 seconds)
- ✅ 7 defect classes: Algae, Major Crack, Minor Crack, Peeling, Plain, Spalling, Stain
- ✅ Confidence scores and probability distributions
- ✅ Timestamped frame capture with classifications
- ✅ Vision Transformer (ViT) model for high accuracy

### 🎛️ Unified Control
- ✅ Start/Stop both systems independently or together
- ✅ Real-time status monitoring
- ✅ Side-by-side transcript and classification logs
- ✅ Live camera preview
- ✅ Color-coded defect detection

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_unified.txt
```

**Required packages:**
- PyAudio, SpeechRecognition (Audio)
- OpenCV, Torch, Torchvision, TIMM (Vision)
- Pillow, NumPy (Image processing)
- Tkinter (Built-in GUI)

### 2. Verify Setup

```bash
python test_camera_module.py
python test_audio_module.py
```

Both should show 5/5 tests passed ✅

### 3. Run the Application

```bash
python unified_monitoring_app.py
```

---

## 🎯 How to Use

### Starting Both Systems

1. **Launch the app**: `python unified_monitoring_app.py`
2. **Click "🚀 Start Both"** to begin audio and camera monitoring
3. **Speak into microphone** - transcripts appear in left panel
4. **Point camera at wall** - classifications appear in right panel
5. **Click "⏹ Stop Both"** when done

### Independent Control

- **Audio Only**: Click "▶ Start Audio" → Speak → Click "⏹ Stop Audio"
- **Camera Only**: Click "▶ Start Camera" → Point at wall → Click "⏹ Stop Camera"

### What You'll See

**Left Panel (Audio Transcripts):**
```
[1] 14:30:05
"Inspecting the north wall for cracks"

[2] 14:30:10
"Found major damage near the window"
```

**Right Panel (Visual Classifications):**
```
[1] 14:30:06
🏗️ Major Crack (92.3%)
   • Major Crack: 92.3%
   • Minor Crack: 4.2%
   • Plain: 2.1%

[2] 14:30:11
🏗️ Peeling (87.6%)
   • Peeling: 87.6%
   • Stain: 8.3%
   • Plain: 3.1%
```

---

## 📊 Wall Defect Classes

The ViT model classifies walls into 7 categories:

| Class | Description | Color Code |
|-------|-------------|------------|
| **Plain (Normal)** | No defects detected | 🟢 Green |
| **Minor Crack** | Small surface cracks | 🟠 Orange |
| **Major Crack** | Severe structural cracks | 🔴 Red |
| **Algae** | Biological growth | 🔵 Cyan |
| **Stain** | Discoloration or staining | 🟣 Purple |
| **Peeling** | Paint/surface peeling | 🟠 Deep Orange |
| **Spalling** | Concrete surface damage | 🔴 Pink |

---

## 📁 Output Files

### Audio Logs
```
logs/audio/
├── session_20251031_143000_001.wav
├── session_20251031_143000_002.wav
└── ...

logs/transcripts/
└── session_20251031_143000.json
```

**Transcript JSON format:**
```json
{
  "session_id": "20251031_143000",
  "started_at": "2025-10-31T14:30:00",
  "transcripts": [
    {
      "timestamp": "2025-10-31T14:30:05",
      "text": "Inspecting the north wall",
      "audio_file": "session_20251031_143000_001.wav"
    }
  ]
}
```

### Camera Logs
```
logs/frames/
├── session_20251031_143000_001.jpg
├── session_20251031_143000_002.jpg
└── ...

logs/classifications/
└── session_20251031_143000.json
```

**Classification JSON format:**
```json
{
  "session_id": "20251031_143000",
  "started_at": "2025-10-31T14:30:00",
  "classifications": [
    {
      "timestamp": "2025-10-31T14:30:06",
      "frame_file": "session_20251031_143000_001.jpg",
      "prediction": "Major Crack",
      "confidence": 92.3,
      "probabilities": {
        "Major Crack": 92.3,
        "Minor Crack": 4.2,
        "Plain (Normal)": 2.1,
        ...
      }
    }
  ]
}
```

---

## 🔧 Configuration

### Audio Settings

Edit `audio_logger.py` or pass parameters:

```python
AudioToTextLogger(
    audio_dir="logs/audio",
    transcript_dir="logs/transcripts",
    sample_rate=16000,        # 16kHz for speech
    channels=1,               # Mono
    chunk_size=1024,          # Buffer size
    process_interval=5,       # Process every 5 seconds
    engine="google"           # "google" or "whisper"
)
```

### Camera Settings

Edit `camera_classifier.py` or pass parameters:

```python
CameraClassifier(
    model_path="models/vit_weights.pth",
    frame_dir="logs/frames",
    classification_dir="logs/classifications",
    capture_interval=5,       # Capture every 5 seconds
    camera_id=0               # Camera device ID
)
```

---

## 🧠 Model Information

### Vision Transformer (ViT)

- **Architecture**: ViT-Base-Patch16-224
- **Input Size**: 224×224 RGB images
- **Patch Size**: 16×16 pixels
- **Model Size**: ~327 MB
- **Classes**: 7 building defect types
- **Training**: 200 epochs on building defect dataset
- **Device**: Runs on CPU or CUDA GPU

**Preprocessing:**
```python
transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], 
                        [0.229, 0.224, 0.225])
])
```

---

## 💡 Use Cases

### 1. Building Inspection
- Record verbal notes while inspecting
- Camera automatically classifies defects
- Synchronized audio and visual logs

### 2. Quality Assurance
- Document findings with timestamps
- Visual evidence with AI classification
- Search transcripts for specific issues

### 3. Safety Monitoring
- Flag critical defects (Major Cracks, Spalling)
- Audio alerts for dangerous conditions
- Complete inspection audit trail

### 4. Research & Analysis
- Collect training data for ML models
- Analyze defect patterns over time
- Correlate audio descriptions with visual data

---

## 🛠️ Troubleshooting

### Camera Issues

**"Failed to open camera"**
- Check camera is connected
- Close other apps using camera (Zoom, Teams, etc.)
- Try different camera_id (0, 1, 2...)
- Grant camera permissions (Windows Settings > Privacy > Camera)

**"Failed to read frame"**
- Camera might be in use
- Check camera drivers are installed
- Try unplugging and reconnecting camera

### Model Issues

**"Model file not found"**
- Ensure `vit_weights.pth` is in `models/` directory
- File should be ~327 MB
- Download from your trained model location

**"Out of memory"**
- Model runs on CPU by default
- Close other heavy applications
- Reduce capture_interval to save resources

### Audio Issues

**"No microphone detected"**
- Check microphone is connected
- Grant microphone permissions
- Windows: Settings > Privacy > Microphone

**"Could not understand audio"**
- Speak clearly and close to microphone
- Reduce background noise
- Try increasing process_interval

---

## 📈 Performance Tips

### For Better Accuracy

**Audio:**
- Speak clearly, 1-2 feet from microphone
- Reduce background noise
- Use process_interval=10 for longer context

**Camera:**
- Ensure good lighting
- Keep camera steady
- Position wall clearly in frame
- Avoid shadows and glare

### For Better Performance

**Resource Usage:**
- Close unnecessary applications
- Use CPU if no GPU available
- Increase capture_interval to reduce load
- Run one system at a time if needed

**GPU Acceleration:**
```bash
# Install PyTorch with CUDA support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

## 🔐 Security & Privacy

### Data Protection

- Audio recordings contain conversations
- Camera frames may contain sensitive areas
- Transcripts may include personal information
- All files stored locally (not uploaded)

### Best Practices

1. **Review recordings** before sharing
2. **Delete sensitive sessions** after use
3. **Encrypt logs** for production environments
4. **Restrict access** to logs directories
5. **Regular cleanup** of old sessions

### Compliance

- GDPR: Obtain consent before recording
- HIPAA: Encrypt if used in healthcare
- Local laws: Check recording regulations
- Privacy: Inform people being recorded

---

## 📚 API Reference

### AudioToTextLogger

```python
from audio_logger import AudioToTextLogger

logger = AudioToTextLogger()

# Start recording
session_id = logger.start_recording()

# Stop recording
summary = logger.stop_recording()

# Get transcripts
transcripts = logger.get_transcripts()

# Search keywords
matches = logger.search_keywords(['crack', 'damage'])
```

### CameraClassifier

```python
from camera_classifier import CameraClassifier

classifier = CameraClassifier(model_path="models/vit_weights.pth")

# Start recording
session_id = classifier.start_recording()

# Stop recording
summary = classifier.stop_recording()

# Get classifications
classifications = classifier.get_classifications()

# Search defects
matches = classifier.search_defects(['Major Crack', 'Spalling'])
```

---

## 🧪 Testing

### Run All Tests

```bash
# Test audio module
python test_audio_module.py

# Test camera module
python test_camera_module.py
```

### Expected Output

```
✅ PASS - Dependencies Test
✅ PASS - Directory Structure Test
✅ PASS - Camera Access Test (or Audio Devices Test)
✅ PASS - Model Loading Test (or Logger Initialization Test)
✅ PASS - CameraClassifier Test (or Session Management Test)

Results: 5/5 tests passed
```

---

## 📦 Project Structure

```
major_project/
├── unified_monitoring_app.py    # Main application (RUN THIS!)
├── audio_logger.py              # Audio module
├── camera_classifier.py         # Camera module
├── test_audio_module.py         # Audio tests
├── test_camera_module.py        # Camera tests
├── requirements_unified.txt     # All dependencies
├── models/
│   └── vit_weights.pth         # ViT model (327 MB)
├── logs/
│   ├── audio/                  # Audio recordings (.wav)
│   ├── transcripts/            # Audio transcripts (.json)
│   ├── frames/                 # Camera frames (.jpg)
│   └── classifications/        # Visual classifications (.json)
└── templates/
    └── audio_interface.html    # Web interface (optional)
```

---

## 🚀 Deployment

### Desktop Application

Already ready! Just run:
```bash
python unified_monitoring_app.py
```

### Standalone Executables

Create .exe with PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed unified_monitoring_app.py
```

### Web Service

Use Flask API:
```bash
python audio_web_api.py  # For audio only
# Create similar API for camera if needed
```

---

## 🤝 Contributing

This is part of the SiteLenz project for building defect detection.

**Improvements to consider:**
- Add more defect classes
- Improve model accuracy with more training data
- Add real-time alerts for critical defects
- Export reports in PDF format
- Database integration for large-scale deployments

---

## 📄 License

Part of SiteLenz project. Refer to main project license.

---

## 🆘 Support

**Issues?**
1. Check troubleshooting section above
2. Run test scripts to diagnose
3. Verify all dependencies installed
4. Check camera/microphone permissions

**Common Commands:**
```bash
# Full system test
python test_audio_module.py && python test_camera_module.py

# Reinstall dependencies
pip install -r requirements_unified.txt --force-reinstall

# Check device status
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
python -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
```

---

## 🎉 You're Ready!

Everything is set up and tested. Launch the application:

```bash
python unified_monitoring_app.py
```

1. Click **"🚀 Start Both"**
2. Speak into microphone
3. Point camera at wall
4. Watch real-time transcription and classification
5. Click **"⏹ Stop Both"** when done

**Enjoy your unified monitoring system!** 🏗️🎤📸
