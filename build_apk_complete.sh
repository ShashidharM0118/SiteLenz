#!/bin/bash
# Complete APK Build Script - Just copy and paste this entire script into Ubuntu terminal

set -e  # Exit on any error

echo "=========================================="
echo "🚀 SiteLenz APK Builder"
echo "=========================================="
echo ""

# Navigate to project
echo "📂 Navigating to project directory..."
cd /mnt/e/projects/major_project || { echo "❌ Failed to navigate to project"; exit 1; }

# Update system
echo ""
echo "📦 Updating system packages..."
sudo apt-get update -qq

# Install dependencies
echo ""
echo "🔧 Installing build dependencies (this may take a few minutes)..."
sudo apt-get install -y \
    python3-pip \
    openjdk-17-jdk \
    git \
    zip \
    unzip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential \
    ccache \
    libltdl-dev

# Install Python build tools
echo ""
echo "🐍 Installing Python build tools..."
pip3 install --upgrade pip setuptools wheel
pip3 install buildozer cython==0.29.33

# Add pip to PATH
export PATH="$HOME/.local/bin:$PATH"

# Prepare main.py
echo ""
echo "📝 Preparing application files..."
cp mobile_kivy_app_lite.py main.py

# Clean previous builds
echo ""
echo "🧹 Cleaning previous builds..."
rm -rf .buildozer bin

# Accept Android licenses
echo ""
echo "📱 Setting up Android build environment..."
mkdir -p ~/.buildozer/android/platform/android-sdk/licenses
echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > ~/.buildozer/android/platform/android-sdk/licenses/android-sdk-license

# Build APK
echo ""
echo "🔨 Building APK (this will take 15-30 minutes on first build)..."
echo "⏳ Please be patient, downloading Android SDK/NDK and compiling..."
echo ""
buildozer -v android debug

# Check result
echo ""
echo "=========================================="
if [ -f "bin/"*.apk ]; then
    echo "✅ SUCCESS! APK built successfully!"
    echo ""
    echo "📱 APK Details:"
    ls -lh bin/*.apk
    echo ""
    echo "📍 Location: $(pwd)/bin/"
    echo ""
    echo "🎉 You can now transfer the APK to your Android device!"
    echo "=========================================="
else
    echo "❌ Build failed. Please check the logs above."
    echo "=========================================="
    exit 1
fi
