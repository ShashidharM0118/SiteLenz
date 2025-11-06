"""
Speech Recognizer Module
Converts audio files to text using Google Speech API and optional Whisper
"""

import speech_recognition as sr
from pathlib import Path
from typing import Optional, Dict, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """
    Handles audio-to-text transcription using multiple engines
    """
    
    def __init__(self, default_language: str = "en-US"):
        """
        Initialize the speech recognizer
        
        Args:
            default_language: Language code for transcription (e.g., 'en-US', 'hi-IN')
        """
        self.recognizer = sr.Recognizer()
        self.language = default_language
        self.whisper_available = False
        
        # Try to import whisper for offline transcription
        try:
            import whisper
            self.whisper_model = None
            self.whisper_available = True
            logger.info("Whisper support available")
        except ImportError:
            logger.info("Whisper not available. Install with: pip install openai-whisper")
    
    def set_language(self, language_code: str):
        """
        Set the language for transcription
        
        Args:
            language_code: Language code (e.g., 'en-US', 'hi-IN', 'es-ES')
        """
        self.language = language_code
        logger.info(f"Language set to: {language_code}")
    
    def transcribe_file(self, audio_file_path: str, engine: str = "google") -> Optional[str]:
        """
        Transcribe an audio file to text
        
        Args:
            audio_file_path: Path to the audio file (WAV format recommended)
            engine: Transcription engine ('google' or 'whisper')
        
        Returns:
            Transcribed text string, or None if transcription fails
        """
        audio_path = Path(audio_file_path)
        
        if not audio_path.exists():
            logger.error(f"Audio file not found: {audio_file_path}")
            return None
        
        try:
            if engine == "whisper" and self.whisper_available:
                return self._transcribe_with_whisper(audio_file_path)
            else:
                return self._transcribe_with_google(audio_file_path)
        
        except sr.UnknownValueError:
            logger.warning(f"No speech detected in: {audio_file_path}")
            return None
        
        except sr.RequestError as e:
            logger.error(f"API request error: {e}")
            return None
        
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return None
    
    def _transcribe_with_google(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe using Google Speech Recognition API (online, free)
        
        Args:
            audio_file_path: Path to audio file
        
        Returns:
            Transcribed text or None
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.record(source)
            
            # Perform recognition
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            logger.info(f"Successfully transcribed: {audio_file_path}")
            return text
        
        except Exception as e:
            logger.error(f"Google transcription error: {e}")
            raise
    
    def _transcribe_with_whisper(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe using OpenAI Whisper (offline, accurate)
        
        Args:
            audio_file_path: Path to audio file
        
        Returns:
            Transcribed text or None
        """
        try:
            import whisper
            
            # Load model if not already loaded (lazy loading)
            if self.whisper_model is None:
                logger.info("Loading Whisper model (this may take a moment)...")
                self.whisper_model = whisper.load_model("base")
            
            # Transcribe
            result = self.whisper_model.transcribe(audio_file_path, language=self.language.split('-')[0])
            text = result["text"].strip()
            
            logger.info(f"Successfully transcribed with Whisper: {audio_file_path}")
            return text
        
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")
            raise
    
    def transcribe_with_timestamp(self, audio_file_path: str, engine: str = "google") -> Optional[Dict]:
        """
        Transcribe audio file and return result with metadata
        
        Args:
            audio_file_path: Path to the audio file
            engine: Transcription engine ('google' or 'whisper')
        
        Returns:
            Dictionary with timestamp, audio file, and transcribed text
            Example: {
                "timestamp": "2025-11-07T14:30:05",
                "audio_file": "path/to/audio.wav",
                "text": "transcribed text here",
                "language": "en-US",
                "engine": "google"
            }
        """
        text = self.transcribe_file(audio_file_path, engine)
        
        if text is None:
            return None
        
        return {
            "timestamp": datetime.now().isoformat(),
            "audio_file": str(Path(audio_file_path).absolute()),
            "text": text,
            "language": self.language,
            "engine": engine
        }
    
    def batch_transcribe(self, audio_files: List[str], engine: str = "google") -> List[Dict]:
        """
        Transcribe multiple audio files
        
        Args:
            audio_files: List of audio file paths
            engine: Transcription engine to use
        
        Returns:
            List of transcription dictionaries
        """
        results = []
        total = len(audio_files)
        
        logger.info(f"Starting batch transcription of {total} files...")
        
        for idx, audio_file in enumerate(audio_files, 1):
            logger.info(f"Processing file {idx}/{total}: {audio_file}")
            result = self.transcribe_with_timestamp(audio_file, engine)
            
            if result:
                results.append(result)
            else:
                logger.warning(f"Skipped file (no transcription): {audio_file}")
        
        logger.info(f"Batch transcription complete: {len(results)}/{total} successful")
        return results


# Example usage
if __name__ == "__main__":
    # Initialize recognizer
    recognizer = SpeechRecognizer(default_language="en-US")
    
    # Transcribe a single file
    audio_file = "logs/audio/recording.wav"
    
    print(f"Transcribing: {audio_file}")
    
    # Method 1: Simple transcription
    text = recognizer.transcribe_file(audio_file)
    if text:
        print(f"Transcription: {text}")
    else:
        print("Transcription failed or no speech detected")
    
    # Method 2: Transcription with metadata
    result = recognizer.transcribe_with_timestamp(audio_file)
    if result:
        print(f"\nDetailed result:")
        print(f"  Timestamp: {result['timestamp']}")
        print(f"  Text: {result['text']}")
        print(f"  Language: {result['language']}")
        print(f"  Engine: {result['engine']}")
    
    # Change language
    recognizer.set_language("hi-IN")  # Hindi
    
    # Use Whisper for offline transcription (if available)
    text_whisper = recognizer.transcribe_file(audio_file, engine="whisper")
    if text_whisper:
        print(f"\nWhisper transcription: {text_whisper}")
