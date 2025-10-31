"""
Quick Test Script for Audio Logger Module
Tests basic functionality without recording
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    try:
        import pyaudio
        print("✅ PyAudio imported successfully")
    except ImportError as e:
        print(f"❌ PyAudio import failed: {e}")
        return False
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition imported successfully")
    except ImportError as e:
        print(f"❌ SpeechRecognition import failed: {e}")
        return False
    
    try:
        from audio_logger import AudioToTextLogger
        print("✅ AudioToTextLogger imported successfully")
    except ImportError as e:
        print(f"❌ AudioToTextLogger import failed: {e}")
        return False
    
    return True


def test_audio_devices():
    """Test if audio input devices are available."""
    print("\nTesting audio devices...")
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        
        device_count = p.get_device_count()
        print(f"✅ Found {device_count} audio devices")
        
        # List input devices
        input_devices = []
        for i in range(device_count):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append(info)
                print(f"   📍 Input Device {i}: {info['name']}")
        
        if not input_devices:
            print("⚠️  No input devices found! Check microphone connection.")
            return False
        
        # Check default input device
        try:
            default_info = p.get_default_input_device_info()
            print(f"\n✅ Default input device: {default_info['name']}")
        except Exception as e:
            print(f"⚠️  No default input device: {e}")
        
        p.terminate()
        return len(input_devices) > 0
        
    except Exception as e:
        print(f"❌ Audio device test failed: {e}")
        return False


def test_logger_initialization():
    """Test if AudioLogger can be initialized."""
    print("\nTesting AudioToTextLogger initialization...")
    try:
        from audio_logger import AudioToTextLogger
        
        logger = AudioToTextLogger(
            audio_dir="logs/audio",
            transcript_dir="logs/transcripts",
            engine="google"
        )
        print("✅ AudioToTextLogger initialized successfully")
        
        info = logger.get_session_info()
        print(f"   Session ID: {info['session_id']}")
        print(f"   Recording: {info['is_recording']}")
        print(f"   Engine: {info['engine']}")
        print(f"   Sample Rate: {info['sample_rate']} Hz")
        
        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False


def test_directory_structure():
    """Test if required directories exist."""
    print("\nTesting directory structure...")
    
    audio_dir = Path("logs/audio")
    transcript_dir = Path("logs/transcripts")
    
    if audio_dir.exists():
        print(f"✅ Audio directory exists: {audio_dir}")
    else:
        print(f"⚠️  Audio directory not found: {audio_dir}")
    
    if transcript_dir.exists():
        print(f"✅ Transcript directory exists: {transcript_dir}")
    else:
        print(f"⚠️  Transcript directory not found: {transcript_dir}")
    
    return audio_dir.exists() and transcript_dir.exists()


def test_session_management():
    """Test session listing and management."""
    print("\nTesting session management...")
    try:
        from audio_logger import AudioToTextLogger
        
        logger = AudioToTextLogger()
        sessions = logger.list_sessions()
        
        print(f"✅ Found {len(sessions)} existing sessions")
        if sessions:
            print("   Recent sessions:")
            for session in sessions[:3]:
                print(f"   - {session}")
        
        return True
    except Exception as e:
        print(f"❌ Session management test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Audio Logger Module - System Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Import Test", test_imports),
        ("Audio Devices Test", test_audio_devices),
        ("Directory Structure Test", test_directory_structure),
        ("Logger Initialization Test", test_logger_initialization),
        ("Session Management Test", test_session_management),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Audio logger is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python audio_integration.py' for interactive demo")
        print("2. Run 'python audio_web_api.py' for web interface")
        print("3. Check AUDIO_MODULE_README.md for full documentation")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("Common issues:")
        print("- No microphone connected or permissions not granted")
        print("- Audio drivers not installed properly")
        print("- Missing dependencies (run: pip install -r requirements_audio.txt)")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
