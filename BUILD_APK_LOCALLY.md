# Build APK Locally (Recommended)

Since GitHub Actions keeps failing due to resource constraints, here's how to build the APK on a Linux machine or using WSL:

## Option 1: Use WSL (Windows Subsystem for Linux)

### Step 1: Install WSL
```powershell
wsl --install -d Ubuntu
```

### Step 2: Open WSL and navigate to project
```bash
cd /mnt/e/projects/major_project
```

### Step 3: Install dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-pip openjdk-17-jdk git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev cmake libffi-dev libssl-dev

pip3 install buildozer cython==0.29.33
```

### Step 4: Build APK
```bash
# Copy the lite version
cp mobile_kivy_app_lite.py main.py

# Build
buildozer -v android debug

# APK will be in bin/ folder
ls -lh bin/*.apk
```

### Step 5: Copy APK back to Windows
```bash
cp bin/*.apk /mnt/e/projects/major_project/
```

## Option 2: Use Online Build Service

### Expo/Appetize Alternative
Since Kivy builds are complex, consider using the **PWA (Progressive Web App)** which is already working:

1. **On Android Chrome**: Open `http://YOUR_SERVER_IP:5000`
2. **Tap menu** → "Add to Home Screen"
3. **Install** - Acts like a native app!

**Benefits:**
- No build needed
- Instant updates
- Works on both Android & iOS
- Already implemented and working

## Option 3: Pre-built APK Services

### Use these services to build from GitHub:
1. **Appetize.io** - Upload project, get APK
2. **BuildBot** - CI/CD for mobile apps
3. **CircleCI** - Better resources than GitHub Actions

## Quick Solution: Use PWA

Your mobile app is already accessible at:
- **http://localhost:5000** (same device)
- **http://10.211.181.132:5000** (from phone on same network)

Just open in Chrome and "Add to Home Screen" - works like an app! ✅
