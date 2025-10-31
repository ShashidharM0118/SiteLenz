"""
Real-time Audio-to-Text Logger Module
Captures audio from microphone and converts to text in real-time
"""

import pyaudio
import wave
import threading
import queue
import json
import os
from datetime import datetime
from pathlib import Path
import logging
import time
import speech_recognition as sr

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AudioToTextLogger:
    """
    Real-time audio recording and transcription class.
    Records audio continuously and processes it for speech-to-text conversion.
    """
    
    def __init__(self, audio_dir="logs/audio", transcript_dir="logs/transcripts", 
                 sample_rate=16000, channels=1, chunk_size=1024, 
                 process_interval=5, engine="google", whisper_model="base"):
        """
        Initialize the audio logger.
        
        Args:
            audio_dir: Directory to save audio files
            transcript_dir: Directory to save transcript JSON files
            sample_rate: Audio sample rate (default: 16000 Hz)
            channels: Number of audio channels (1=mono, 2=stereo)
            chunk_size: Size of audio chunks to read
            process_interval: Seconds between processing audio chunks
            engine: Speech recognition engine ("google" or "whisper")
            whisper_model: Whisper model size if using whisper ("tiny", "base", "small", "medium", "large")
        """
        # Audio settings
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = pyaudio.paInt16
        self.process_interval = process_interval
        
        # Recognition engine
        self.engine = engine
        self.whisper_model = whisper_model
        self.recognizer = sr.Recognizer()
        
        # Directories
        self.audio_dir = Path(audio_dir)
        self.transcript_dir = Path(transcript_dir)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.transcript_dir.mkdir(parents=True, exist_ok=True)
        
        # Session management
        self.session_id = None
        self.session_file = None
        self.transcripts = []
        
        # Recording state
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.frames = []
        
        # Threading
        self.record_thread = None
        self.process_thread = None
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        
        # PyAudio instance
        self.audio = None
        self.stream = None
        
        logger.info("AudioToTextLogger initialized")
    
    def _generate_session_id(self):
        """Generate unique session ID based on timestamp."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _get_audio_filename(self, timestamp):
        """Generate audio filename for a given timestamp."""
        return f"session_{self.session_id}_{timestamp}.wav"
    
    def _get_transcript_filename(self):
        """Generate transcript filename for current session."""
        return f"session_{self.session_id}.json"
    
    def _save_audio_chunk(self, frames, timestamp):
        """Save audio frames to a WAV file."""
        try:
            filename = self._get_audio_filename(timestamp)
            filepath = self.audio_dir / filename
            
            with wave.open(str(filepath), 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))
            
            logger.info(f"Saved audio chunk: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving audio chunk: {e}")
            return None
    
    def _save_transcript(self):
        """Save transcripts to JSON file."""
        try:
            with self.lock:
                filepath = self.transcript_dir / self._get_transcript_filename()
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'session_id': self.session_id,
                        'started_at': self.transcripts[0]['timestamp'] if self.transcripts else None,
                        'transcripts': self.transcripts
                    }, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved transcript: {filepath.name}")
        except Exception as e:
            logger.error(f"Error saving transcript: {e}")
    
    def _transcribe_audio(self, audio_data):
        """
        Transcribe audio data using specified engine.
        
        Args:
            audio_data: AudioData object from speech_recognition
            
        Returns:
            str: Transcribed text or None if failed
        """
        try:
            if self.engine == "google":
                # Use Google Speech Recognition (online)
                text = self.recognizer.recognize_google(audio_data)
                return text
            elif self.engine == "whisper":
                # Use OpenAI Whisper (offline)
                text = self.recognizer.recognize_whisper(
                    audio_data, 
                    model=self.whisper_model,
                    language="english"
                )
                return text
            else:
                logger.error(f"Unknown engine: {self.engine}")
                return None
        except sr.UnknownValueError:
            logger.debug("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return None
    
    def _record_audio(self):
        """Record audio in background thread."""
        logger.info("Recording thread started")
        
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            logger.info("Audio stream opened")
            
            while not self.stop_event.is_set():
                try:
                    data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    self.frames.append(data)
                    self.audio_queue.put(data)
                except Exception as e:
                    logger.error(f"Error reading audio: {e}")
                    break
            
            # Cleanup
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.audio:
                self.audio.terminate()
            
            logger.info("Recording thread stopped")
            
        except Exception as e:
            logger.error(f"Recording thread error: {e}")
    
    def _process_audio(self):
        """Process audio chunks for transcription in background thread."""
        logger.info("Processing thread started")
        
        chunk_frames = []
        last_process_time = time.time()
        
        while not self.stop_event.is_set() or not self.audio_queue.empty():
            try:
                # Collect audio data
                try:
                    data = self.audio_queue.get(timeout=0.5)
                    chunk_frames.append(data)
                except queue.Empty:
                    continue
                
                # Process every N seconds
                current_time = time.time()
                if current_time - last_process_time >= self.process_interval:
                    if chunk_frames:
                        logger.info(f"Processing {len(chunk_frames)} audio chunks")
                        
                        # Save audio chunk
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                        audio_filename = self._save_audio_chunk(chunk_frames, timestamp)
                        
                        # Convert to AudioData for recognition
                        try:
                            audio_bytes = b''.join(chunk_frames)
                            audio_data = sr.AudioData(
                                audio_bytes,
                                self.sample_rate,
                                self.audio.get_sample_size(self.format)
                            )
                            
                            # Transcribe
                            text = self._transcribe_audio(audio_data)
                            
                            if text:
                                transcript_entry = {
                                    'timestamp': datetime.now().isoformat(),
                                    'text': text,
                                    'audio_file': audio_filename
                                }
                                
                                with self.lock:
                                    self.transcripts.append(transcript_entry)
                                
                                logger.info(f"Transcribed: {text[:50]}...")
                                
                                # Save incrementally
                                self._save_transcript()
                            
                        except Exception as e:
                            logger.error(f"Error processing audio chunk: {e}")
                        
                        # Reset for next interval
                        chunk_frames = []
                        last_process_time = current_time
                
            except Exception as e:
                logger.error(f"Processing thread error: {e}")
        
        # Process remaining frames
        if chunk_frames:
            logger.info("Processing remaining audio chunks")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            audio_filename = self._save_audio_chunk(chunk_frames, timestamp)
            
            try:
                audio_bytes = b''.join(chunk_frames)
                audio_data = sr.AudioData(
                    audio_bytes,
                    self.sample_rate,
                    self.audio.get_sample_size(self.format)
                )
                text = self._transcribe_audio(audio_data)
                
                if text:
                    transcript_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'text': text,
                        'audio_file': audio_filename
                    }
                    with self.lock:
                        self.transcripts.append(transcript_entry)
                    self._save_transcript()
            except Exception as e:
                logger.error(f"Error processing final chunk: {e}")
        
        logger.info("Processing thread stopped")
    
    def start_recording(self):
        """
        Start recording and transcription session.
        
        Returns:
            str: Session ID for this recording session
        """
        if self.is_recording:
            logger.warning("Recording already in progress")
            return self.session_id
        
        # Initialize session
        self.session_id = self._generate_session_id()
        self.transcripts = []
        self.frames = []
        self.is_recording = True
        self.stop_event.clear()
        
        # Start threads
        self.record_thread = threading.Thread(target=self._record_audio, daemon=True)
        self.process_thread = threading.Thread(target=self._process_audio, daemon=True)
        
        self.record_thread.start()
        self.process_thread.start()
        
        logger.info(f"Recording started - Session ID: {self.session_id}")
        return self.session_id
    
    def stop_recording(self):
        """
        Stop recording and transcription session.
        
        Returns:
            dict: Session summary with transcript count and files
        """
        if not self.is_recording:
            logger.warning("No recording in progress")
            return None
        
        logger.info("Stopping recording...")
        
        # Signal threads to stop
        self.stop_event.set()
        
        # Wait for threads to finish
        if self.record_thread and self.record_thread.is_alive():
            self.record_thread.join(timeout=5)
        if self.process_thread and self.process_thread.is_alive():
            self.process_thread.join(timeout=10)
        
        self.is_recording = False
        
        # Final save
        self._save_transcript()
        
        summary = {
            'session_id': self.session_id,
            'transcript_count': len(self.transcripts),
            'transcript_file': str(self.transcript_dir / self._get_transcript_filename()),
            'audio_dir': str(self.audio_dir)
        }
        
        logger.info(f"Recording stopped - {len(self.transcripts)} transcripts saved")
        return summary
    
    def get_transcripts(self, session_id=None):
        """
        Get transcripts for a session.
        
        Args:
            session_id: Session ID to retrieve (default: current session)
            
        Returns:
            list: List of transcript dictionaries
        """
        if session_id is None:
            # Return current session transcripts
            with self.lock:
                return self.transcripts.copy()
        else:
            # Load from file
            try:
                filepath = self.transcript_dir / f"session_{session_id}.json"
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('transcripts', [])
            except FileNotFoundError:
                logger.error(f"Session not found: {session_id}")
                return []
            except Exception as e:
                logger.error(f"Error loading transcripts: {e}")
                return []
    
    def search_keywords(self, keywords, session_id=None, case_sensitive=False):
        """
        Search for keywords in transcripts.
        
        Args:
            keywords: List of keywords to search for
            session_id: Session ID to search (default: current session)
            case_sensitive: Whether search should be case-sensitive
            
        Returns:
            list: List of matching transcript entries with keyword info
        """
        transcripts = self.get_transcripts(session_id)
        matches = []
        
        for transcript in transcripts:
            text = transcript['text']
            if not case_sensitive:
                text = text.lower()
                keywords_to_search = [k.lower() for k in keywords]
            else:
                keywords_to_search = keywords
            
            found_keywords = [kw for kw in keywords_to_search if kw in text]
            
            if found_keywords:
                match = transcript.copy()
                match['matched_keywords'] = found_keywords
                matches.append(match)
        
        logger.info(f"Found {len(matches)} matches for keywords: {keywords}")
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
            'transcript_count': len(self.transcripts),
            'engine': self.engine,
            'sample_rate': self.sample_rate,
            'process_interval': self.process_interval
        }
    
    def list_sessions(self):
        """
        List all available recording sessions.
        
        Returns:
            list: List of session IDs
        """
        try:
            session_files = list(self.transcript_dir.glob("session_*.json"))
            sessions = []
            for file in session_files:
                session_id = file.stem.replace("session_", "")
                sessions.append(session_id)
            return sorted(sessions, reverse=True)
        except Exception as e:
            logger.error(f"Error listing sessions: {e}")
            return []
