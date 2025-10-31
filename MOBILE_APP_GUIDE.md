# 📱 SiteLenz Mobile App - Complete Guide

## ✨ What You Got

A **Progressive Web App (PWA)** that works on any mobile device (Android & iOS) with:

✅ **Native-like Experience** - Installable on home screen
✅ **Camera Access** - Real-time defect classification  
✅ **Audio Recording** - Speech-to-text transcription  
✅ **Offline Support** - PWA caching  
✅ **Beautiful UI** - Mobile-optimized design  
✅ **All Features** - Same as desktop app  

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_mobile.txt
```

### 2. Start the Server

```bash
python mobile_api_server.py
```

You'll see:
```
🏗️ SiteLenz Mobile API Server
Starting server...
Mobile App: http://localhost:5000
```

### 3. Access from Mobile

**Option A: Same WiFi Network**
1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   # Look for "IPv4 Address" (e.g., 192.168.1.100)
   ```

2. On your phone browser, visit:
   ```
   http://YOUR_IP:5000
   # Example: http://192.168.1.100:5000
   ```

**Option B: USB Tethering/Hotspot**
1. Enable hotspot on phone
2. Connect computer to phone's WiFi
3. Visit `http://localhost:5000` on phone

**Option C: Deploy to Cloud** (for internet access)
- Deploy on Heroku, AWS, or ngrok
- Access from anywhere

---

## 📱 Install as App

### Android
1. Open the URL in Chrome
2. Tap the **menu (⋮)** → **"Add to Home screen"**
3. App icon appears on home screen
4. Opens like a native app!

### iOS
1. Open the URL in Safari
2. Tap the **Share button** → **"Add to Home Screen"**
3. App icon appears on home screen
4. Opens like a native app!

---

## 🎯 How to Use

### Home Screen Layout

```
┌─────────────────────────────────────┐
│      🏗️ SiteLenz Monitor           │
├─────────────────────────────────────┤
│                                     │
│  📸 Camera Feed                     │
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │    [Live Camera View]       │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│  Latest: Major Crack (92.3%)       │
│                                     │
│  🎤 Audio Recording                │
│  ┌────────┐  ┌────────┐            │
│  │   0    │  │   0    │            │
│  │Transcri│  │Classif.│            │
│  └────────┘  └────────┘            │
│                                     │
│  [🎤 Start Audio] [⏹ Stop Audio]   │
│  [📸 Start Camera] [⏹ Stop Camera] │
│                                     │
│  [🚀 Start Both Systems]            │
│                                     │
│  [📝 Transcripts] [🔍 Classifications]│
│  ┌─────────────────────────────┐   │
│  │ [Log entries appear here]  │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│  🏠 Monitor │ 📂 Sessions │ ⚙️ Settings│
└─────────────────────────────────────┘
```

### Starting Both Systems

1. **Grant Permissions**
   - Camera: Allow when prompted
   - Microphone: Allow when prompted

2. **Click "🚀 Start Both Systems"**
   - Audio recording starts
   - Camera monitoring starts
   - Live preview shows

3. **Inspect Walls**
   - Point camera at wall
   - Speak your observations
   - Classification appears on screen
   - Transcripts update in real-time

4. **Click "⏹ Stop Both"** when done
   - All data saved to server
   - View logs in tabs below

---

## 📊 Features

### 🎤 Audio Tab
```
[1] 14:30:05
"Inspecting the north wall for cracks"

[2] 14:30:10
"Found major damage near window"
```

### 🔍 Classifications Tab
```
[1] 14:30:06
🏗️ Major Crack (92.3%)
   • Major Crack: 92.3%
   • Minor Crack: 4.2%
   • Plain: 2.1%

[2] 14:30:11
🏗️ Peeling (87.6%)
   • Peeling: 87.6%
   • Stain: 8.3%
   • Plain: 3.1%
```

### 📂 Sessions Tab
View all recorded sessions:
- Click any session to view details
- See combined audio + visual data
- Export functionality (coming soon)

---

## 🎨 UI Features

### Modern Design
- **Gradient header** - Professional look
- **Card-based layout** - Easy to read
- **Large touch targets** - Mobile-friendly
- **Smooth animations** - Native feel
- **Color-coded defects** - Quick identification

### Real-time Updates
- **Live camera preview** - 30 FPS
- **Auto-refreshing logs** - Every 3 seconds
- **Status badges** - Recording indicators
- **Confidence bars** - Visual feedback
- **Stats counters** - Transcript/classification counts

### Responsive Design
- **Portrait optimized** - Natural phone use
- **Adapts to screen size** - Works on all devices
- **Touch gestures** - Swipe, tap, scroll
- **Bottom navigation** - Easy thumb reach

---

## 🔧 API Endpoints

The backend provides REST API for all operations:

### Audio
- `POST /api/audio/start` - Start recording
- `POST /api/audio/stop` - Stop recording
- `GET /api/audio/status` - Get status
- `GET /api/audio/transcripts` - Get transcripts
- `POST /api/audio/search` - Search keywords

### Camera
- `POST /api/camera/start` - Start monitoring
- `POST /api/camera/stop` - Stop monitoring
- `GET /api/camera/status` - Get status
- `POST /api/camera/classify` - Classify image
- `GET /api/camera/classifications` - Get classifications
- `POST /api/camera/search` - Search defects

### Unified
- `POST /api/unified/start` - Start both
- `POST /api/unified/stop` - Stop both
- `GET /api/unified/status` - Get both statuses

### Sessions
- `GET /api/sessions/list` - List all sessions
- `GET /api/sessions/<id>` - Get session details

---

## 🌐 Deployment Options

### Option 1: Local Network (Free)
**Best for:** Home/office use

