"""
Integration Helper Module
Simple wrapper to integrate speech-to-text with existing audio recorder
"""

from pathlib import Path
from typing import List, Dict, Optional
import logging
from datetime import datetime

from speech_recognizer import SpeechRecognizer
from transcript_manager import TranscriptManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioTextIntegration:
    """
    Integration wrapper for audio recording + speech-to-text transcription
    """
    
    def __init__(self, session_id: Optional[str] = None, language: str = "en-US", 
                 transcripts_dir: str = "logs/transcripts"):
        """
        Initialize the audio-text integration
        
        Args:
            session_id: Session identifier (auto-generated if None)
            language: Language code for transcription
            transcripts_dir: Directory for storing transcripts
        """
        # Generate session ID if not provided
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.session_id = session_id
        self.recognizer = SpeechRecognizer(default_language=language)
        self.manager = TranscriptManager(base_dir=transcripts_dir)
        
        logger.info(f"AudioTextIntegration initialized for session: {session_id}")
    
    def process_audio_file(self, audio_file: str, engine: str = "google") -> Optional[str]:
        """
        Process a single audio file: transcribe and save
        
        Args:
            audio_file: Path to audio file (WAV format recommended)
            engine: Transcription engine ('google' or 'whisper')
        
        Returns:
            Transcribed text, or None if transcription failed
        
        Example:
            >>> ati = AudioTextIntegration(session_id="exam_123")
            >>> text = ati.process_audio_file("logs/audio/recording.wav")
            >>> print(f"Transcription: {text}")
        """
        logger.info(f"Processing audio file: {audio_file}")
        
        # Transcribe with metadata
        result = self.recognizer.transcribe_with_timestamp(audio_file, engine)
        
        if result is None:
            logger.warning(f"Failed to transcribe: {audio_file}")
            return None
        
        # Save to transcript manager
        self.manager.save_transcript(
            session_id=self.session_id,
            timestamp=result["timestamp"],
            audio_file=result["audio_file"],
            text=result["text"],
            language=result["language"],
            engine=result["engine"]
        )
        
        logger.info(f"Successfully processed and saved transcript")
        return result["text"]
    
    def process_audio_folder(self, folder_path: str, file_pattern: str = "*.wav", 
                            engine: str = "google") -> Dict[str, str]:
        """
        Batch process multiple audio files from a folder
        
        Args:
            folder_path: Path to folder containing audio files
            file_pattern: File pattern to match (e.g., '*.wav', '*.mp3')
            engine: Transcription engine to use
        
        Returns:
            Dictionary mapping file paths to transcribed text
            {
                "file1.wav": "transcribed text 1",
                "file2.wav": None,  # if failed
                "file3.wav": "transcribed text 3"
            }
        
        Example:
            >>> ati = AudioTextIntegration(session_id="batch_001")
            >>> results = ati.process_audio_folder("logs/audio/", "*.wav")
            >>> print(f"Processed {len(results)} files")
        """
        folder = Path(folder_path)
        
        if not folder.exists():
            logger.error(f"Folder not found: {folder_path}")
            return {}
        
        # Find all audio files matching pattern
        audio_files = list(folder.glob(file_pattern))
        logger.info(f"Found {len(audio_files)} audio files to process")
        
        results = {}
        
        for idx, audio_file in enumerate(audio_files, 1):
            logger.info(f"Processing file {idx}/{len(audio_files)}: {audio_file.name}")
            
            text = self.process_audio_file(str(audio_file), engine)
            results[str(audio_file)] = text
        
        successful = sum(1 for v in results.values() if v is not None)
        logger.info(f"Batch processing complete: {successful}/{len(audio_files)} successful")
        
        return results
    
    def get_session_transcript(self, session_id: Optional[str] = None) -> List[Dict]:
        """
        Get all transcripts for a session
        
        Args:
            session_id: Session identifier (uses current session if None)
        
        Returns:
            List of transcript dictionaries
        
        Example:
            >>> ati = AudioTextIntegration(session_id="exam_123")
            >>> transcripts = ati.get_session_transcript()
            >>> for t in transcripts:
            ...     print(f"{t['timestamp']}: {t['text']}")
        """
        if session_id is None:
            session_id = self.session_id
        
        transcripts = self.manager.get_transcripts(session_id)
        logger.info(f"Retrieved {len(transcripts)} transcripts for session: {session_id}")
        
        return transcripts
    
    def search_transcripts(self, keywords: List[str], session_id: Optional[str] = None) -> List[Dict]:
        """
        Search transcripts for specific keywords
        
        Args:
            keywords: List of keywords to search for
            session_id: Session to search (searches all if None)
        
        Returns:
            List of matching transcript entries
        
        Example:
            >>> ati = AudioTextIntegration()
            >>> matches = ati.search_transcripts(["error", "warning"])
            >>> print(f"Found {len(matches)} matching transcripts")
        """
        return self.manager.search_keywords(keywords, session_id)
    
    def export_session(self, output_format: str = "txt", output_file: Optional[str] = None, 
                      session_id: Optional[str] = None):
        """
        Export session transcripts to file
        
        Args:
            output_format: Export format ('txt' or 'json')
            output_file: Output file path (auto-generated if None)
            session_id: Session to export (uses current session if None)
        
        Example:
            >>> ati = AudioTextIntegration(session_id="exam_123")
            >>> ati.export_session("txt", "reports/exam_123.txt")
        """
        if session_id is None:
            session_id = self.session_id
        
        # Generate output filename if not provided
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = "txt" if output_format == "txt" else "json"
            output_file = f"exports/session_{session_id}_{timestamp}.{extension}"
        
        # Export based on format
        if output_format == "txt":
            self.manager.export_to_txt(session_id, output_file)
        elif output_format == "json":
            self.manager.export_to_json(session_id, output_file)
        else:
            logger.error(f"Unsupported export format: {output_format}")
            return
        
        logger.info(f"Session exported to: {output_file}")
    
    def get_session_statistics(self, session_id: Optional[str] = None) -> Dict:
        """
        Get statistics for a session
        
        Args:
            session_id: Session identifier (uses current session if None)
        
        Returns:
            Dictionary with session statistics
        
        Example:
            >>> ati = AudioTextIntegration(session_id="exam_123")
            >>> stats = ati.get_session_statistics()
            >>> print(f"Total words: {stats['total_words']}")
        """
        if session_id is None:
            session_id = self.session_id
        
        return self.manager.get_session_stats(session_id)
    
    def change_language(self, language_code: str):
        """
        Change the transcription language
        
        Args:
            language_code: Language code (e.g., 'en-US', 'hi-IN', 'es-ES')
        
        Example:
            >>> ati = AudioTextIntegration()
            >>> ati.change_language("hi-IN")  # Switch to Hindi
        """
        self.recognizer.set_language(language_code)
        logger.info(f"Language changed to: {language_code}")


