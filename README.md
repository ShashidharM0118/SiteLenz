# 🏗️ SiteLenz: Building Defect Classification System

AI-powered system for detecting and classifying building defects using Vision Transformer (ViT).

## 🎯 Project Overview

**Detects 7 types of building defects:**
- Algae growth
- Major cracks
- Minor cracks  
- Peeling paint
- Plain (normal surface)
- Spalling concrete
- Stains

## 📁 Project Structure

```
SiteLenz/
├── inference.ipynb          # 🚀 Main notebook - Load model & predict
├── models/                  # 📦 Place trained .pth file here
│   └── vit_weights.pth     # Your trained model (download from Kaggle)
├── data/                    # 📊 Dataset (train/val/test splits)
│   ├── train/              # Training images (by class)
│   ├── val/                # Validation images  
│   └── test/               # Test images
├── sample images/           # 🖼️ Sample defect images
├── code/
│   └── output analysis/    # 📈 Analysis notebooks
├── requirements.txt         # 📋 Python dependencies
└── verify_models.py        # ✅ Verify .pth files
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
pip install -r requirements.txt
```

### 2. Add Your Trained Model

Download `vit_weights.pth` from Kaggle and place it in the `models/` folder.

### 3. Run Inference

Open `inference.ipynb` in Jupyter/VS Code and run all cells.

## 📊 Model Specifications

- **Architecture**: Vision Transformer (ViT-Base-Patch16-224)
- **Parameters**: ~86 million
- **Input Size**: 224×224 RGB images
- **Output**: 7 defect classes with confidence scores
- **Model Size**: ~330 MB

## 🔍 Usage Examples

### Single Image Prediction

```python
from inference import predict_image

prediction, confidence = predict_image(
    'sample images/class_images/major crack/crack (1).jpg',
    model, CLASS_NAMES, device
)
print(f"Prediction: {prediction} ({confidence*100:.1f}% confidence)")
```

### Batch Prediction

```python
# Predict all images in test dataset
accuracy, predictions, labels = evaluate_model(model, test_loader, device)
print(f"Test Accuracy: {accuracy:.2f}%")
```

## 📈 Performance

- **Test Accuracy**: Check confusion matrix in `inference.ipynb`
- **Training Time**: ~4-5 hours on Kaggle GPU T4 x2
- **Inference Speed**: ~50-100 images/second on GPU

## 🛠️ Tools & Technologies

- **PyTorch**: Deep learning framework
- **timm**: Vision Transformer implementation
- **scikit-learn**: Metrics and evaluation
- **matplotlib/seaborn**: Visualization

## 📝 Requirements

```
torch>=2.0.0
torchvision>=0.15.0
timm>=0.9.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
pillow>=9.5.0
```

## 🎓 Model Training

This project uses a pre-trained Vision Transformer model fine-tuned on building defect images. Training was performed on Kaggle with:
- 200 epochs
- AdamW optimizer
- Mixed precision training (FP16)
- Data augmentation

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Status**: ✅ Production Ready | Last Updated: October 2025
