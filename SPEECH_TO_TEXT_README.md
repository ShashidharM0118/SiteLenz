# 🎤 Audio-to-Text Integration System

Complete speech-to-text integration for your existing audio recording system.

## 📋 Overview

This system adds **automatic speech-to-text transcription** to your existing audio recorder without requiring a database. All transcripts are stored in lightweight JSON files.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install SpeechRecognition PyAudio pydub
```

> **Windows Users**: If PyAudio fails, download the wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

### 2. Basic Usage

```python
from integration_helper import AudioTextIntegration

# Initialize
ati = AudioTextIntegration(session_id="exam_123")

# Transcribe audio file
text = ati.process_audio_file("recording.wav")
print(f"Transcription: {text}")
```

**That's it!** The transcript is automatically saved to `logs/transcripts/session_exam_123.json`

## 📦 Components

### 1. **speech_recognizer.py** - Core Transcription Engine

Converts audio files to text using:
- **Google Speech API** (online, free, fast)
- **Whisper** (offline, more accurate) - optional

```python
from speech_recognizer import SpeechRecognizer

recognizer = SpeechRecognizer(default_language="en-US")

# Simple transcription
text = recognizer.transcribe_file("audio.wav")

# With metadata
result = recognizer.transcribe_with_timestamp("audio.wav")
# Returns: {"timestamp": "...", "audio_file": "...", "text": "..."}

# Change language
recognizer.set_language("hi-IN")  # Hindi
recognizer.set_language("es-ES")  # Spanish

# Use Whisper (offline)
text = recognizer.transcribe_file("audio.wav", engine="whisper")
```

### 2. **transcript_manager.py** - Storage Manager

Manages transcripts using JSON files (no database required).

```python
from transcript_manager import TranscriptManager

manager = TranscriptManager(base_dir="logs/transcripts")

# Save transcript
manager.save_transcript(
    session_id="exam_123",
    timestamp="2025-11-07T14:30:05",
    audio_file="recording.wav",
    text="Transcribed text here"
)

# Get all transcripts
transcripts = manager.get_transcripts("exam_123")

# Search keywords
matches = manager.search_keywords(["important", "error"])

# Export
manager.export_to_txt("exam_123", "report.txt")
manager.export_to_json("exam_123", "report.json")

# Statistics
stats = manager.get_session_stats("exam_123")
print(f"Total words: {stats['total_words']}")
```

### 3. **integration_helper.py** - Easy Integration Wrapper

One-line integration with your existing audio recorder.

```python
from integration_helper import AudioTextIntegration

ati = AudioTextIntegration(session_id="exam_123")

# Process single file
text = ati.process_audio_file("recording.wav")

# Batch process folder
results = ati.process_audio_folder("logs/audio/", "*.wav")

# Get session transcripts
transcripts = ati.get_session_transcript()

# Search
matches = ati.search_transcripts(["keyword1", "keyword2"])

# Export
ati.export_session("txt", "report.txt")
ati.export_session("json", "report.json")

# Statistics
stats = ati.get_session_statistics()
```

## 🔌 Integration with Existing Audio Recorder

### Option 1: Hook into Recording Callback

```python
from integration_helper import AudioTextIntegration

class MyAudioRecorder:
    def __init__(self):
        self.audio_text = AudioTextIntegration(session_id="session_001")
    
    def on_recording_saved(self, audio_file_path):
        """Called when audio recording is saved"""
        # Automatically transcribe
        text = self.audio_text.process_audio_file(audio_file_path)
        
        if text:
            print(f"✓ Transcribed: {text[:50]}...")
            return text
        else:
            print("✗ Transcription failed")
            return None
    
    def get_all_transcripts(self):
        return self.audio_text.get_session_transcript()
    
    def export_final_report(self):
        self.audio_text.export_session("txt", "reports/final_report.txt")
```

### Option 2: Batch Process After Session

```python
from integration_helper import AudioTextIntegration

# After recording session ends
ati = AudioTextIntegration(session_id="exam_123")

# Process all recorded files at once
results = ati.process_audio_folder("logs/audio/", "*.wav")

# Export report
ati.export_session("txt", "reports/exam_123_transcript.txt")
```

## 📁 File Structure

```
your_project/
├── speech_recognizer.py         # Core transcription
├── transcript_manager.py         # Storage manager
├── integration_helper.py         # Easy wrapper
├── quick_start.py               # Usage examples
├── requirements_addition.txt     # Dependencies
│
├── logs/
│   ├── audio/                   # Your audio files
│   │   ├── recording_001.wav
│   │   └── recording_002.wav
│   │
│   └── transcripts/             # Transcripts (auto-created)
│       ├── session_exam_123.json
│       └── session_batch_001.json
│
└── exports/                     # Reports (auto-created)
    ├── exam_123_transcript.txt
    └── exam_123_transcript.json
