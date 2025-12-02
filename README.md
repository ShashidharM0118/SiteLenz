# 🏗️ SiteLenz - Infrastructure Monitoring & Defect Detection System

Complete AI-powered system for detecting building defects with mobile app, voice annotations, and 3D reconstruction.

---

## 🎯 Features

### Core Capabilities
- 🤖 **AI Defect Detection**: Vision Transformer (ViT) classifies 7 types of building defects
- 📱 **Mobile App**: Flutter app for Android/iOS with camera integration
- 🎤 **Voice Annotations**: Record observations while capturing images
- 🏗️ **3D Reconstruction**: Create 3D models from multiple images
- 👁️ **3D Model Viewer**: Interactive AR-enabled model viewer
- 📊 **Unified Logging**: Track all inspections with timestamps
- 📄 **AI-Powered PDF Reports**: Comprehensive inspection reports with statistics, risk assessment, and cost estimates (powered by Groq AI)

### Defect Types Detected
1. Algae growth
2. Major cracks
3. Minor cracks
4. Peeling paint
5. Plain (normal surface)
6. Spalling concrete
7. Stains

---

## 🚀 Quick Start

### Prerequisites
- **Python**: 3.10 or 3.11 (3.13 has compatibility issues)
- **Flutter**: 3.0+ for mobile app
- **Visual C++ Redistributables**: Required for PyTorch on Windows

---

## 📱 Mobile App Setup

### 1. Install Flutter Dependencies

```bash
cd flutter_app
flutter pub get
```

### 2. Build & Run

```bash
# Run on connected device
flutter run

# Build release APK
flutter build apk --release
```

**APK Location:** `flutter_app/build/app/outputs/flutter-apk/app-release.apk`

**✅ App is ready!** See `flutter_app/README.md` for detailed instructions.

---

## 🖥️ Backend Server Setup

### Configure API Keys

The project now uses **Groq API** for AI-powered chat and analysis features.

1. **Get a free Groq API key:**
   - Visit: https://console.groq.com/
   - Sign up for a free account
   - Copy your API key

2. **Create `.env` file:**
   ```bash
   # Copy the example file
   cp .env.example .env
   ```

3. **Add your API key to `.env`:**
   ```dotenv
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

4. **Test the configuration:**
   ```bash
   python config_env.py
   # Should show: ✓ GROQ_API_KEY: gsk_xxxx...xxxx
   ```

5. **Test the Groq client:**
   ```bash
   python groq_helper.py
   # Should show successful test responses
   ```

### Fix PyTorch DLL Error (Windows)

**The Issue:** `ImportError: DLL load failed while importing _C`

**Solution 1: Install VC++ Redistributables (RECOMMENDED)**
```
Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
Install and restart your computer
```

**Solution 2: Reinstall PyTorch CPU Version**
```powershell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**Solution 3: Use Python 3.10 Instead of 3.13**
```powershell
# Python 3.13 is too new and has compatibility issues
# Download Python 3.10: https://www.python.org/downloads/
```

### Install Backend Dependencies

```bash
cd E:\projects\major_project
pip install -r requirements.txt
```

### Start the Server

```bash
python app.py
```

Server will run on: `http://localhost:5000`

### Verify Server is Running

```powershell
netstat -ano | findstr :5000

# Should show:
# TCP    0.0.0.0:5000    0.0.0.0:0    LISTENING
```

---

## 📱 Connect Mobile App to Server

### 1. Get Your PC's IP Address

```powershell
ipconfig

# Look for "IPv4 Address" (e.g., 192.168.1.100)
```

### 2. Allow Firewall Access

```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="Flask Server" dir=in action=allow protocol=TCP localport=5000
```

### 3. Configure in App

1. Open SiteLenz app
2. Go to **Settings** tab
3. Enter server URL: `http://YOUR_IP:5000`
4. Tap **"Test Connection"**
5. Wait for success ✅

---

## 🎯 Complete Setup Checklist

### Backend Setup
- [ ] Python 3.10 or 3.11 installed (NOT 3.13)
- [ ] Visual C++ Redistributables installed
- [ ] `.env` file created with GROQ_API_KEY
- [ ] API key working: `python config_env.py`
- [ ] PyTorch working: `python -c "import torch; print(torch.__version__)"`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Model file in `models/vit_weights.pth`
- [ ] Server starts: `python app.py`
- [ ] Port 5000 open: `netstat -ano | findstr :5000`
- [ ] Firewall allows connections

### Mobile App Setup
- [ ] Flutter SDK installed
- [ ] Device/emulator connected: `flutter devices`
- [ ] Dependencies installed: `cd flutter_app && flutter pub get`
- [ ] APK builds: `flutter build apk --release`
- [ ] APK installed on device

### App Configuration
- [ ] Server URL configured in Settings
- [ ] Connection test successful
- [ ] Camera permission granted
- [ ] Microphone permission granted
- [ ] Can capture and classify images
- [ ] Voice recording works
- [ ] Logs display correctly

---

## 📂 Project Structure

