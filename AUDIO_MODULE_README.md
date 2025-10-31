# Audio-to-Text Conversion Module

Real-time audio recording and speech-to-text transcription module for desktop applications.

## Features

✅ **Continuous audio recording** from microphone in background thread  
✅ **Real-time speech-to-text** conversion (processes audio every 5 seconds)  
✅ **Timestamped transcripts** saved to JSON files  
✅ **Keyword search** functionality for flagging suspicious words  
✅ **Session-based logging** with unique session IDs  
✅ **Thread-safe** implementation (non-blocking)  
✅ **Online & Offline** transcription support  
✅ **JSON-based storage** (no database required)  

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements_audio.txt
```

### 2. System Dependencies

**Windows:**
- PyAudio is included in the wheel package (no additional setup needed)

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### 3. Optional: Offline Transcription (Whisper)

For offline transcription without internet:

```bash
pip install openai-whisper torch torchaudio
```

## Quick Start

### Basic Usage

```python
from audio_logger import AudioToTextLogger

# Initialize logger
logger = AudioToTextLogger(
    audio_dir="logs/audio",
    transcript_dir="logs/transcripts",
    process_interval=5,  # Process every 5 seconds
    engine="google"  # or "whisper" for offline
)

# Start recording
session_id = logger.start_recording()
print(f"Recording started - Session: {session_id}")

# ... recording happens in background ...

# Stop recording
summary = logger.stop_recording()
print(f"Saved {summary['transcript_count']} transcripts")

# Get transcripts
transcripts = logger.get_transcripts()
for t in transcripts:
    print(f"{t['timestamp']}: {t['text']}")
```

### Keyword Monitoring

```python
# Search for suspicious keywords
keywords = ["password", "confidential", "secret"]
matches = logger.search_keywords(keywords)

for match in matches:
    print(f"Found: {match['matched_keywords']}")
    print(f"Text: {match['text']}")
```

### Run Examples

```bash
python audio_integration.py
```

Choose from:
1. Interactive mode (keyboard control)
2. Timed recording (30 seconds)
3. Keyword monitoring

## API Reference

### AudioToTextLogger

#### Constructor

```python
AudioToTextLogger(
    audio_dir="logs/audio",           # Audio files directory
    transcript_dir="logs/transcripts", # Transcript files directory
    sample_rate=16000,                 # Audio sample rate (Hz)
    channels=1,                        # 1=mono, 2=stereo
    chunk_size=1024,                   # Audio chunk size
    process_interval=5,                # Process audio every N seconds
    engine="google",                   # "google" or "whisper"
    whisper_model="base"               # Whisper model size
)
```

#### Methods

**start_recording()**
- Starts recording session
- Returns: `session_id` (str)

**stop_recording()**
- Stops recording session
- Returns: Summary dict with session info

**get_transcripts(session_id=None)**
- Get transcripts for session
- Args: `session_id` (optional, defaults to current)
- Returns: List of transcript dicts

**search_keywords(keywords, session_id=None, case_sensitive=False)**
- Search for keywords in transcripts
- Args:
  - `keywords`: List of keywords to search
  - `session_id`: Session to search (optional)
  - `case_sensitive`: Case-sensitive search (default: False)
- Returns: List of matching transcript entries

**get_session_info()**
- Get current session information
- Returns: Dict with session details

**list_sessions()**
- List all available sessions
- Returns: List of session IDs

## File Structure

```
logs/
├── audio/
│   ├── session_20251031_143000_001.wav
│   ├── session_20251031_143000_002.wav
│   └── ...
└── transcripts/
    └── session_20251031_143000.json
```

### Transcript JSON Format

```json
{
  "session_id": "20251031_143000",
  "started_at": "2025-10-31T14:30:00.123456",
  "transcripts": [
    {
      "timestamp": "2025-10-31T14:30:05.123456",
      "text": "Hello, this is a test recording",
      "audio_file": "session_20251031_143000_001.wav"
    }
  ]
}
```

## Integration with Desktop App

### Example: Flask Web App

```python
from flask import Flask, jsonify, request
from audio_logger import AudioToTextLogger

