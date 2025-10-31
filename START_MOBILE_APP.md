# 🚀 Quick Start - Mobile App

## Start the Server

```bash
python mobile_api_server.py
```

You'll see:
```
🏗️ SiteLenz Mobile API Server
================================
✅ Server running on: http://0.0.0.0:5000
✅ Access from mobile: http://YOUR_IP:5000
```

## Access from Your Phone

### Step 1: Find Your Computer's IP Address

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter (e.g., `192.168.1.100`)

**Mac/Linux:**
```bash
ifconfig
```

### Step 2: Connect Your Phone

Make sure your phone is on the **same WiFi network** as your computer.

### Step 3: Open on Phone

Open your phone browser and visit:
```
http://YOUR_IP:5000
```
Example: `http://192.168.1.100:5000`

### Step 4: Install as App

**Android (Chrome):**
1. Tap menu (⋮) → "Add to Home screen"
2. Name it "SiteLenz"
3. Tap "Add"

**iOS (Safari):**
1. Tap Share button
2. Scroll down and tap "Add to Home Screen"
3. Name it "SiteLenz"
4. Tap "Add"

## Features

✅ Real-time camera classification
✅ Audio recording & transcription
✅ Mobile-optimized interface
✅ Works offline (PWA)
✅ All desktop features

## Troubleshooting

**Can't connect from phone?**
- Check both devices on same WiFi
- Windows: Allow port 5000 through firewall
- Try `http://` not `https://`

**Camera not working?**
- Grant camera permission when prompted
- Check Settings → Browser → Permissions

**No audio transcription?**
- Grant microphone permission
- Check internet connection (Google Speech API needs internet)

---

For complete documentation, see **MOBILE_APP_GUIDE.md**
