"""
Quick Start Guide - Audio to Text Integration
"""

# ========================================
# STEP 1: INSTALL DEPENDENCIES
# ========================================
# pip install SpeechRecognition PyAudio pydub

# ========================================
# STEP 2: BASIC USAGE
# ========================================

from integration_helper import AudioTextIntegration

# Initialize with session ID
ati = AudioTextIntegration(session_id="my_session_001")

# Process a single audio file (automatically transcribes and saves)
text = ati.process_audio_file("path/to/recording.wav")
print(f"Transcription: {text}")

# That's it! The transcript is automatically saved to:
# logs/transcripts/session_my_session_001.json

# ========================================
# STEP 3: RETRIEVE TRANSCRIPTS
# ========================================

# Get all transcripts for current session
transcripts = ati.get_session_transcript()
for t in transcripts:
    print(f"{t['timestamp']}: {t['text']}")

# ========================================
# STEP 4: BATCH PROCESSING
# ========================================

# Process entire folder of audio files
results = ati.process_audio_folder("logs/audio/", "*.wav")
print(f"Processed {len(results)} files")

# ========================================
# STEP 5: SEARCH & EXPORT
# ========================================

# Search for keywords
matches = ati.search_transcripts(["important", "error"])
print(f"Found {len(matches)} matches")

# Export to text file
ati.export_session("txt", "reports/transcript.txt")

# Export to JSON
ati.export_session("json", "reports/transcript.json")

# ========================================
# INTEGRATION WITH EXISTING AUDIO RECORDER
# ========================================

"""
Example: Integrate with your existing audio recording system

# In your existing audio recorder code:

from integration_helper import AudioTextIntegration

class MyAudioRecorder:
    def __init__(self):
        self.audio_text = AudioTextIntegration(session_id="exam_123")
    
    def on_recording_saved(self, audio_file_path):
        # This gets called when your audio recorder saves a file
        
        # Automatically transcribe and save
        text = self.audio_text.process_audio_file(audio_file_path)
        
        if text:
            print(f"✓ Transcribed: {text[:50]}...")
        else:
            print("✗ Transcription failed")
    
    def get_all_transcripts(self):
        # Retrieve all transcripts for this session
        return self.audio_text.get_session_transcript()
    
    def export_report(self):
        # Export at end of session
        self.audio_text.export_session("txt", "reports/final_transcript.txt")

# Usage:
recorder = MyAudioRecorder()

# When user records audio, your system saves to:
audio_path = "logs/audio/recording_001.wav"

# Then call:
recorder.on_recording_saved(audio_path)

# At end of session:
all_transcripts = recorder.get_all_transcripts()
recorder.export_report()
"""

# ========================================
# ADVANCED FEATURES
# ========================================

# Change language
ati.change_language("hi-IN")  # Hindi
ati.change_language("es-ES")  # Spanish

# Use Whisper for offline transcription (more accurate)
text = ati.process_audio_file("audio.wav", engine="whisper")

# Get session statistics
stats = ati.get_session_statistics()
print(f"Total words: {stats['total_words']}")
print(f"Total transcripts: {stats['total_transcripts']}")

# Search across all sessions
matches = ati.search_transcripts(["keyword"], session_id=None)

# ========================================
# ERROR HANDLING
# ========================================

text = ati.process_audio_file("audio.wav")
if text is None:
    print("Transcription failed - possible reasons:")
    print("1. No speech detected in audio")
    print("2. Audio quality too low")
    print("3. Network error (for Google API)")
    print("4. Unsupported audio format")

# ========================================
# FILE STRUCTURE
# ========================================

"""
Your project structure will be:

your_project/
├── speech_recognizer.py       # Core transcription engine
├── transcript_manager.py       # Transcript storage manager
├── integration_helper.py       # Easy integration wrapper
├── quick_start.py             # This file (examples)
├── requirements_addition.txt   # Dependencies to install
│
├── logs/
│   ├── audio/                 # Your audio recordings
│   │   ├── recording_001.wav
│   │   └── recording_002.wav
│   │
│   └── transcripts/           # JSON transcripts (auto-created)
│       ├── session_exam_123.json
│       └── session_batch_001.json
│
└── exports/                   # Exported reports (auto-created)
    ├── exam_123_transcript.txt
    └── exam_123_transcript.json
"""

# ========================================
# JSON FILE FORMAT
# ========================================

"""
logs/transcripts/session_exam_123.json:

{
  "session_id": "exam_123",
  "created_at": "2025-11-07T14:30:00",
  "transcripts": [
    {
      "timestamp": "2025-11-07T14:30:05",
      "audio_file": "E:/projects/logs/audio/recording_001.wav",
      "text": "This is the transcribed text from the audio",
      "language": "en-US",
      "engine": "google"
    },
    {
      "timestamp": "2025-11-07T14:31:12",
      "audio_file": "E:/projects/logs/audio/recording_002.wav",
      "text": "Another transcribed audio recording",
      "language": "en-US",
      "engine": "google"
    }
  ]
}
"""

print("✓ Quick start guide loaded!")
print("Run this file to see examples: python quick_start.py")