```
major_project/
├── app.py                          # Main Flask backend server
├── camera_classifier.py            # Image classification logic
├── requirements.txt                # Python dependencies
│
├── models/                         # AI models
│   ├── vit_weights.pth            # Vision Transformer model
│   └── curat_vt_*.txt             # Model reports
│
├── data/                          # Training dataset
│   ├── train/                     # Training images by class
│   ├── val/                       # Validation images
│   └── test/                      # Test images
│
├── flutter_app/                   # Mobile application
│   ├── lib/                       # Dart source code
│   │   ├── main.dart             # App entry point
│   │   ├── screens/              # App screens
│   │   │   ├── home_screen.dart
│   │   │   ├── camera_screen.dart
│   │   │   ├── reconstruction_3d_screen.dart
│   │   │   ├── model_viewer_screen.dart     # 3D viewer
│   │   │   ├── logs_screen.dart
│   │   │   └── settings_screen.dart
│   │   ├── services/
│   │   │   └── api_service.dart  # Backend API
│   │   └── widgets/              # Reusable components
│   ├── assets/                    # App assets
│   │   ├── images/
│   │   ├── icons/
│   │   └── models/               # 3D model files (.glb)
│   ├── android/                   # Android config
│   ├── pubspec.yaml              # Flutter dependencies
│   └── README.md                 # Flutter app docs
│
├── reconstruction_3d/             # 3D reconstruction module
│   ├── api/                       # REST API endpoints
│   ├── colmap/                    # COLMAP integration
│   ├── processing/                # Model processing
│   ├── sessions/                  # Capture sessions
│   └── output/                    # Generated 3D models
│
├── logs/                          # Application logs
│   ├── audio/                     # Voice recordings
│   ├── transcripts/               # Speech-to-text
│   ├── classifications/           # Detection results
│   └── frames/                    # Captured images
│
├── sample images/                 # Test images
│   └── class_images/             # By defect type
│
├── FIX_PYTORCH_ERROR.md          # PyTorch troubleshooting
└── README.md                      # This file
```

---

## 🛠️ Troubleshooting

### Backend Issues

#### PyTorch DLL Error
```
ImportError: DLL load failed while importing _C
```

**Fix:** Install Visual C++ Redistributables
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
- See `FIX_PYTORCH_ERROR.md` for detailed solutions

#### Server Won't Start
```powershell
# Check if port is in use
netstat -ano | findstr :5000

# Kill process if needed (replace PID)
taskkill /PID <PID> /F
```

#### Module Not Found Errors
```bash
pip install -r requirements.txt
```

### Mobile App Issues

#### Build Failed
```bash
cd flutter_app
flutter clean
flutter pub get
flutter build apk --release
```

#### Can't Connect to Server
1. Check server is running: `netstat -ano | findstr :5000`
2. Check firewall is open (see "Allow Firewall Access" above)
3. Verify IP address is correct
4. Ensure phone and PC are on same WiFi
5. Try accessing `http://YOUR_IP:5000` in phone's browser

#### 3D Model Viewer Not Loading
1. Test with sample URL first:
   ```
   https://modelviewer.dev/shared-assets/models/Astronaut.glb
   ```
2. Check internet connection
3. Verify model file format is `.glb` or `.gltf`
4. Ensure file size is under 20 MB

### Permissions Issues

#### Camera Not Working
- Go to Settings → Apps → SiteLenz → Permissions
- Enable Camera permission
- Restart app

#### Microphone Not Working
- Enable Microphone permission in app settings
- Check if microphone works in other apps

---

## 🎮 Using the App

### 1. Basic Image Classification
1. Open app → **Camera** tab
2. Point at defect and tap capture
3. View classification result instantly

### 2. Voice + Image Capture
1. Go to **Voice + Image** tab
2. Tap record and speak your observations
3. Capture image while recording
4. View combined log with transcript

### 4. 3D Room Reconstruction
1. Navigate to **3D Reconstruction** tab
2. Tap **"Start 3D Session"**
3. Walk around room capturing **10+ images** from different angles
4. Tap **"Build 3D Model"**
5. Wait for processing
6. Tap **"View 3D Model"** to see in 3D viewer

### 5. Generate Professional PDF Report
1. Go to **Reports** tab
2. Tap **"Generate Report"** - AI analyzes all data and generates 10+ page professional report
3. Download or share the PDF

### 6. 3D Model Viewer Controls
- **Drag** → Rotate model
- **Pinch** → Zoom in/out
- **Two-finger drag** → Pan camera
- **⚙️ Icon** → Settings (background, auto-rotate)
- **ℹ️ Icon** → Model information
- **AR Mode** → View in augmented reality (if device supports)

---

## 📊 Model Specifications

### AI Model
- **Architecture**: Vision Transformer (ViT-Base-Patch16-224)
- **Parameters**: ~86 million
- **Input Size**: 224×224 RGB images
- **Output**: 7 defect classes + confidence scores
- **Model Size**: ~330 MB
- **Training**: 200 epochs on Kaggle T4 x2 GPU