```bash
python mobile_api_server.py
# Access from any device on same WiFi
```

**Pros:** Free, fast, private  
**Cons:** Only works on same network

### Option 2: ngrok (Quick & Easy)
**Best for:** Testing, demos

```bash
# Install ngrok
pip install pyngrok

# In mobile_api_server.py, add:
from pyngrok import ngrok
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")
```

**Pros:** Works anywhere, HTTPS  
**Cons:** Session-based, requires ngrok account

### Option 3: Cloud Deployment
**Best for:** Production use

**Heroku:**
```bash
# Install Heroku CLI
heroku create sitelenz-mobile
git push heroku main
```

**AWS/Azure:**
- Deploy as Flask app
- Configure auto-scaling
- Add HTTPS/SSL

**Pros:** Always available, scalable  
**Cons:** Costs money, setup required

---

## 💡 Usage Tips

### For Best Results

**Camera:**
- Good lighting is crucial
- Keep camera steady
- Fill frame with wall section
- Avoid shadows and glare
- Clean camera lens

**Audio:**
- Speak clearly
- Reduce background noise
- Hold phone close when speaking
- Pause between observations

**Performance:**
- Close other apps
- Ensure good WiFi signal
- Use newer phone for better performance
- Clear app cache periodically

### Battery Optimization

**Long inspections:**
- Bring power bank
- Enable low power mode
- Reduce screen brightness
- Stop systems when not actively using

---

## 🛠️ Troubleshooting

### Camera Not Working

**"Camera access denied"**
- Settings → Apps → Chrome/Safari → Permissions → Camera → Allow
- Reload the page

**"No camera detected"**
- Check if camera works in default camera app
- Restart browser
- Try different browser

### Audio Not Working

**"Microphone access denied"**
- Settings → Apps → Chrome/Safari → Permissions → Microphone → Allow
- Reload the page

**"Not transcribing"**
- Check internet connection (Google Speech API requires internet)
- Speak louder
- Reduce background noise

### Can't Connect from Phone

**"Can't reach server"**
- Check both devices on same WiFi
- Verify IP address is correct
- Check firewall isn't blocking port 5000
- Try `http://` not `https://`

**On Windows:**
```bash
# Allow through firewall
netsh advfirewall firewall add rule name="Flask" dir=in action=allow protocol=TCP localport=5000
```

### App Not Installing

**Android:**
- Use Chrome browser (not Firefox/Edge)
- Must be HTTPS or localhost
- Check "Install apps" permission enabled

**iOS:**
- Must use Safari browser
- iOS 11.3+ required
- May need to trust certificate

---

## 🔐 Security

### For Production Deployment

1. **Add Authentication**
```python
# In mobile_api_server.py
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Your auth logic
    return username == "admin" and password == "secure_pass"

@app.route('/api/...')
@auth.login_required
def endpoint():
    ...
```

2. **Enable HTTPS**
```python
if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Self-signed
    # Or use proper SSL certificates
```

3. **Add Rate Limiting**
```python
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["100 per hour"])
```

---

## 📈 Performance

### Expected Performance

**Model Loading:** ~2-3 seconds  
**Classification Time:** ~0.5-1 second per frame  
**Audio Processing:** ~1-2 seconds per 5-second chunk  
**Camera Preview:** 30 FPS  
**Battery Usage:** ~20-30% per hour (both systems)  

### Optimization Tips

1. **Increase intervals** for longer battery:
```python
# In camera_classifier.py
capture_interval=10  # Instead of 5
```

2. **Use GPU** if available (server-side):
```python
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
```

3. **Reduce resolution** for faster processing:
```python
# In mobile_app.html camera constraints
video: { 
    facingMode: 'environment',
    width: { ideal: 640 },
    height: { ideal: 480 }
}
```

---

## 🎓 Technical Details

### Architecture

```
[Mobile App (PWA)]
       ↕ REST API
[Flask Server]
   ↙         ↘
[AudioLogger] [CameraClassifier]
   ↓              ↓
[JSON Logs]   [JSON Logs]
```

### Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript
- Progressive Web App APIs
- MediaDevices API (camera/mic)
- Service Worker (offline support)

**Backend:**
- Flask (Python web framework)
- Flask-CORS (cross-origin requests)
- PyTorch + ViT (classification)
- SpeechRecognition (audio)

### Data Flow

1. User clicks "Start Both"
2. Frontend → `POST /api/unified/start`
3. Server starts AudioLogger + CameraClassifier
4. Frontend captures camera frames every 5s
5. Frontend → `POST /api/camera/classify` with image
6. Server classifies and returns result
7. Frontend updates UI
8. Audio recorded server-side
9. User clicks "Stop Both"
10. All data saved to JSON files

---

## 🎉 You're Ready!

### Start the Server

```bash
python mobile_api_server.py
```

### Access from Mobile

1. Find computer IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. On phone browser: `http://YOUR_IP:5000`
3. Grant camera and microphone permissions
4. Click "🚀 Start Both Systems"
5. Start inspecting!

---

## 📞 Support

### Quick Diagnostics

```bash
# Test server is running
curl http://localhost:5000/api/health

# Check if accessible from network
# On phone browser: http://YOUR_IP:5000/api/health
```

### Common Issues

**Q: Can I use this offline?**  
A: Camera works offline, but audio needs internet for Google Speech API. Use Whisper for offline audio.

**Q: Does it work on iPhone?**  
A: Yes! Use Safari browser and add to home screen.

**Q: Can multiple phones connect?**  
A: Yes! Each phone gets its own session.

**Q: How do I export data?**  
A: Access JSON files in `logs/` directory on server.

---

**Enjoy your mobile building inspection app!** 📱🏗️✨
