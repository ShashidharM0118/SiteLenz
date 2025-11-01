#!/bin/bash
# APK Build Script for Ubuntu/WSL

echo "=========================================="
echo "SiteLenz APK Build Script"
echo "=========================================="

# Step 1: Update system
echo "Step 1: Updating system packages..."
sudo apt-get update

# Step 2: Install dependencies
echo "Step 2: Installing build dependencies..."
sudo apt-get install -y python3-pip openjdk-17-jdk git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev cmake libffi-dev libssl-dev

# Step 3: Install Python build tools
echo "Step 3: Installing Python build tools..."
pip3 install --upgrade pip
pip3 install buildozer cython==0.29.33

# Step 4: Navigate to project
echo "Step 4: Navigating to project directory..."
cd /mnt/e/projects/major_project

# Step 5: Copy lite version as main.py
echo "Step 5: Preparing main.py..."
cp mobile_kivy_app_lite.py main.py

# Step 6: Clean previous builds
echo "Step 6: Cleaning previous builds..."
rm -rf .buildozer bin

# Step 7: Build APK
echo "Step 7: Building APK (this may take 15-30 minutes)..."
buildozer -v android debug

# Step 8: Check if APK was created
echo "Step 8: Checking build output..."
if [ -f "bin/sitelenzlite-0.1-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    echo "=========================================="
    echo "✅ SUCCESS! APK built successfully!"
    echo "APK Location: bin/sitelenzlite-0.1-arm64-v8a_armeabi-v7a-debug.apk"
    ls -lh bin/*.apk
    echo "=========================================="
else
    echo "=========================================="
    echo "❌ Build failed. Check logs above for errors."
    echo "=========================================="
fi
