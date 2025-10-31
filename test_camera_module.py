"""
Test script for Camera Classifier
Verifies camera access and model loading
"""

import sys
from pathlib import Path

def test_camera_access():
    """Test if camera can be accessed."""
    print("\n" + "="*60)
    print("Testing Camera Access")
    print("="*60)
    
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            print("❌ Failed to open camera")
            print("   Possible issues:")
            print("   - No camera connected")
            print("   - Camera in use by another application")
            print("   - Insufficient permissions")
            return False
        
        ret, frame = camera.read()
        if not ret:
            print("❌ Failed to read frame from camera")
            camera.release()
            return False
        
        h, w = frame.shape[:2]
        print(f"✅ Camera opened successfully")
        print(f"   Resolution: {w}x{h}")
        
        camera.release()
        return True
        
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False


def test_model_loading():
    """Test if ViT model can be loaded."""
    print("\n" + "="*60)
    print("Testing Model Loading")
    print("="*60)
    
    try:
        import torch
        import timm
        from pathlib import Path
        
        model_path = Path("models/vit_weights.pth")
        
        if not model_path.exists():
            print(f"❌ Model file not found: {model_path}")
            print("   Please ensure vit_weights.pth is in the models/ directory")
            return False
        
        file_size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✅ Model file found: {model_path}")
        print(f"   Size: {file_size_mb:.2f} MB")
        
        # Load model
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"   Device: {device}")
        
        model = timm.create_model('vit_base_patch16_224', 
                                 pretrained=False, 
                                 num_classes=7)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model = model.to(device)
        model.eval()
        
        print(f"✅ Model loaded successfully")
        print(f"   Architecture: ViT-Base-Patch16-224")
        print(f"   Classes: 7")
        
        return True
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False


def test_camera_classifier():
    """Test CameraClassifier initialization."""
    print("\n" + "="*60)
    print("Testing CameraClassifier")
    print("="*60)
    
    try:
        from camera_classifier import CameraClassifier
        
        classifier = CameraClassifier(
            model_path="models/vit_weights.pth",
            capture_interval=5
        )
        
        print("✅ CameraClassifier initialized")
        
        info = classifier.get_session_info()
        print(f"   Device: {info['device']}")
        print(f"   Model loaded: {info['model_loaded']}")
        print(f"   Capture interval: {info['capture_interval']}s")
        
        return True
        
    except Exception as e:
        print(f"❌ CameraClassifier test failed: {e}")
        return False


def test_dependencies():
    """Test if all required packages are installed."""
    print("\n" + "="*60)
    print("Testing Dependencies")
    print("="*60)
    
    packages = {
        'cv2': 'opencv-python',
        'torch': 'torch',
        'torchvision': 'torchvision',
        'timm': 'timm',
        'PIL': 'Pillow',
        'numpy': 'numpy'
    }
    
    all_installed = True
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            all_installed = False
    
    return all_installed


def test_directories():
    """Test if required directories exist."""
    print("\n" + "="*60)
    print("Testing Directory Structure")
    print("="*60)
    
    directories = [
        "logs/frames",
        "logs/classifications",
        "logs/audio",
        "logs/transcripts",
        "models"
    ]
    
    all_exist = True
    for directory in directories:
        path = Path(directory)
        if path.exists():
            print(f"✅ {directory}")
        else:
            print(f"⚠️  {directory} - Not found (will be created)")
            path.mkdir(parents=True, exist_ok=True)
            all_exist = False
    
    return True


def main():
    """Run all tests."""
    print("="*60)
    print("Camera Classifier Module - System Test")
    print("="*60)
    
    tests = [
        ("Dependencies Test", test_dependencies),
        ("Directory Structure Test", test_directories),
        ("Camera Access Test", test_camera_access),
        ("Model Loading Test", test_model_loading),
        ("CameraClassifier Test", test_camera_classifier),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Camera classifier is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python unified_monitoring_app.py' for full app")
        print("2. Check camera preview in the application")
        print("3. Click 'Start Camera' to begin classification")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("Common issues:")
        print("- Camera not connected or in use")
        print("- Model file (vit_weights.pth) missing")
        print("- Missing dependencies (run: pip install -r requirements_unified.txt)")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
