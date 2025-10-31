# 📱 How to Build Android APK for SiteLenz

## ⚠️ Important Note

Building Android APK from Python requires **Linux** (Ubuntu recommended) because Buildozer doesn't work on Windows. Here are your options:

---

## 🎯 Option 1: Use WSL2 (Windows Subsystem for Linux) - RECOMMENDED

This is the **easiest way** if you're on Windows.

### Step 1: Install WSL2

```powershell
# In PowerShell (as Administrator)
wsl --install -d Ubuntu
```

Restart your computer.

### Step 2: Setup in WSL2

```bash
# Open Ubuntu terminal
cd /mnt/e/projects/major_project

# Install dependencies
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk wget

# Install Buildozer
pip3 install buildozer cython

# Install Android build tools
buildozer android debug
```

### Step 3: Build APK

```bash
# Copy model file to accessible location
mkdir -p models
cp /mnt/e/projects/major_project/models/vit_weights.pth models/

# Build APK
buildozer android debug

# APK will be in: bin/sitelenz-1.0-arm64-v8a-debug.apk
```

### Step 4: Install on Phone

```bash
# Transfer APK to phone via USB or cloud
# Then install it on your Android phone
```

---

## 🎯 Option 2: Use GitHub Actions (Cloud Build) - EASIEST

Let GitHub build the APK for you automatically!

### Step 1: Create GitHub Actions Workflow

I'll create this file for you:

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y git zip unzip openjdk-17-jdk wget
        pip install buildozer cython
    
    - name: Build APK
      run: |
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: sitelenz-apk
        path: bin/*.apk
```

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Add Android APK build support"
git push
```

### Step 3: Download APK

1. Go to GitHub → Actions tab
2. Click on the latest workflow run
3. Download the APK from artifacts
4. Install on your phone

---

## 🎯 Option 3: Use Google Colab (Free Cloud Build)

### Step 1: Open Google Colab

Go to: https://colab.research.google.com/

### Step 2: Run Build Script

```python
# Install Buildozer
!pip install buildozer cython

# Clone your repository
!git clone https://github.com/ShashidharM0118/SiteLenz.git
%cd SiteLenz

# Install system dependencies
!sudo apt update
!sudo apt install -y git zip unzip openjdk-17-jdk wget

# Build APK
!buildozer android debug

# Download APK
from google.colab import files
files.download('bin/sitelenz-1.0-arm64-v8a-debug.apk')
```

---

## 🎯 Option 4: Simplified Web App (PWA) - CURRENT SOLUTION

The **easiest solution** that works NOW:

### Already Created! ✅

You already have a working Progressive Web App that:
- Works on ANY Android/iOS phone
- Installable from browser (looks like native app)
- No APK needed
- All features working

### How to Use:

1. **Phone browser:** Visit `http://10.211.181.132:5000`
2. **Install:** Chrome menu → "Add to Home screen"
3. **Use:** Opens like a native app!

**This is the recommended solution** because:
- ✅ Works NOW (no build required)
- ✅ Cross-platform (Android + iOS)
- ✅ No app store needed
- ✅ Easy updates (just refresh)
- ✅ Same features as APK

---

## 📦 What's Included for APK Build

I've created:

1. **mobile_kivy_app.py** - Kivy-based mobile app (for APK)
2. **buildozer.spec** - Build configuration
3. **This guide** - Build instructions

### Files Structure:

```
major_project/
├── mobile_kivy_app.py      # Kivy mobile app
├── buildozer.spec          # Build config
├── models/
│   └── vit_weights.pth     # ViT model (327 MB)
└── BUILD_APK_GUIDE.md      # This file
```

---

## ⚙️ Build Process Explained

### What Buildozer Does:

1. **Downloads Android SDK** (~500 MB)
2. **Downloads Android NDK** (~1 GB)
3. **Compiles Python** for Android
4. **Packages app** with all dependencies
5. **Creates APK** (~200 MB with model)

### Build Time:
- First build: **30-60 minutes** (downloads everything)
- Subsequent builds: **5-10 minutes**

### APK Size:
- With ViT model: **~200 MB**
- Without model: **~50 MB**

---

## 🚀 Recommended Approach

### For Quick Testing → Use PWA (Current Solution)

✅ **Already working**
✅ **No build needed**
✅ **Works on any phone**

Server running at: `http://10.211.181.132:5000`

### For App Store Distribution → Build APK

📱 **Use GitHub Actions** (easiest)
🐧 **Or use WSL2** (local build)

---

## 🔧 Troubleshooting APK Build

### Error: "Command failed: buildozer"

**Solution:**
```bash
# Install Java
sudo apt install openjdk-17-jdk

# Update Buildozer
pip install --upgrade buildozer
```

### Error: "NDK not found"

**Solution:**
```bash
buildozer android clean
buildozer android debug
```

### Error: "APK too large"

**Solution:** Remove model from APK, download it on first run:

```python
# In mobile_kivy_app.py
import requests

def download_model():
    url = "http://YOUR_SERVER/models/vit_weights.pth"
    response = requests.get(url)
    with open('vit_weights.pth', 'wb') as f:
        f.write(response.content)
```

---

## 📱 Installing APK on Phone

### Method 1: USB Transfer

```bash
# Connect phone via USB
adb install bin/sitelenz-1.0-arm64-v8a-debug.apk
```

### Method 2: Cloud Transfer

1. Upload APK to Google Drive / Dropbox
2. Download on phone
3. Install (may need to enable "Install from Unknown Sources")

### Method 3: Direct Download

Host APK on your server:
```bash
# On server
python -m http.server 8000

# On phone browser
http://YOUR_IP:8000/bin/sitelenz-1.0-arm64-v8a-debug.apk
```

---

## 🎊 Summary

### Quick Start (PWA - Already Working):
```
✅ Server running: http://10.211.181.132:5000
✅ Open on phone browser
✅ Install to home screen
✅ Start using!
```

### Build APK (If Needed):
```
1. Use GitHub Actions (easiest)
   OR
2. Use WSL2 on Windows
   OR
3. Use Google Colab

Build command: buildozer android debug
Result: bin/sitelenz-1.0-arm64-v8a-debug.apk
```

### My Recommendation:

🎯 **Keep using the PWA** (current solution) because:
- It's already working
- No complex build process
- Works on all phones
- Easy to update
- Same features as APK

Build APK only if you need:
- Offline operation without server
- Faster performance
- Google Play Store distribution

---

**The PWA is ready NOW. APK build requires Linux environment (WSL2/GitHub Actions/Colab).**