# Example Usage
if __name__ == "__main__":
    print("=" * 80)
    print("Audio-Text Integration - Example Usage")
    print("=" * 80)
    
    # Example 1: Process single audio file
    print("\n--- Example 1: Single File Processing ---")
    ati = AudioTextIntegration(session_id="exam_123")
    
    # After your existing audio recorder saves a file:
    audio_file = "logs/audio/recording.wav"
    text = ati.process_audio_file(audio_file)
    
    if text:
        print(f"✓ Transcription: {text}")
    else:
        print("✗ Transcription failed")
    
    # Example 2: Batch process folder
    print("\n--- Example 2: Batch Folder Processing ---")
    ati2 = AudioTextIntegration(session_id="batch_session_001")
    results = ati2.process_audio_folder("logs/audio/", "*.wav")
    
    print(f"Processed {len(results)} files:")
    for file, text in results.items():
        status = "✓" if text else "✗"
        preview = text[:50] + "..." if text and len(text) > 50 else text or "Failed"
        print(f"  {status} {Path(file).name}: {preview}")
    
    # Example 3: Get all transcripts for session
    print("\n--- Example 3: Retrieve Session Transcripts ---")
    transcripts = ati.get_session_transcript("exam_123")
    print(f"Session 'exam_123' has {len(transcripts)} transcripts:")
    for t in transcripts:
        print(f"  - {t['timestamp']}: {t['text'][:50]}...")
    
    # Example 4: Search across transcripts
    print("\n--- Example 4: Keyword Search ---")
    matches = ati.search_transcripts(["test", "recording", "audio"])
    print(f"Found {len(matches)} transcripts with keywords:")
    for m in matches:
        print(f"  - Session {m['session_id']}: {m['text'][:50]}...")
    
    # Example 5: Export session
    print("\n--- Example 5: Export Session ---")
    ati.export_session("txt", "reports/exam_123_transcript.txt")
    ati.export_session("json", "reports/exam_123_transcript.json")
    print("✓ Session exported to reports/")
    
    # Example 6: Get statistics
    print("\n--- Example 6: Session Statistics ---")
    stats = ati.get_session_statistics("exam_123")
    print(f"Session Statistics:")
    print(f"  Total Transcripts: {stats['total_transcripts']}")
    print(f"  Total Words: {stats['total_words']}")
    print(f"  Total Characters: {stats['total_characters']}")
    print(f"  Avg Words/Transcript: {stats['average_words_per_transcript']}")
    
    # Example 7: Change language
    print("\n--- Example 7: Multi-language Support ---")
    ati.change_language("hi-IN")  # Switch to Hindi
    # Now process Hindi audio files...
    
    print("\n" + "=" * 80)
    print("Integration examples complete!")
    print("=" * 80)
