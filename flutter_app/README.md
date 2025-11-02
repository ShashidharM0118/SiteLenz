# SiteLenz - Infrastructure Monitoring & Defect Detection

Complete mobile application for infrastructure monitoring with AI-powered defect detection, voice annotations, and 3D reconstruction capabilities.

---

## 🚀 Quick Start

### Prerequisites

1. **Flutter SDK** (3.0+): https://flutter.dev/docs/get-started/install
2. **Android Studio** or **Xcode** (for iOS)
3. **Python Backend Server** running (see Backend Setup below)

### Installation & Running

```bash
# 1. Navigate to flutter app directory
cd flutter_app

# 2. Install dependencies
flutter pub get

# 3. Run on connected device/emulator
flutter run

# 4. Build APK for Android
flutter build apk --release
```

APK will be in: `build/app/outputs/flutter-apk/app-release.apk`

---

## 📱 Features

### Core Features
- 🎤 **Voice + Image Capture**: Record voice observations while capturing images
- 📸 **Camera Classification**: Instant AI-powered defect detection
- 🏗️ **3D Room Reconstruction**: Capture multiple images to create 3D models
- 👁️ **3D Model Viewer**: Interactive viewer with AR support
- 📜 **Unified Logs**: View transcripts, images, and classifications
- ⚙️ **Server Configuration**: Easy backend connection setup

### 3D Viewer Capabilities
- ✅ GLB/GLTF model support
- ✅ Interactive touch controls (rotate, zoom, pan)
- ✅ Auto-rotation mode
- ✅ AR viewing (device-dependent)
- ✅ Multiple background options
- ✅ Settings panel
- ✅ Loading states & error handling

---

## 🖥️ Backend Setup (Python Server)

### Fix PyTorch DLL Error

The error you're seeing is due to missing Visual C++ Redistributables. Fix it:

**Option 1: Install Visual C++ Redistributables (Recommended)**
```powershell
# Download and install:
# https://aka.ms/vs/17/release/vc_redist.x64.exe
```

**Option 2: Reinstall PyTorch**
```powershell
# Uninstall current PyTorch
pip uninstall torch torchvision torchaudio

# Reinstall with CPU version (more stable)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**Option 3: Use Conda (Most Reliable)**
```powershell
# If you have Conda/Miniconda
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

### Start Backend Server

```powershell
# Navigate to project root
cd E:\projects\major_project

# Install Python dependencies (if not done)
pip install -r requirements.txt

# Start the server
python app.py
```

Server will run on: `http://localhost:5000`

### Verify Server is Running

```powershell
# Check if port 5000 is active
netstat -ano | findstr :5000

# You should see:
# TCP    0.0.0.0:5000    0.0.0.0:0    LISTENING
```

---

## 📱 App Configuration

### 1. Connect to Server

1. Open the app
2. Go to **Settings** tab
3. Enter server URL:
   - **Local device**: `http://localhost:5000`
   - **Same WiFi**: `http://YOUR_PC_IP:5000` (e.g., `http://192.168.1.100:5000`)
   - **Remote**: Your server's public URL
4. Tap **"Test Connection"**
5. Wait for success message ✅

### 2. Get Your PC's IP Address

```powershell
# Run in PowerShell
ipconfig

# Look for "IPv4 Address" under your active network adapter
# Example: 192.168.1.100
```

### 3. Allow Firewall Access

If app can't connect, allow Python through firewall:

```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="Flask Server" dir=in action=allow protocol=TCP localport=5000
```

---

## 🏗️ Using 3D Model Viewer

### Method 1: Via 3D Reconstruction (Integrated)

1. Open app → Navigate to **"3D Room Reconstruction"**
2. Tap **"Start 3D Session"**
3. Walk around the room and capture **10+ images** from different angles
4. Tap **"Build 3D Model"**
5. Wait for processing to complete
6. Tap **"View 3D Model"** button ✨

### Method 2: Test with Sample Models

Add this code to test the viewer anywhere in your app:

```dart
import 'screens/model_viewer_screen.dart';

// Add test button
ElevatedButton.icon(
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const ModelViewerScreen(
          modelUrl: 'https://modelviewer.dev/shared-assets/models/Astronaut.glb',
          title: 'Test 3D Model',
        ),
      ),
    );
  },
  icon: const Icon(Icons.view_in_ar),
  label: const Text('Test 3D Viewer'),
)
```

