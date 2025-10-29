# 🌐 Web Interface Guide

## Quick Start

### 1. Install Flask (if not already installed)
```bash
pip install flask
```

### 2. Run the Web App
```bash
python app.py
```

### 3. Open in Browser
Go to: **http://localhost:5000**

## 📸 How to Use

1. **Upload Image**: Click the upload area or drag & drop an image
2. **Analyze**: Click the "Analyze Defect" button
3. **View Results**: See the predicted defect type with confidence score

## 🎨 Features

- ✅ **Drag & Drop**: Easy image upload
- ✅ **Real-time Prediction**: Instant results
- ✅ **Confidence Scores**: See prediction confidence
- ✅ **All Probabilities**: View probabilities for all 7 classes
- ✅ **Beautiful UI**: Modern, responsive design
- ✅ **Mobile Friendly**: Works on phones and tablets

## 🔧 API Endpoints

### `GET /`
Main web interface

### `POST /predict`
Upload and analyze image
- **Input**: Image file (JPG, PNG)
- **Output**: JSON with prediction and probabilities

### `GET /health`
Check if server is running
- **Output**: Server status and model info

## 📊 Detectable Defects

1. **Algae** - Algae growth on surfaces
2. **Major Crack** - Large structural cracks
3. **Minor Crack** - Small hairline cracks
4. **Peeling** - Paint or coating peeling
5. **Plain (Normal)** - No defects detected
6. **Spalling** - Concrete chipping/flaking
7. **Stain** - Discoloration or stains

## 🛠️ Troubleshooting

**Port already in use?**
```bash
# Change port in app.py (last line)
app.run(debug=True, host='0.0.0.0', port=8080)
```

**Model not found?**
- Make sure `vit_weights.pth` is in the `models/` folder

**Slow predictions?**
- Model runs on GPU if available (much faster)
- CPU predictions take 2-5 seconds per image

## 🚀 Deployment Options

### Local Network Access
```python
# In app.py, use:
app.run(host='0.0.0.0', port=5000)
# Access from other devices: http://YOUR_IP:5000
```

### Production Deployment
For production, use gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 💡 Tips

- **Best Image Quality**: Upload clear, well-lit photos
- **Image Size**: Any size works (auto-resized to 224x224)
- **Formats**: JPG, JPEG, PNG supported
- **Speed**: GPU ~0.1s, CPU ~2-5s per image

---

**Ready to use!** 🎉 Just run `python app.py` and start analyzing building defects!
