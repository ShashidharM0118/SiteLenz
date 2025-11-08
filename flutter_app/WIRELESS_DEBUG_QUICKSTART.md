# 📱 Wireless Debugging - Quick Start

## 🚀 First Time Setup (5 minutes)

### On Your Phone:
1. **Settings** → **About Phone** → Tap **Build Number** 7 times
2. **Settings** → **System** → **Developer Options** → Enable **USB Debugging**
3. Connect USB cable to computer

### On Your Computer:
```powershell
# Run the automated setup script
cd e:\projects\major_project\flutter_app
.\setup_wireless.ps1
```

**That's it!** Follow the prompts and disconnect USB when asked.

---

## 💨 Daily Use (30 seconds)

```powershell
# Option 1: Use quick connect script (after first setup)
.\quick_connect.ps1

# Option 2: Manual connect
adb connect YOUR_IP:5555

# Then run your app
flutter run
```

---

## 📋 Manual Setup (if script doesn't work)

```powershell
# 1. Connect USB cable
adb devices

# 2. Enable wireless mode
adb tcpip 5555

# 3. Find phone IP (Settings → About → Status → IP Address)

# 4. Disconnect USB cable

# 5. Connect wirelessly (replace with your IP)
adb connect 192.168.1.XXX:5555

# 6. Verify
adb devices

# 7. Run app
flutter run
```

---

## 🔧 Common Commands

| Action | Command |
|--------|---------|
| Connect | `adb connect IP:5555` |
| Disconnect | `adb disconnect IP:5555` |
| List devices | `adb devices` |
| Flutter devices | `flutter devices` |
| Run app | `flutter run` |
| Restart ADB | `adb kill-server && adb start-server` |

---

## ❌ Troubleshooting

**Can't connect?**
```powershell
adb kill-server
adb start-server
adb connect YOUR_IP:5555
```

**Device offline?**
```powershell
adb disconnect
adb connect YOUR_IP:5555
```

**Connection drops frequently?**
- Settings → Battery → Battery Optimization → Wireless Debugging → Don't optimize
- Use 5GHz Wi-Fi if available

---

## ✅ Requirements Checklist

- [ ] Both devices on same Wi-Fi network
- [ ] Developer Options enabled on phone
- [ ] USB Debugging enabled
- [ ] Phone IP address known
- [ ] ADB installed on computer

---

**Need detailed help?** See `WIRELESS_DEBUGGING_GUIDE.md`
