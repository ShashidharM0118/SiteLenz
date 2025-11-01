# 🏗️ SiteLenz 3D Room Reconstruction System

Complete 3D reconstruction system for creating spatial models of rooms with crack/defect annotations.

## 📋 Overview

This module enables:
- **3D Room Scanning**: Convert photos into 3D models
- **COLMAP Integration**: Professional photogrammetry pipeline
- **Crack Overlay**: Visualize defects in 3D space
- **Voice Annotations**: Spatial audio notes
- **Multi-format Export**: PLY, OBJ, GLB formats

## 🚀 Quick Start

### Prerequisites

1. **Install COLMAP**: Download from https://colmap.github.io/install.html
   - Windows: Download pre-built binaries
   - Add COLMAP to PATH or note installation directory

2. **Install Python Packages**:
```bash
pip install opencv-python numpy scipy trimesh plyfile
```

### Start Using

1. **Start Flask Server**:
```bash
python app.py
```

2. **Create 3D Session**:
```bash
POST http://localhost:5000/api/3d/start-session
{
  "project_name": "bedroom_scan",
  "room_type": "bedroom"
}
```

3. **Upload Images**:
```bash
POST http://localhost:5000/api/3d/upload-image
{
  "session_id": "session_1234567890",
  "image": "base64_encoded_image",
  "camera_pose": {"position": [x, y, z], "rotation": [qx, qy, qz, qw]},
  "classification": "Major Crack",
  "transcript": "Large crack on north wall"
}
```

4. **Start Reconstruction**:
```bash
POST http://localhost:5000/api/3d/reconstruct
{
  "session_id": "session_1234567890",
  "quality": "high"
}
```

5. **Check Status**:
```bash
GET http://localhost:5000/api/3d/status/recon_1234567890
```

6. **Download Model**:
```bash
GET http://localhost:5000/api/3d/download/recon_1234567890/glb
```

## 📁 Folder Structure

```
reconstruction_3d/
├── api/
│   └── routes.py          # Flask API endpoints
├── colmap/
│   └── colmap_wrapper.py  # COLMAP integration
├── processing/
│   └── model_processor.py # 3D model processing
├── config.py              # Configuration settings
├── sessions/              # Active capture sessions
├── output/                # Final 3D models
└── README.md              # This file
```

## 🔧 API Endpoints

### 1. Start Session
**POST** `/api/3d/start-session`

Create a new 3D capture session.

**Request**:
```json
{
  "project_name": "room_scan_1",
  "room_type": "bedroom"
}
```

**Response**:
```json
{
  "success": true,
  "session_id": "session_1234567890",
  "message": "Session started successfully"
}
```

### 2. Upload Image
**POST** `/api/3d/upload-image`

Upload an image with camera position and classification.

**Request**:
```json
{
  "session_id": "session_1234567890",
  "image": "base64_encoded_jpg",
  "camera_pose": {
    "position": [1.5, 0.8, 2.3],
    "rotation": [0, 0, 0, 1]
  },
  "transcript": "Crack near window",
  "classification": "Major Crack",
  "confidence": 95.5
}
```

**Response**:
```json
{
  "success": true,
  "image_count": 15,
  "annotation_count": 3,
  "message": "Image 14 uploaded successfully"
}
```

### 3. Start Reconstruction
**POST** `/api/3d/reconstruct`

Begin 3D model reconstruction.

**Request**:
```json
{
  "session_id": "session_1234567890",
  "quality": "high"
}
```

**Quality options**: `high`, `medium`, `low`

**Response**:
```json
{
  "success": true,
  "reconstruction_id": "recon_1234567890",
  "message": "Reconstruction started",
  "estimated_time_minutes": 5
}
```

### 4. Check Status
**GET** `/api/3d/status/<recon_id>`

Get reconstruction progress.

**Response**:
```json
{
  "success": true,
  "status": "running",
  "progress": 75,
  "message": "Processing 3D model...",
  "current_step": "processing"
}
```

Status values: `queued`, `running`, `completed`, `failed`

### 5. Download Model
**GET** `/api/3d/download/<recon_id>/<file_type>`

Download reconstructed model.

File types: `ply`, `obj`, `glb`

### 6. List Sessions
**GET** `/api/3d/sessions`

Get all active sessions.

### 7. Delete Session
**DELETE** `/api/3d/session/<session_id>`

Remove a session and its data.

## ⚙️ Configuration

Edit `config.py` to customize:

### COLMAP Settings
```python
COLMAP_CONFIG = {
    'feature_extractor': {
        'SiftExtraction.max_num_features': 8192,
        'SiftExtraction.use_gpu': 1,
    },
    'feature_matcher': {
        'SiftMatching.max_ratio': 0.8,
        'SiftMatching.use_gpu': 1,
    },
    # ... more settings
}
```

