from flask import Flask, render_template, request, jsonify
import torch
import timm
from torchvision import transforms
from PIL import Image
import io
import base64
import os
import time
from datetime import datetime

app = Flask(__name__)

# Configuration
MODEL_PATH = 'models/vit_weights.pth'
NUM_CLASSES = 7
CLASS_NAMES = ['Algae', 'Major Crack', 'Minor Crack', 'Peeling', 'Plain (Normal)', 'Spalling', 'Stain']
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Load model once at startup
print(f"Loading model on {DEVICE}...")
model = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=NUM_CLASSES)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model = model.to(DEVICE)
model.eval()
print("✅ Model loaded successfully!")

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read and process image
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        # Convert image to base64 for display
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        # Preprocess and predict
        img_tensor = transform(img).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        # Prepare results
        prediction = CLASS_NAMES[predicted.item()]
        confidence_score = confidence.item() * 100
        
        # Get all class probabilities
        all_probabilities = []
        for i, prob in enumerate(probabilities[0]):
            all_probabilities.append({
                'class': CLASS_NAMES[i],
                'probability': float(prob.item() * 100)
            })
        
        # Sort by probability
        all_probabilities.sort(key=lambda x: x['probability'], reverse=True)
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'confidence': round(confidence_score, 2),
            'probabilities': all_probabilities,
            'image': f'data:image/jpeg;base64,{img_base64}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/unified/capture', methods=['POST'])
def unified_capture():
    """Handle unified capture from mobile app"""
    try:
        # Accept JSON with base64 encoded image
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Decode base64 image
        img_base64 = data['image']
        transcript = data.get('transcript', 'No transcript')
        
        # Convert base64 to image
        img_bytes = base64.b64decode(img_base64)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        # Preprocess and predict
        img_tensor = transform(img).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        # Prepare results
        prediction = CLASS_NAMES[predicted.item()]
        confidence_score = confidence.item() * 100
        
        return jsonify({
            'success': True,
            'classification': prediction,
            'confidence': round(confidence_score, 2),
            'transcript': transcript,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        print(f"Error in unified_capture: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'device': str(DEVICE)
    })

if __name__ == '__main__':
    print("🚀 Starting SiteLenz Web Interface...")
    print(f"📍 Open your browser at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
