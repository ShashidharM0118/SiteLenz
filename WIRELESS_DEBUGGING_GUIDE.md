# 📱 Wireless Debugging Guide for Flutter

## 🎯 Quick Setup (Recommended Method)

### Method 1: Using ADB Wireless (Android 11+)

#### Step 1: Enable Developer Options on Your Phone
1. Open **Settings** on your Android device
2. Go to **About Phone**
3. Tap **Build Number** 7 times (you'll see "You are now a developer!")
4. Go back to **Settings** → **System** → **Developer Options**

#### Step 2: Enable Wireless Debugging
1. In **Developer Options**, find **Wireless Debugging**
2. Toggle it **ON**
3. Tap on **Wireless Debugging** to see the IP address and port

#### Step 3: Connect from Your Computer

**Initial Setup (USB required once):**
```powershell
# 1. Connect phone via USB cable first
adb devices

# 2. Enable TCP/IP mode on port 5555
adb tcpip 5555

# 3. Find your phone's IP address
# Go to Settings → About Phone → Status → IP Address
# OR use this command:
adb shell ip addr show wlan0

# 4. Disconnect USB cable

# 5. Connect wirelessly (replace with your phone's IP)
adb connect 192.168.1.XXX:5555

# 6. Verify connection
adb devices
```

#### Step 4: Run Flutter App Wirelessly
```powershell
# Navigate to your project
cd e:\projects\major_project\flutter_app

# List devices
flutter devices

# Run on wireless device
flutter run
```

---

## 🚀 Method 2: Pairing Method (Android 11+ - No USB Required After First Setup)

#### Step 1: On Your Phone
1. **Settings** → **Developer Options** → **Wireless Debugging**
2. Tap **Pair device with pairing code**
3. Note the **IP address**, **Port**, and **Pairing Code**

#### Step 2: On Your Computer
```powershell
# Pair with the device (use the IP and port from your phone)
adb pair 192.168.1.XXX:XXXXX

# Enter the pairing code when prompted

# After pairing, connect using the main wireless debugging port (usually port 5555)
adb connect 192.168.1.XXX:5555

# Verify
adb devices
```

---

## 🔧 Method 3: Using Android Studio (Easiest)

#### Step 1: Setup
1. Connect phone via USB
2. Open Android Studio
3. Go to **Run** → **Select Device** → **Pair Devices Using Wi-Fi**
4. Follow the on-screen instructions

#### Step 2: In VS Code
```powershell
# The device will now appear in Flutter devices
flutter devices
flutter run
```

---

## 📝 Quick Commands Reference

### Check Connected Devices
```powershell
adb devices
flutter devices
```

### Connect to Device
```powershell
# Replace IP_ADDRESS with your phone's IP
adb connect IP_ADDRESS:5555
```

### Disconnect
```powershell
adb disconnect IP_ADDRESS:5555
```

### Restart ADB (if issues occur)
```powershell
adb kill-server
adb start-server
```

### Find Device IP Address (via ADB)
```powershell
adb shell ip addr show wlan0
```

---

## 🛠️ Complete Setup Script (PowerShell)

Save this as `setup_wireless.ps1`:

```powershell
# Wireless Debugging Setup Script for Flutter

Write-Host "=== Flutter Wireless Debugging Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if device is connected via USB
Write-Host "Step 1: Checking for USB-connected devices..." -ForegroundColor Yellow
adb devices
Write-Host ""

# Step 2: Enable TCP/IP
Write-Host "Step 2: Enabling TCP/IP on port 5555..." -ForegroundColor Yellow
adb tcpip 5555
Start-Sleep -Seconds 2
Write-Host ""

# Step 3: Get device IP
Write-Host "Step 3: Getting device IP address..." -ForegroundColor Yellow
$ip = adb shell ip addr show wlan0 | Select-String -Pattern "inet\s+(\d+\.\d+\.\d+\.\d+)" | ForEach-Object { $_.Matches.Groups[1].Value }
Write-Host "Device IP: $ip" -ForegroundColor Green
Write-Host ""

# Step 4: Instructions
Write-Host "Step 4: Please disconnect USB cable now" -ForegroundColor Yellow
Read-Host "Press Enter when ready"
Write-Host ""

# Step 5: Connect wirelessly
Write-Host "Step 5: Connecting wirelessly..." -ForegroundColor Yellow
adb connect "$ip:5555"
Start-Sleep -Seconds 2
Write-Host ""

# Step 6: Verify
Write-Host "Step 6: Verifying connection..." -ForegroundColor Yellow
adb devices
flutter devices
Write-Host ""

Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host "You can now run: flutter run" -ForegroundColor Green
```

---

## 🔍 Troubleshooting

### Issue: "unable to connect to IP_ADDRESS:5555"

**Solutions:**
```powershell
# 1. Restart ADB
adb kill-server
adb start-server

# 2. Re-enable TCP/IP (connect USB first)
adb tcpip 5555

# 3. Check if firewall is blocking
# Windows: Allow ADB through Windows Firewall

# 4. Verify both devices are on same Wi-Fi network
```

### Issue: Device not showing in `flutter devices`

**Solutions:**
```powershell
# 1. Check ADB can see it
adb devices

# 2. Restart Flutter daemon
flutter daemon --stop
flutter devices

# 3. Hot restart VS Code
```

### Issue: Connection keeps dropping

**Solutions:**
1. **Disable Battery Optimization** for Wireless Debugging
   - Settings → Battery → Battery Optimization → All apps
   - Find "Wireless Debugging" → Don't optimize
   
2. **Keep Wi-Fi awake**
   - Settings → Developer Options → Stay awake (enable)

3. **Use 5GHz Wi-Fi** if available (more stable)

### Issue: "device offline"

**Solutions:**
```powershell
# Reconnect
adb disconnect
adb connect IP_ADDRESS:5555

# If that doesn't work, restart from USB
adb usb
adb tcpip 5555
adb connect IP_ADDRESS:5555
```

---

## 💡 Pro Tips

### 1. Create a Batch File for Quick Connection

Create `connect_phone.bat`:
```batch
@echo off
adb connect 192.168.1.XXX:5555
adb devices
flutter devices
pause
```

### 2. Add to VS Code Tasks

`.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Connect Phone Wirelessly",
      "type": "shell",
      "command": "adb connect 192.168.1.XXX:5555",
      "problemMatcher": []
    }
  ]
}
```

### 3. Save Your Device IP

Add to your `.env` file:
```env
PHONE_IP=192.168.1.XXX
```

### 4. Faster Development

```powershell
# Hot reload is faster over Wi-Fi than rebuilding
# Use 'r' in terminal for hot reload
# Use 'R' for hot restart
```

---

## 🎬 Step-by-Step Video Tutorial Equivalent

### First Time Setup (5 minutes):

1. **Connect USB cable** to your phone
2. **Open PowerShell** in your project directory
3. Run: `adb devices` (verify device shows)
4. Run: `adb tcpip 5555`
5. **Find IP**: Settings → About → Status → IP Address
6. **Disconnect USB cable**
7. Run: `adb connect YOUR_IP:5555`
8. Run: `flutter run`

### Daily Use (30 seconds):

1. **Open PowerShell**
2. Run: `adb connect YOUR_IP:5555`
3. Run: `flutter run`

---

## 📱 Supported Devices

- ✅ Android 11 and above (native wireless debugging)
- ✅ Android 10 and below (via `adb tcpip` method)
- ❌ iOS (requires Xcode Wireless Debugging - macOS only)

---

## 🔒 Security Notes

- Wireless debugging is only available on **trusted Wi-Fi networks**
- Disable when not in use to prevent unauthorized access
- ADB connections are not encrypted by default
- Use on **private home/office networks only**

---

## 🆘 Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `device offline` | Connection interrupted | Reconnect: `adb connect IP:5555` |
| `no devices/emulators found` | Not connected | Run `adb connect` again |
| `unable to connect` | Wrong IP or firewall | Check IP, disable firewall |
| `device unauthorized` | Not authorized on phone | Allow USB debugging prompt |
| `multiple devices` | Multiple phones connected | Specify device: `flutter run -d device_id` |

---

## ✅ Verification Checklist

- [ ] Developer Options enabled
- [ ] Wireless Debugging enabled (Android 11+) OR USB debugging enabled
- [ ] Phone and computer on same Wi-Fi network
- [ ] ADB installed (`adb version` works)
- [ ] Phone IP address known
- [ ] `adb devices` shows device
- [ ] `flutter devices` shows device
- [ ] Can run `flutter run` successfully

---

## 🎯 Your Specific Setup

Based on your project at `e:\projects\major_project\flutter_app`:

```powershell
# 1. Navigate to project
cd e:\projects\major_project\flutter_app

# 2. Connect phone (replace with your IP)
adb connect 192.168.1.XXX:5555

# 3. Run app
flutter run

# 4. For hot reload during development
# Press 'r' in the terminal
```

---

**Ready to start wireless debugging!** 🚀

For more help, see:
- [Official Android Docs](https://developer.android.com/studio/command-line/adb#wireless)
- [Flutter Docs](https://docs.flutter.dev/get-started/install/windows)
