"""
Transcript Manager Module
Manages transcripts using JSON files (no database required)
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TranscriptManager:
    """
    Manages audio transcripts using JSON file storage
    """
    
    def __init__(self, base_dir: str = "logs/transcripts"):
        """
        Initialize the transcript manager
        
        Args:
            base_dir: Base directory for storing transcript JSON files
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"TranscriptManager initialized. Storage: {self.base_dir}")
    
    def _get_session_file(self, session_id: str) -> Path:
        """
        Get the JSON file path for a session
        
        Args:
            session_id: Session identifier
        
        Returns:
            Path to session JSON file
        """
        return self.base_dir / f"session_{session_id}.json"
    
    def _load_session(self, session_id: str) -> Dict:
        """
        Load session data from JSON file
        
        Args:
            session_id: Session identifier
        
        Returns:
            Session dictionary with structure:
            {
                "session_id": "20251107_143000",
                "created_at": "2025-11-07T14:30:00",
                "transcripts": [...]
            }
        """
        session_file = self._get_session_file(session_id)
        
        if session_file.exists():
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error loading session {session_id}: {e}")
                return self._create_new_session(session_id)
        else:
            return self._create_new_session(session_id)
    
    def _create_new_session(self, session_id: str) -> Dict:
        """
        Create a new session structure
        
        Args:
            session_id: Session identifier
        
        Returns:
            New session dictionary
        """
        return {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "transcripts": []
        }
    
    def _save_session(self, session_data: Dict):
        """
        Save session data to JSON file
        
        Args:
            session_data: Session dictionary to save
        """
        session_id = session_data["session_id"]
        session_file = self._get_session_file(session_id)
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Session saved: {session_id}")
        except Exception as e:
            logger.error(f"Error saving session {session_id}: {e}")
            raise
    
    def save_transcript(self, session_id: str, timestamp: str, audio_file: str, text: str, **metadata):
        """
        Save a transcript entry to session
        
        Args:
            session_id: Session identifier
            timestamp: ISO timestamp of transcription
            audio_file: Path to audio file
            text: Transcribed text
            **metadata: Additional metadata (language, engine, etc.)
        """
        session_data = self._load_session(session_id)
        
        transcript_entry = {
            "timestamp": timestamp,
            "audio_file": str(Path(audio_file).absolute()),
            "text": text,
            **metadata
        }
        
        session_data["transcripts"].append(transcript_entry)
        self._save_session(session_data)
        
        logger.info(f"Transcript added to session {session_id}: {len(text)} characters")
    
    def get_transcripts(self, session_id: str) -> List[Dict]:
        """
        Get all transcripts for a session
        
        Args:
            session_id: Session identifier
        
        Returns:
            List of transcript dictionaries
        """
        session_data = self._load_session(session_id)
        return session_data.get("transcripts", [])
    
    def search_keywords(self, keywords_list: List[str], session_id: Optional[str] = None) -> List[Dict]:
        """
        Search for transcripts containing specific keywords
        
        Args:
            keywords_list: List of keywords to search for
            session_id: Optional session to search in (searches all sessions if None)
        
        Returns:
            List of matching transcript entries with session info
        """
        matching_entries = []
        
        # Determine which sessions to search
        if session_id:
            session_files = [self._get_session_file(session_id)]
        else:
            session_files = list(self.base_dir.glob("session_*.json"))
        
        # Search through sessions
        for session_file in session_files:
            if not session_file.exists():
                continue
            
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                # Check each transcript
                for transcript in session_data.get("transcripts", []):
                    text = transcript.get("text", "").lower()
                    
                    # Check if any keyword matches
                    if any(keyword.lower() in text for keyword in keywords_list):
                        # Add session info to result
                        result = transcript.copy()
                        result["session_id"] = session_data["session_id"]
                        matching_entries.append(result)
            
            except json.JSONDecodeError as e:
                logger.error(f"Error reading session file {session_file}: {e}")
                continue
        
        logger.info(f"Found {len(matching_entries)} transcripts matching keywords: {keywords_list}")
        return matching_entries
    
    def export_to_txt(self, session_id: str, output_file: str):
        """
        Export session transcripts to plain text file
        
        Args:
            session_id: Session identifier
            output_file: Path to output text file
        """
        session_data = self._load_session(session_id)
        transcripts = session_data.get("transcripts", [])
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Session: {session_id}\n")
                f.write(f"Created: {session_data.get('created_at', 'Unknown')}\n")
                f.write(f"Total Transcripts: {len(transcripts)}\n")
                f.write("=" * 80 + "\n\n")
                
                for idx, transcript in enumerate(transcripts, 1):
                    f.write(f"--- Transcript #{idx} ---\n")
                    f.write(f"Timestamp: {transcript.get('timestamp', 'N/A')}\n")
                    f.write(f"Audio File: {transcript.get('audio_file', 'N/A')}\n")
                    f.write(f"Text: {transcript.get('text', '')}\n")
                    f.write("\n")
            
            logger.info(f"Exported {len(transcripts)} transcripts to: {output_path}")
        
        except Exception as e:
            logger.error(f"Error exporting to TXT: {e}")
            raise
    
    def export_to_json(self, session_id: str, output_file: str):
        """
        Export session transcripts to JSON file
        
        Args:
            session_id: Session identifier
            output_file: Path to output JSON file
        """
        session_data = self._load_session(session_id)
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported session to: {output_path}")
        
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise
    
    def list_sessions(self) -> List[str]:
        """
        List all available session IDs
        
        Returns:
            List of session ID strings
        """
        session_files = list(self.base_dir.glob("session_*.json"))
        session_ids = [f.stem.replace("session_", "") for f in session_files]
        return sorted(session_ids)
    
    def get_session_stats(self, session_id: str) -> Dict:
        """
        Get statistics for a session
        
        Args:
            session_id: Session identifier
        
        Returns:
            Dictionary with session statistics
        """
        session_data = self._load_session(session_id)
        transcripts = session_data.get("transcripts", [])
        
        total_chars = sum(len(t.get("text", "")) for t in transcripts)
        total_words = sum(len(t.get("text", "").split()) for t in transcripts)
        
        return {
            "session_id": session_id,
            "created_at": session_data.get("created_at", "Unknown"),
            "total_transcripts": len(transcripts),
            "total_characters": total_chars,
            "total_words": total_words,
            "average_words_per_transcript": total_words // len(transcripts) if transcripts else 0
        }