app = Flask(__name__)
logger = AudioToTextLogger()

@app.route('/api/audio/start', methods=['POST'])
def start_recording():
    session_id = logger.start_recording()
    return jsonify({'session_id': session_id, 'status': 'recording'})

@app.route('/api/audio/stop', methods=['POST'])
def stop_recording():
    summary = logger.stop_recording()
    return jsonify(summary)

@app.route('/api/audio/transcripts', methods=['GET'])
def get_transcripts():
    transcripts = logger.get_transcripts()
    return jsonify({'transcripts': transcripts})

@app.route('/api/audio/search', methods=['POST'])
def search():
    keywords = request.json.get('keywords', [])
    matches = logger.search_keywords(keywords)
    return jsonify({'matches': matches})
```

### Example: PyQt Desktop App

```python
from PyQt5.QtCore import QThread, pyqtSignal
from audio_logger import AudioToTextLogger

class AudioRecorderThread(QThread):
    transcript_ready = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.logger = AudioToTextLogger()
    
    def start_recording(self):
        self.session_id = self.logger.start_recording()
    
    def stop_recording(self):
        summary = self.logger.stop_recording()
        transcripts = self.logger.get_transcripts()
        for t in transcripts:
            self.transcript_ready.emit(t)
        return summary

# In your main window:
# self.audio_thread = AudioRecorderThread()
# self.audio_thread.transcript_ready.connect(self.on_transcript)
# self.start_button.clicked.connect(self.audio_thread.start_recording)
```

## Configuration

### Audio Settings

- **Sample Rate**: 16000 Hz (recommended for speech)
- **Channels**: 1 (mono, recommended for speech)
- **Chunk Size**: 1024 (balance between latency and performance)
- **Process Interval**: 5 seconds (balance between real-time and accuracy)

### Transcription Engines

**Google Speech API (Online)**
- Pros: High accuracy, no setup
- Cons: Requires internet, API limits
- Best for: Production apps with internet

**Whisper (Offline)**
- Pros: Offline, unlimited usage, good accuracy
- Cons: Slower, requires GPU for best performance
- Best for: Privacy-sensitive apps, no internet

## Troubleshooting

### "No module named 'pyaudio'"

**Windows:**
```bash
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### "OSError: No Default Input Device Available"

- Check microphone is connected
- Grant microphone permissions to Python
- Windows: Settings > Privacy > Microphone

### "Could not understand audio"

- Speak clearly and close to microphone
- Reduce background noise
- Check microphone volume settings
- Try increasing `process_interval` for longer audio chunks

### "Recognition service error"

- Check internet connection (for Google API)
- Try switching to Whisper for offline mode
- Check firewall settings

## Performance Tips

1. **Use appropriate process_interval**: 
   - 3-5 seconds for real-time feedback
   - 10+ seconds for better accuracy

2. **Choose right engine**:
   - Google: Fast, accurate, requires internet
   - Whisper: Slower, offline, privacy-focused

3. **Optimize Whisper model size**:
   - `tiny`: Fastest, lowest accuracy
   - `base`: Good balance (recommended)
   - `small/medium/large`: Higher accuracy, slower

4. **Thread safety**: All methods are thread-safe and can be called from any thread

## Security Considerations

- Audio files contain sensitive information
- Transcripts may contain PII (Personally Identifiable Information)
- Add `logs/audio/` and `logs/transcripts/` to `.gitignore`
- Implement access controls for production
- Consider encryption for sensitive recordings
- Regular cleanup of old sessions

## License

This module is part of the SiteLenz project. Refer to the main project license.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the examples in `audio_integration.py`
3. Check system audio permissions
4. Verify all dependencies are installed
