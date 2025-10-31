"""
Simple integration example for AudioToTextLogger
Demonstrates how to integrate audio logging into your desktop application
"""

import time
import sys
from audio_logger import AudioToTextLogger


def simple_example():
    """Basic usage example with keyboard control."""
    print("=" * 60)
    print("Audio-to-Text Logger - Simple Example")
    print("=" * 60)
    
    # Initialize logger
    # Use engine="google" for online recognition (requires internet)
    # Use engine="whisper" for offline recognition (requires whisper package)
    logger = AudioToTextLogger(
        audio_dir="logs/audio",
        transcript_dir="logs/transcripts",
        process_interval=5,  # Process every 5 seconds
        engine="google"  # Change to "whisper" for offline
    )
    
    print("\nAvailable commands:")
    print("  start  - Start recording")
    print("  stop   - Stop recording")
    print("  status - Show current status")
    print("  view   - View transcripts")
    print("  search - Search for keywords")
    print("  list   - List all sessions")
    print("  quit   - Exit program")
    print()
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "start":
                if logger.is_recording:
                    print("⚠️  Already recording!")
                else:
                    session_id = logger.start_recording()
                    print(f"✅ Recording started - Session ID: {session_id}")
                    print("   Speak into your microphone...")
                    print("   Audio will be processed every 5 seconds")
            
            elif command == "stop":
                if not logger.is_recording:
                    print("⚠️  Not currently recording!")
                else:
                    summary = logger.stop_recording()
                    print(f"\n✅ Recording stopped")
                    print(f"   Session ID: {summary['session_id']}")
                    print(f"   Transcripts: {summary['transcript_count']}")
                    print(f"   Saved to: {summary['transcript_file']}")
            
            elif command == "status":
                info = logger.get_session_info()
                print("\n📊 Current Status:")
                print(f"   Session ID: {info['session_id']}")
                print(f"   Recording: {'🔴 Yes' if info['is_recording'] else '⚪ No'}")
                print(f"   Transcripts: {info['transcript_count']}")
                print(f"   Engine: {info['engine']}")
                print(f"   Sample Rate: {info['sample_rate']} Hz")
            
            elif command == "view":
                transcripts = logger.get_transcripts()
                if not transcripts:
                    print("📭 No transcripts available")
                else:
                    print(f"\n📝 Transcripts ({len(transcripts)}):")
                    for i, t in enumerate(transcripts, 1):
                        print(f"\n   [{i}] {t['timestamp']}")
                        print(f"       Text: {t['text']}")
                        print(f"       Audio: {t['audio_file']}")
            
            elif command == "search":
                keywords_input = input("   Enter keywords (comma-separated): ")
                keywords = [k.strip() for k in keywords_input.split(',')]
                matches = logger.search_keywords(keywords)
                
                if not matches:
                    print(f"🔍 No matches found for: {', '.join(keywords)}")
                else:
                    print(f"\n🔍 Found {len(matches)} matches:")
                    for i, match in enumerate(matches, 1):
                        print(f"\n   [{i}] {match['timestamp']}")
                        print(f"       Text: {match['text']}")
                        print(f"       Matched: {', '.join(match['matched_keywords'])}")
            
            elif command == "list":
                sessions = logger.list_sessions()
                if not sessions:
                    print("📭 No sessions found")
                else:
                    print(f"\n📁 Available Sessions ({len(sessions)}):")
                    for i, session_id in enumerate(sessions, 1):
                        print(f"   {i}. {session_id}")
            
            elif command == "quit":
                if logger.is_recording:
                    print("\n⚠️  Stopping recording before exit...")
                    logger.stop_recording()
                print("\n👋 Goodbye!")
                break
            
            else:
                print(f"❌ Unknown command: {command}")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            if logger.is_recording:
                print("Stopping recording...")
                logger.stop_recording()
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def timed_recording_example():
    """Example with automatic timed recording."""
    print("=" * 60)
    print("Timed Recording Example (30 seconds)")
    print("=" * 60)
    
    logger = AudioToTextLogger(
        process_interval=5,
        engine="google"
    )
    
    # Start recording
    print("\n🎤 Starting 30-second recording...")
    session_id = logger.start_recording()
    print(f"Session ID: {session_id}")
    print("Speak into your microphone!\n")
    
    # Record for 30 seconds
    try:
        for i in range(30, 0, -1):
            print(f"⏱️  {i} seconds remaining...", end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    
    # Stop recording
    print("\n\n🛑 Stopping recording...")
    summary = logger.stop_recording()
    
    # Show results
    print(f"\n✅ Recording complete!")
    print(f"   Transcripts: {summary['transcript_count']}")
    
    transcripts = logger.get_transcripts()
    if transcripts:
        print(f"\n📝 Transcribed text:")
        for i, t in enumerate(transcripts, 1):
            print(f"\n   [{i}] {t['text']}")


def keyword_monitoring_example():
    """Example with keyword monitoring (suspicious words)."""
    print("=" * 60)
    print("Keyword Monitoring Example")
    print("=" * 60)
    
    # Define suspicious keywords to monitor
    suspicious_keywords = [
        "password", "credit card", "ssn", "confidential",
        "secret", "private", "unauthorized"
    ]
    
    logger = AudioToTextLogger(
        process_interval=5,
        engine="google"
    )
    
    print(f"\n🔍 Monitoring for keywords: {', '.join(suspicious_keywords)}")
    print("Recording for 20 seconds...\n")
    
    # Start recording
    session_id = logger.start_recording()
    
    # Record for 20 seconds
    try:
        time.sleep(20)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
    
    # Stop and check for keywords
    logger.stop_recording()
    
    # Search for suspicious keywords
    matches = logger.search_keywords(suspicious_keywords)
    
    if matches:
        print(f"\n⚠️  ALERT: Found {len(matches)} suspicious mentions!")
        for i, match in enumerate(matches, 1):
            print(f"\n   [{i}] {match['timestamp']}")
            print(f"       Text: {match['text']}")
            print(f"       Keywords: {', '.join(match['matched_keywords'])}")
    else:
        print("\n✅ No suspicious keywords detected")


if __name__ == "__main__":
    print("\nSelect example to run:")
    print("1. Interactive mode (keyboard control)")
    print("2. Timed recording (30 seconds)")
    print("3. Keyword monitoring")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        simple_example()
    elif choice == "2":
        timed_recording_example()
    elif choice == "3":
        keyword_monitoring_example()
    else:
        print("Invalid choice!")