# Example usage
if __name__ == "__main__":
    # Initialize manager
    manager = TranscriptManager()
    
    # Save a transcript
    session_id = "20251107_143000"
    manager.save_transcript(
        session_id=session_id,
        timestamp="2025-11-07T14:30:05",
        audio_file="logs/audio/recording_001.wav",
        text="This is a test transcription of audio recording.",
        language="en-US",
        engine="google"
    )
    
    # Add another transcript
    manager.save_transcript(
        session_id=session_id,
        timestamp="2025-11-07T14:31:12",
        audio_file="logs/audio/recording_002.wav",
        text="This is another test recording with different content.",
        language="en-US",
        engine="google"
    )
    
    # Get all transcripts for session
    transcripts = manager.get_transcripts(session_id)
    print(f"\nSession {session_id} has {len(transcripts)} transcripts:")
    for t in transcripts:
        print(f"  - {t['timestamp']}: {t['text'][:50]}...")
    
    # Search for keywords
    matches = manager.search_keywords(["test", "recording"])
    print(f"\nFound {len(matches)} transcripts with keywords:")
    for m in matches:
        print(f"  - Session {m['session_id']}: {m['text'][:50]}...")
    
    # Get session statistics
    stats = manager.get_session_stats(session_id)
    print(f"\nSession Statistics:")
    print(f"  Total Transcripts: {stats['total_transcripts']}")
    print(f"  Total Words: {stats['total_words']}")
    print(f"  Avg Words/Transcript: {stats['average_words_per_transcript']}")
    
    # Export to text file
    manager.export_to_txt(session_id, f"exports/session_{session_id}.txt")
    print(f"\nExported to text file!")
    
    # Export to JSON
    manager.export_to_json(session_id, f"exports/session_{session_id}_export.json")
    print(f"Exported to JSON file!")
    
    # List all sessions
    all_sessions = manager.list_sessions()
    print(f"\nAll available sessions: {all_sessions}")