### Method 3: View Local Models

1. Place `.glb` files in `assets/models/`
2. Use in code:

```dart
ModelViewerScreen(
  modelPath: 'assets/models/your_model.glb',
  title: 'My Model',
)
```

### 3D Viewer Controls

- **Drag** → Rotate model
- **Pinch** → Zoom in/out
- **Two-finger drag** → Pan camera
- **⚙️ Icon** → Settings (backgrounds, auto-rotate)
- **ℹ️ Icon** → Model information

### Converting PLY to GLB

Your 3D reconstruction outputs `.ply` files. To view them:

**Using Blender (Free):**
1. Download: https://www.blender.org/
2. File → Import → Stanford (.ply)
3. File → Export → glTF 2.0 (.glb)

**Online Converter:**
- https://products.aspose.app/3d/conversion/ply-to-glb

---

## 🔧 Building APK

### Debug Build (For Testing)
```bash
flutter build apk --debug
```

### Release Build (For Distribution)
```bash
flutter build apk --release
```

### Optimized Build (Smaller Size)
```bash
flutter build apk --split-per-abi --release
```

**Output Location:** `build/app/outputs/flutter-apk/`

**File Sizes:**
- Debug: ~50-70 MB
- Release: ~20-30 MB
- Split ABI: ~15-20 MB per architecture

---

## 📂 Project Structure

```
flutter_app/
├── lib/
│   ├── main.dart                          # App entry point & routes
│   ├── screens/
│   │   ├── home_screen.dart               # Main navigation
│   │   ├── voice_image_screen.dart        # Voice + Image capture
│   │   ├── camera_screen.dart             # Camera-only mode
│   │   ├── reconstruction_3d_screen.dart  # 3D reconstruction
│   │   ├── model_viewer_screen.dart       # 3D model viewer
│   │   ├── model_viewer_examples.dart     # Code examples
│   │   ├── logs_screen.dart               # View all logs
│   │   └── settings_screen.dart           # Server config
│   ├── services/
│   │   └── api_service.dart               # Backend API
│   └── widgets/                           # Reusable components
├── assets/
│   ├── images/                            # App images
│   ├── icons/                             # App icons
│   └── models/                            # 3D model files (.glb)
├── android/                               # Android config
├── ios/                                   # iOS config
├── pubspec.yaml                           # Dependencies
└── README.md                              # This file
```

---

## 🔐 Permissions Required

The app requires these permissions:

| Permission | Purpose |
|------------|---------|
| 📷 Camera | Taking photos for defect detection |
| 🎤 Microphone | Voice recording and annotations |
| 🌐 Internet | Backend server communication |
| 💾 Storage | Saving captured images |
| 📱 AR (optional) | Augmented reality 3D viewing |

Permissions are requested automatically on first use.

---

## 🐛 Troubleshooting

### Backend Issues

#### Error: "DLL load failed while importing _C"

**Solution:**
```powershell
# Install Visual C++ Redistributables
# Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

# OR reinstall PyTorch
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### Server Not Starting

```powershell
# Check if port 5000 is already in use
netstat -ano | findstr :5000

# Kill process if needed (replace PID)
taskkill /PID <PID> /F

# Restart server
python app.py
```

### Flutter Build Issues

#### Error: "Gradle build failed"

```bash
# Clean build
cd flutter_app
flutter clean
flutter pub get
flutter build apk --release
```

#### Error: "SDK location not found"

Create `android/local.properties`:
```properties
sdk.dir=C:\\Users\\YourUsername\\AppData\\Local\\Android\\sdk
```

### App Connection Issues

#### Cannot Connect to Server

1. **Check server is running:**
   ```powershell
   netstat -ano | findstr :5000
   ```

2. **Check firewall:**
   ```powershell
   netsh advfirewall firewall add rule name="Flask Server" dir=in action=allow protocol=TCP localport=5000
   ```

3. **Get correct IP:**
   ```powershell
   ipconfig
   # Use IPv4 address
   ```

4. **Test from browser:**
   - Open: `http://YOUR_IP:5000` on phone's browser
   - Should see backend response

5. **Ensure same WiFi:**
   - PC and phone must be on same network
   - Check if network allows device-to-device communication

#### 3D Model Not Loading

