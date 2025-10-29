# 🚀 Quick Setup Guide

## Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Add Your Trained Model
1. Download `vit_weights.pth` from Kaggle (from your training output)
2. Place it in the `models/` folder

Your structure should look like:
```
SiteLenz/
├── inference.ipynb
├── models/
│   └── vit_weights.pth    ← Place your model here
└── data/
    └── test/
```

### Step 3: Run Inference
1. Open `inference.ipynb` in Jupyter or VS Code
2. Run all cells (Ctrl+Enter or Run All)
3. Done! 🎉

## 🔍 What You Can Do

### Predict Single Image
```python
image_path = 'sample images/class_images/major crack/crack (1).jpg'
prediction, confidence = predict_image(image_path, model, CLASS_NAMES, device)
# Output: "major_crack" with 98.5% confidence
```

### Evaluate on Test Set
```python
accuracy, predictions, labels = evaluate_model(model, test_loader, device)
# Output: Test Accuracy: 95.2%
```

### View Confusion Matrix
Already included in the notebook - just run the cells!

## ❗ Troubleshooting

**Error: "Model file not found"**
- Make sure `vit_weights.pth` is in the `models/` folder

**Error: "timm not found"**
- Run: `pip install timm`

**Error: "CUDA out of memory"**
- Reduce batch size in the notebook (default: 32)

## 📊 Expected Output Files

After running Kaggle training, you should have:
- ✅ `vit_weights.pth` (~330MB) - **Required**
- `vit_results.csv` - Optional
- `curat_vt_confusion_matrix.png` - Optional
- `curat_vt_classification_report.txt` - Optional

**Only the `.pth` file is needed for inference!**

## 🎯 Next Steps

1. Test on your own images
2. Integrate into a web app (Flask/FastAPI)
3. Deploy to production
4. Collect feedback and retrain if needed

---

Need help? Check `README.md` for detailed documentation.