### Model Processing
```python
MODEL_CONFIG = {
    'point_cloud': {
        'voxel_size': 0.02,  # Downsampling resolution
        'outlier_removal': True,
    },
    'mesh': {
        'reconstruction_method': 'alpha_shape',
        'simplification_factor': 0.95,
    }
}
```

### API Limits
```python
API_CONFIG = {
    'max_session_age_hours': 24,
    'max_images_per_session': 200,
    'min_images_for_reconstruction': 10,
}
```

## 🎨 Crack Classification Colors

```python
CRACK_OVERLAY_CONFIG = {
    'marker_size': 0.05,  # meters
    'colors': {
        'Algae': [0, 255, 0],          # Green
        'Major Crack': [255, 0, 0],     # Red
        'Minor Crack': [255, 165, 0],   # Orange
        'Peeling': [128, 0, 128],       # Purple
        'Spalling': [139, 69, 19],      # Brown
        'Stain': [255, 255, 0],         # Yellow
    }
}
```

## 📱 Flutter App Integration

Add to your Flutter app:

```dart
// Start 3D session
final response = await apiService.post('/api/3d/start-session', {
  'project_name': 'Room Scan',
});

// Upload images with ARCore positions
await apiService.post('/api/3d/upload-image', {
  'session_id': sessionId,
  'image': base64Image,
  'camera_pose': {
    'position': [x, y, z],
    'rotation': [qx, qy, qz, qw],
  },
  'classification': classification,
  'transcript': voiceLog,
});

// Start reconstruction
await apiService.post('/api/3d/reconstruct', {
  'session_id': sessionId,
  'quality': 'medium',
});

// Poll for status
final status = await apiService.get('/api/3d/status/$reconId');
```

## 🔍 How It Works

1. **Image Collection**: User walks around room taking photos
2. **ARCore Tracking**: Flutter app captures camera positions
3. **Feature Extraction**: COLMAP finds matching features between images
4. **Sparse Reconstruction**: Creates 3D point cloud from features
5. **Dense Reconstruction**: Multi-view stereo creates detailed model
6. **Mesh Generation**: Converts point cloud to textured mesh
7. **Crack Overlay**: Adds colored markers at defect locations
8. **Export**: Saves as PLY/OBJ/GLB for viewing

## 📊 Quality Presets

### High Quality
- 16,384 features per image
- 3200px max image size
- ~2 minutes per image
- Best for final deliverables

### Medium Quality (Default)
- 8,192 features per image
- 2000px max image size
- ~1 minute per image
- Good balance

### Low Quality
- 4,096 features per image
- 1600px max image size
- ~30 seconds per image
- Quick previews

## 🐛 Troubleshooting

### COLMAP Not Found
```
Error: 'colmap' is not recognized
```
**Solution**: Add COLMAP to PATH or specify full path in code:
```python
colmap = COLMAPWrapper(
    workspace_path=str(session_folder),
    colmap_exe="C:/Program Files/COLMAP/colmap.exe"
)
```

### Reconstruction Failed
Check:
- Minimum 10 images uploaded
- Images have sufficient overlap
- Lighting conditions consistent
- Camera moved between shots

### Out of Memory
- Reduce quality setting
- Use fewer images
- Lower max_image_size in config

## 📄 Output Files

Each reconstruction produces:

```
output/recon_1234567890/
├── model.ply          # Point cloud with colors
├── model.obj          # Mesh with materials
├── model.glb          # WebGL-ready format
└── metadata.json      # Reconstruction info
```

### Metadata Example
```json
{
  "reconstruction_id": "recon_1234567890",
  "session_id": "session_1234567890",
  "project_name": "bedroom_scan",
  "num_images": 45,
  "num_annotations": 8,
  "model_info": {
    "mesh": {
      "num_vertices": 125000,
      "num_faces": 250000,
      "is_watertight": true,
      "volume": 45.3,
      "surface_area": 156.8
    }
  },
  "created_at": 1699012345.67
}
```

## 🌐 Web Viewer

Coming soon: Interactive 3D viewer using Three.js

## 🔐 Security Notes

- Sessions auto-expire after 24 hours
- Max 200 images per session
- No authentication (add for production)
- Validate all user inputs

## 📝 License

Part of SiteLenz project - All rights reserved

## 🤝 Contributing

Created as part of the SiteLenz construction inspection system.

## 📧 Support

For issues, check logs in:
- Console output (Flask server)
- `reconstruction_3d/sessions/<session_id>/`
- Check COLMAP installation

---

**Built with**: COLMAP, Trimesh, OpenCV, Flask, Python 3.13