```

## 📄 JSON Format

`logs/transcripts/session_exam_123.json`:

```json
{
  "session_id": "exam_123",
  "created_at": "2025-11-07T14:30:00",
  "transcripts": [
    {
      "timestamp": "2025-11-07T14:30:05",
      "audio_file": "E:/projects/logs/audio/recording_001.wav",
      "text": "This is the transcribed text",
      "language": "en-US",
      "engine": "google"
    }
  ]
}
```

## 🌍 Multi-Language Support

```python
ati = AudioTextIntegration()

# English (US)
ati.change_language("en-US")

# Hindi
ati.change_language("hi-IN")

# Spanish
ati.change_language("es-ES")

# French
ati.change_language("fr-FR")

# Then process audio files...
text = ati.process_audio_file("hindi_audio.wav")
```

## 🔍 Search & Filter

```python
# Search by keywords across all sessions
matches = ati.search_transcripts(["error", "warning", "problem"])

for match in matches:
    print(f"Session: {match['session_id']}")
    print(f"Time: {match['timestamp']}")
    print(f"Text: {match['text']}")
    print(f"Audio: {match['audio_file']}")
    print("---")

# Search within specific session
matches = ati.search_transcripts(["keyword"], session_id="exam_123")
```

## 📊 Statistics & Reports

```python
# Get session statistics
stats = ati.get_session_statistics("exam_123")

print(f"Total Transcripts: {stats['total_transcripts']}")
print(f"Total Words: {stats['total_words']}")
print(f"Total Characters: {stats['total_characters']}")
print(f"Avg Words/Transcript: {stats['average_words_per_transcript']}")

# Export to text file
ati.export_session("txt", "reports/exam_123.txt")

# Export to JSON
ati.export_session("json", "reports/exam_123.json")
```

## 🎯 Advanced Features

### Batch Processing

```python
# Process entire folder
results = ati.process_audio_folder("logs/audio/", "*.wav")

for file, text in results.items():
    if text:
        print(f"✓ {file}: {text[:50]}...")
    else:
        print(f"✗ {file}: Failed")
```

### Offline Transcription (Whisper)

```bash
# Install Whisper
pip install openai-whisper torch torchaudio
```

```python
# Use Whisper for better accuracy (offline)
text = ati.process_audio_file("audio.wav", engine="whisper")
```

### Error Handling

```python
text = ati.process_audio_file("audio.wav")

if text is None:
    print("Transcription failed - possible reasons:")
    print("• No speech detected")
    print("• Poor audio quality")
    print("• Network error (Google API)")
    print("• Unsupported format")
```

## 🛠️ Installation

### Method 1: Using requirements file

```bash
pip install -r requirements_addition.txt
```

### Method 2: Individual packages

```bash
pip install SpeechRecognition==3.10.0
pip install PyAudio==0.2.14
pip install pydub==0.25.1
```

### Method 3: With Whisper (offline support)

```bash
pip install SpeechRecognition PyAudio pydub
pip install openai-whisper torch torchaudio
```

## 🐛 Troubleshooting

### PyAudio Installation Fails (Windows)

1. Download wheel file: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Install: `pip install PyAudio-0.2.14-cp311-cp311-win_amd64.whl`

### No Speech Detected

- Check audio quality
- Ensure audio contains speech
- Try different microphone settings
- Use Whisper for better accuracy

### API Request Error

- Check internet connection (Google API requires online)
- Use Whisper for offline transcription
- Check firewall settings

## 📖 Complete Example

```python
from integration_helper import AudioTextIntegration

# Initialize with session ID
ati = AudioTextIntegration(session_id="exam_session_001")

# === During Recording ===
# Your audio recorder saves files, then:
audio_file = "logs/audio/question_01.wav"
text = ati.process_audio_file(audio_file)
print(f"Q1 Transcript: {text}")

audio_file = "logs/audio/question_02.wav"
text = ati.process_audio_file(audio_file)
print(f"Q2 Transcript: {text}")

# === After Session ===
# Get all transcripts
all_transcripts = ati.get_session_transcript()
print(f"\nTotal transcripts: {len(all_transcripts)}")

# Search for specific content
errors = ati.search_transcripts(["error", "problem"])
print(f"Found {len(errors)} error mentions")

# Get statistics
stats = ati.get_session_statistics()
print(f"Total words spoken: {stats['total_words']}")

# Export final report
ati.export_session("txt", "reports/exam_session_001.txt")
ati.export_session("json", "reports/exam_session_001.json")

print("✓ Session complete!")
```

## 🎓 Use Cases

- **Exam Proctoring**: Record and transcribe student responses
- **Interview Recording**: Automatic interview transcription
- **Meeting Notes**: Convert meeting audio to text
- **Podcast Transcription**: Batch convert podcast episodes
- **Voice Memos**: Transcribe voice notes automatically
- **Accessibility**: Add captions to audio content

## 📝 License

Free to use for your project.

## 🤝 Support

See `quick_start.py` for more examples and usage patterns.

---

**Made for easy integration with existing audio recording systems** 🎤✨
