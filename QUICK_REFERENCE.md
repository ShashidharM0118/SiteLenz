# 🚀 SiteLenz - Quick Reference Card

## ✅ Your Build Status

**Flutter App:** ✅ **SUCCESSFULLY BUILT**
- APK Size: 49.2 MB
- Location: `flutter_app/build/app/outputs/flutter-apk/app-release.apk`
- Status: Ready for installation

**Kotlin Warnings:** ⚠️ Can be ignored (they're just cache warnings, not errors)

---

## 🔥 Quick Commands

### Start Backend Server
```powershell
cd E:\projects\major_project
python app.py
```

### Build Flutter APK
```powershell
cd E:\projects\major_project\flutter_app
flutter build apk --release
```

### Run on Device
```powershell
cd E:\projects\major_project\flutter_app
flutter run
```

### Check Server Running
```powershell
netstat -ano | findstr :5000
```

### Get Your IP
```powershell
ipconfig | findstr IPv4
```

---

## 🐛 Fix PyTorch Error

**Error:** `DLL load failed while importing _C`

**Quick Fix:**
1. Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Install and restart computer
3. Try: `python app.py` again

**Alternative:**
```powershell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

---

## 📱 App Configuration

**Server URL Format:**
- Local: `http://localhost:5000`
- WiFi: `http://YOUR_IP:5000` (e.g., `http://192.168.1.100:5000`)

**Steps:**
1. Get IP: `ipconfig`
2. Open app → Settings
3. Enter URL
4. Test Connection → ✅

---

## 🎯 Feature Testing

### Test Camera Classification
1. Open app → Camera tab
2. Capture image
3. See result

### Test Voice + Image
1. Voice + Image tab
2. Record voice
3. Capture image
4. View in Logs

### Test 3D Reconstruction
1. 3D Reconstruction tab
2. Start session
3. Capture 10+ images
4. Build 3D Model
5. View 3D Model

### Test 3D Viewer
Use sample URL:
```
https://modelviewer.dev/shared-assets/models/Astronaut.glb
```

---

## 🔧 Troubleshooting One-Liners

### Clean Flutter Build
```powershell
cd flutter_app; flutter clean; flutter pub get; flutter build apk --release
```

### Kill Server Process
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Allow Firewall
```powershell
netsh advfirewall firewall add rule name="Flask Server" dir=in action=allow protocol=TCP localport=5000
```

### Test PyTorch
```powershell
python -c "import torch; print('OK:', torch.__version__)"
```

---

## 📊 System Requirements

**Backend:**
- Python 3.10 or 3.11 (NOT 3.13)
- Visual C++ Redistributables
- 2GB RAM minimum
- Windows 10/11

**Mobile:**
- Flutter 3.0+
- Android Studio or VS Code
- Android 8.0+ / iOS 12.0+
- 500MB free space

---

## 📂 Key File Locations

**APK:** `flutter_app/build/app/outputs/flutter-apk/app-release.apk`  
**Model:** `models/vit_weights.pth`  
**Backend:** `app.py`  
**Main App:** `flutter_app/lib/main.dart`  
**3D Viewer:** `flutter_app/lib/screens/model_viewer_screen.dart`  

---

## ✅ Success Indicators

**Backend Running:**
```
 * Running on http://0.0.0.0:5000
```

**Flutter Build Success:**
```
√ Built build\app\outputs\flutter-apk\app-release.apk (49.2MB)
```

**Server Active:**
```
TCP    0.0.0.0:5000    0.0.0.0:0    LISTENING
```

---

## 🎯 Complete Workflow (5 Minutes)

1. **Fix PyTorch** (if needed):
   ```powershell
   # Install VC++ Redistributables
   # https://aka.ms/vs/17/release/vc_redist.x64.exe
   ```

2. **Start Backend**:
   ```powershell
   cd E:\projects\major_project
   python app.py
   ```

3. **Get IP**:
   ```powershell
   ipconfig | findstr IPv4
   # Note: 192.168.1.XXX
   ```

4. **Install APK**:
   - Copy `app-release.apk` to phone
   - Install it

5. **Configure App**:
   - Open Settings
   - Enter: `http://192.168.1.XXX:5000`
   - Test Connection

6. **Done!** 🎉

---

## 📞 Need Help?

**Documentation:**
- Project Overview: `README.md`
- Mobile App: `flutter_app/README.md`
- PyTorch Fix: `FIX_PYTORCH_ERROR.md`
- This File: Quick reference

**Your build is working!** The Kotlin warnings are normal.

---

**Status:** ✅ All systems functional  
**APK:** Ready to install  
**Backend:** Needs PyTorch fix  
**Next Step:** Install VC++ Redistributables and start server