### 3D Reconstruction
- **Method**: COLMAP Structure-from-Motion
- **Input**: 10+ images from different angles
- **Output**: PLY point cloud (convertible to GLB)
- **Processing Time**: 2-5 minutes (depends on image count)

---

## 🔧 Development

### Backend Development
```bash
# Run in development mode
python app.py

# The server auto-reloads on code changes
```

### Mobile App Development
```bash
cd flutter_app

# Hot reload during development
flutter run
# Press 'r' for hot reload
# Press 'R' for hot restart

# Check for issues
flutter doctor
flutter analyze
```

### Adding New Features

**Backend:**
- Add routes in `app.py`
- Implement logic in appropriate files
- Update `requirements.txt` if adding dependencies

**Mobile:**
- Create screen in `flutter_app/lib/screens/`
- Add route in `flutter_app/lib/main.dart`
- Update `flutter_app/pubspec.yaml` for new packages

---

## 📦 Key Dependencies

### Python Backend
```
Flask==2.3.2
torch==2.0.1
torchvision==0.15.2
timm==0.9.12
Pillow==9.5.0
numpy>=1.24.0
opencv-python>=4.8.0
python-dotenv>=1.0.0
requests>=2.31.0
```

**Note:** The project uses Groq API for AI chat features. Get a free API key at https://console.groq.com/

### Flutter Mobile
```yaml
camera: ^0.10.5+5           # Camera access
image_picker: ^1.0.4        # Image selection
model_viewer_plus: ^1.7.2   # 3D model viewer
webview_flutter: ^4.4.2     # WebView support
provider: ^6.1.1            # State management
http: ^1.1.0                # HTTP requests
```

---

## 🎯 Quick Test Workflow

### 1. Start Backend
```powershell
cd E:\projects\major_project
python app.py
# Wait for "Running on http://0.0.0.0:5000"
```

### 2. Get IP Address
```powershell
ipconfig
# Note your IPv4 (e.g., 192.168.1.100)
```

### 3. Run Mobile App
```powershell
cd flutter_app
flutter run
```

### 4. Configure Connection
1. Open app Settings
2. Enter: `http://192.168.1.100:5000`
3. Tap "Test Connection" → ✅

### 5. Test Features
1. **Camera**: Capture → See classification
2. **Voice**: Record + Capture → See transcript
3. **3D**: Capture 10+ images → Build → View
4. **Logs**: Check all captured data

---

## 📝 Important Notes

### Python Version Compatibility
- ✅ **Python 3.10**: Fully tested and working
- ✅ **Python 3.11**: Works well
- ⚠️ **Python 3.12**: May have issues
- ❌ **Python 3.13**: Not compatible with current PyTorch

### APK Build Success
The Flutter build warnings about Kotlin caches are **normal** and can be ignored. As long as you see:
```
√ Built build\app\outputs\flutter-apk\app-release.apk (49.2MB)
```
Your APK is ready! ✅

### 3D Model Formats
- **Generated by app**: `.ply` (point cloud)
- **Viewable in app**: `.glb` or `.gltf`
- **Convert PLY to GLB**: Use Blender or online tools
  - Blender: https://www.blender.org/
  - Online: https://products.aspose.app/3d/conversion/ply-to-glb

---

## 🌟 What's New

### Latest Updates
- ✅ Fixed Flutter build errors (model_viewer_plus compatibility)
- ✅ Added comprehensive 3D model viewer with AR support
- ✅ Integrated 3D reconstruction workflow
- ✅ Cleaned up documentation (single README approach)
- ✅ Added PyTorch error fix guide
- ✅ Improved mobile app UI/UX
- ✅ Enhanced error handling and loading states

---

## 📞 Support

### Documentation Files
- **This File**: Complete project overview
- **`flutter_app/README.md`**: Detailed mobile app guide
- **`FIX_PYTORCH_ERROR.md`**: PyTorch troubleshooting

### Resources
- **Flutter**: https://flutter.dev/docs
- **PyTorch**: https://pytorch.org/docs
- **model_viewer_plus**: https://pub.dev/packages/model_viewer_plus
- **COLMAP**: https://colmap.github.io/

### Free 3D Models for Testing
- Sketchfab: https://sketchfab.com/
- Poly Haven: https://polyhaven.com/models
- Model Viewer: https://modelviewer.dev/shared-assets/models/

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎉 You're Ready!

**To run the complete system:**

1. **Fix PyTorch**: Install VC++ Redistributables or use Python 3.10
2. **Start backend**: `python app.py`
3. **Build app**: `cd flutter_app && flutter build apk --release`
4. **Configure**: Set server URL in app Settings
5. **Start monitoring!** 🚀

---

**Status**: ✅ Production Ready  
**Last Updated**: November 2025  
**Flutter APK**: 49.2 MB (Release Build)  
**Backend**: Flask + PyTorch  
**Mobile**: Flutter 3.0+

**Need help?** Check the troubleshooting sections above or see the detailed documentation files.
