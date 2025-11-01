# SiteLenz Flutter Mobile App

Native Android/iOS mobile application for infrastructure monitoring and defect detection.

## Features

- 🎤 **Voice + Image Capture**: Record voice observations and capture images simultaneously
- 📸 **Camera Classification**: Take photos and get instant defect classification
- 📜 **Unified Logs**: View all voice transcripts with associated images and classifications
- ⚙️ **Server Configuration**: Easy server connection setup
- 🌐 **Cross-platform**: Works on Android and iOS

## Setup

### Prerequisites

1. Install Flutter: https://flutter.dev/docs/get-started/install
2. Install Android Studio or Xcode
3. Make sure your backend server is running

### Installation

```bash
# Navigate to flutter app directory
cd flutter_app

# Get dependencies
flutter pub get

# Run on connected device/emulator
flutter run

# Build APK for Android
flutter build apk --release

# Build for iOS
flutter build ios --release
```

### Server Configuration

1. Open the app
2. Go to "Settings" tab
3. Enter your server URL (e.g., `http://192.168.1.100:5000`)
4. Tap "Test Connection"
5. Once connected, you're ready to use the app!

## Building APK

```bash
# Debug APK (for testing)
flutter build apk --debug

# Release APK (for distribution)
flutter build apk --release

# Split APKs by ABI (smaller file sizes)
flutter build apk --split-per-abi --release
```

APK will be located in `build/app/outputs/flutter-apk/`

## Project Structure

```
lib/
├── main.dart                   # App entry point
├── screens/
│   ├── home_screen.dart        # Main navigation
│   ├── voice_image_screen.dart # Voice + Image capture
│   ├── camera_screen.dart      # Camera-only mode
│   ├── logs_screen.dart        # View all logs
│   └── settings_screen.dart    # Server configuration
├── services/
│   └── api_service.dart        # Backend API communication
└── widgets/                    # Reusable components
```

## Permissions

The app requires the following permissions:
- Camera: For taking photos
- Microphone: For voice recording
- Internet: For server communication
- Storage: For saving images

## Troubleshooting

### Cannot connect to server
- Ensure both devices are on the same WiFi network
- Check if server is running (`python app.py`)
- Verify the server URL format: `http://YOUR_IP:5000`
- Try disabling firewall temporarily

### Camera not working
- Grant camera permissions in app settings
- Restart the app
- Check if other apps can use the camera

### Voice recording issues
- Grant microphone permissions
- Ensure device has a working microphone
- Check system audio settings

## Technologies Used

- Flutter 3.0+
- Dart
- Camera plugin
- Speech-to-text
- HTTP client
- Provider state management

## License

MIT License