1. **Check file format** - Must be `.glb` or `.gltf`
2. **Test with sample URL first:**
   ```
   https://modelviewer.dev/shared-assets/models/Astronaut.glb
   ```
3. **Check internet connection** (for remote URLs)
4. **Verify file size** - Keep under 20 MB for smooth loading

#### Camera Not Working

1. Go to phone Settings → Apps → SiteLenz → Permissions
2. Enable Camera permission
3. Restart the app

#### Voice Recording Issues

1. Enable Microphone permission in app settings
2. Test microphone in another app
3. Check if phone is in silent mode

---

## 🛠️ Development

### Adding Dependencies

```bash
# Add to pubspec.yaml, then:
flutter pub get
```

### Hot Reload During Development

```bash
flutter run

# Then press 'r' to hot reload
# Press 'R' to hot restart
```

### Running Tests

```bash
flutter test
```

### Checking for Issues

```bash
flutter doctor
flutter analyze
```

---

## 📦 Key Dependencies

### Flutter Packages

```yaml
# UI & Design
cupertino_icons: ^1.0.6
google_fonts: ^6.1.0
flutter_animate: ^4.3.0

# Camera & Media
camera: ^0.10.5+5
image_picker: ^1.0.4
permission_handler: ^11.0.1

# 3D Viewer
model_viewer_plus: ^1.7.2
webview_flutter: ^4.4.2

# Networking
http: ^1.1.0
dio: ^5.4.0

# State Management
provider: ^6.1.1

# Storage
shared_preferences: ^2.2.2
sqflite: ^2.3.0
path_provider: ^2.1.1
```

### Python Backend

```
Flask==2.3.2
torch==2.0.1
torchvision==0.15.2
Pillow==9.5.0
whisper (for voice transcription)
```

---

## 🎯 Complete Setup Checklist

### Backend Setup
- [ ] Python 3.8+ installed
- [ ] Visual C++ Redistributables installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] PyTorch working (no DLL errors)
- [ ] Server starts: `python app.py`
- [ ] Port 5000 open: `netstat -ano | findstr :5000`
- [ ] Firewall allows connections

### Flutter Setup
- [ ] Flutter SDK installed
- [ ] Android Studio/Xcode installed
- [ ] Device/emulator connected: `flutter devices`
- [ ] Dependencies installed: `flutter pub get`
- [ ] No build errors: `flutter build apk`
- [ ] App runs: `flutter run`

### App Configuration
- [ ] Server URL configured in Settings
- [ ] Test connection successful
- [ ] Camera permission granted
- [ ] Microphone permission granted
- [ ] Can capture images
- [ ] Can record voice
- [ ] Classifications working
- [ ] 3D reconstruction works
- [ ] 3D viewer displays models

---

## 🚀 Quick Test Workflow

### 1. Start Backend
```powershell
cd E:\projects\major_project
python app.py
# Wait for "Running on http://0.0.0.0:5000"
```

### 2. Get Your IP
```powershell
ipconfig
# Note your IPv4 address (e.g., 192.168.1.100)
```

### 3. Run Flutter App
```powershell
cd flutter_app
flutter run
```

### 4. Configure in App
1. Open Settings
2. Enter: `http://192.168.1.100:5000`
3. Test Connection → Should show ✅

### 5. Test Features
1. **Camera**: Capture image → See classification
2. **Voice**: Record while capturing → See transcript
3. **3D Recon**: Capture 10+ images → Build model → View in 3D viewer
4. **Logs**: View all captured data

---

## 📞 Support & Resources

### Documentation
- **Flutter**: https://flutter.dev/docs
- **model_viewer_plus**: https://pub.dev/packages/model_viewer_plus
- **GLTF Format**: https://www.khronos.org/gltf/

### Free 3D Models for Testing
- **Sketchfab**: https://sketchfab.com/ (filter: Downloadable)
- **Poly Haven**: https://polyhaven.com/models
- **Model Viewer**: https://modelviewer.dev/shared-assets/models/

### Tools
- **Blender** (3D modeling): https://www.blender.org/
- **Android Studio**: https://developer.android.com/studio

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎉 You're Ready!

**To run the complete system:**

1. Fix PyTorch: Install Visual C++ Redistributables
2. Start backend: `python app.py`
3. Run app: `cd flutter_app && flutter run`
4. Configure server URL in app Settings
5. Start monitoring! 🚀

**Need help?** Check the Troubleshooting section above.
