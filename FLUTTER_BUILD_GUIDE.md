# Flutter APK Build Instructions

## Current Status
✅ Flutter installed (3.35.7)
✅ Flutter app created with all dependencies
✅ Android permissions configured (CAMERA, RECORD_AUDIO, INTERNET)
⏳ Installing Android Studio (in progress...)

## What's Happening Now
Android Studio is being downloaded and installed (1.3GB). This includes:
- Android SDK
- Android NDK
- Build tools
- Platform tools

## After Android Studio Installation

### Step 1: Complete Android Studio Setup
1. **Launch Android Studio** (will open automatically after install)
2. **Follow the setup wizard:**
   - Accept licenses
   - Choose "Standard" installation
   - Download Android SDK components (this takes 10-15 minutes)
3. **Close Android Studio** when setup completes

### Step 2: Accept Android Licenses
Open PowerShell and run:
```powershell
cd E:\projects\major_project\flutter_app
E:\Softwares\flutter\bin\flutter doctor --android-licenses
```
Press 'y' to accept all licenses.

### Step 3: Verify Flutter Setup
```powershell
E:\Softwares\flutter\bin\flutter doctor -v
```
You should see:
- ✅ Flutter
- ✅ Android toolchain
- ✅ VS Code

### Step 4: Build the APK
```powershell
cd E:\projects\major_project\flutter_app
E:\Softwares\flutter\bin\flutter build apk --release
```

Build takes 5-10 minutes on first run.

### Step 5: Get Your APK
After successful build:
```powershell
# APK location:
E:\projects\major_project\flutter_app\build\app\outputs\flutter-apk\app-release.apk

# Copy to project root for easy access:
Copy-Item "build\app\outputs\flutter-apk\app-release.apk" -Destination "E:\projects\major_project\SiteLenz.apk"
```

## Testing Options

### Option A: Test on Real Device
1. **Enable Developer Mode** on your Android phone:
   - Settings → About Phone → Tap "Build Number" 7 times
   - Settings → Developer Options → Enable "USB Debugging"
2. **Connect phone via USB**
3. **Run:**
   ```powershell
   cd E:\projects\major_project\flutter_app
   E:\Softwares\flutter\bin\flutter devices  # Should show your phone
   E:\Softwares\flutter\bin\flutter run --release
   ```

### Option B: Test on Emulator
1. **Open Android Studio**
2. **Tools → Device Manager → Create Virtual Device**
3. **Choose Pixel 6 Pro → Next → Download System Image (Android 13) → Finish**
4. **Launch emulator**
5. **Run:**
   ```powershell
   cd E:\projects\major_project\flutter_app
   E:\Softwares\flutter\bin\flutter run --release
   ```

## App Features (Voice-Triggered Capture)

Your Flutter app includes:
1. **Voice + Image Tab**: 
   - Tap microphone to record voice
   - Automatically captures image when you stop speaking
   - Sends both to server for analysis
   - Displays classification result

2. **Camera Tab**: 
   - Manual image capture
   - Real-time classification

3. **Logs Tab**: 
   - View all voice + image captures
   - See timestamps and results

4. **Settings Tab**: 
   - Change server IP if needed
   - Default: http://10.211.181.132:5000

## Troubleshooting

### "Unable to locate Android SDK"
- Wait for Android Studio installation to complete
- Run Android Studio setup wizard
- Run: `flutter doctor --android-licenses`

### "Gradle build failed"
- Ensure internet connection is stable
- First build downloads ~500MB of dependencies
- Try again: `flutter clean && flutter build apk --release`

### "No devices found"
- Enable USB debugging on phone
- Install device drivers (Windows may auto-install)
- Or use emulator from Android Studio

### Build takes forever
- First build: 5-10 minutes (normal)
- Subsequent builds: 1-2 minutes
- Uses Gradle caching

## Quick Commands Reference

```powershell
# Navigate to project
cd E:\projects\major_project\flutter_app

# Check setup
E:\Softwares\flutter\bin\flutter doctor

# Get dependencies
E:\Softwares\flutter\bin\flutter pub get

# Build APK
E:\Softwares\flutter\bin\flutter build apk --release

# Run on device
E:\Softwares\flutter\bin\flutter run --release

# Clean build cache
E:\Softwares\flutter\bin\flutter clean

# List connected devices
E:\Softwares\flutter\bin\flutter devices
```

## What Happens Next

I'm installing Android Studio now. When it completes:
1. Launch Android Studio and complete setup
2. I'll run the license acceptance command
3. I'll build the APK
4. You'll have SiteLenz.apk ready to install on your phone!

**Estimated time remaining: 10-20 minutes** (download + setup + build)
