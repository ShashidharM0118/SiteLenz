"""
3D Reconstruction Configuration
Settings for COLMAP, model processing, and API
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
SESSIONS_DIR = BASE_DIR / "sessions"
OUTPUT_DIR = BASE_DIR / "output"
MODELS_DIR = BASE_DIR / "models"

# COLMAP settings
COLMAP_CONFIG = {
    # Feature extraction
    'feature_extractor': {
        'SiftExtraction.max_image_size': 3200,
        'SiftExtraction.max_num_features': 8192,
        'SiftExtraction.first_octave': -1,
        'SiftExtraction.num_threads': -1,
        'SiftExtraction.use_gpu': 1,
        'SiftExtraction.gpu_index': '0',
    },
    
    # Feature matching
    'feature_matcher': {
        'SiftMatching.max_ratio': 0.8,
        'SiftMatching.max_distance': 0.7,
        'SiftMatching.cross_check': 1,
        'SiftMatching.max_error': 4.0,
        'SiftMatching.max_num_matches': 32768,
        'SiftMatching.confidence': 0.999,
        'SiftMatching.min_inlier_ratio': 0.25,
        'SiftMatching.use_gpu': 1,
        'SiftMatching.gpu_index': '0',
    },
    
    # Sparse reconstruction
    'mapper': {
        'Mapper.ba_refine_focal_length': 1,
        'Mapper.ba_refine_principal_point': 0,
        'Mapper.ba_refine_extra_params': 1,
        'Mapper.min_num_matches': 15,
        'Mapper.init_min_num_inliers': 100,
        'Mapper.abs_pose_min_num_inliers': 30,
        'Mapper.abs_pose_min_inlier_ratio': 0.25,
        'Mapper.ba_local_num_images': 6,
        'Mapper.ba_global_max_num_iterations': 50,
        'Mapper.ba_local_max_num_iterations': 25,
        'Mapper.ba_global_max_refinements': 5,
        'Mapper.ba_local_max_refinements': 3,
        'Mapper.snapshot_images_freq': 0,
    },
    
    # Dense reconstruction
    'dense': {
        'max_image_size': 2000,
        'window_radius': 5,
        'window_step': 1,
        'num_samples': 15,
        'num_iterations': 5,
        'geom_consistency': 1,
        'filter_min_ncc': 0.1,
        'filter_min_triangulation_angle': 3.0,
        'filter_min_num_consistent': 3,
        'filter_geom_consistency_max_cost': 1.0,
        'cuda_index': '0',
        'num_threads': -1,
    }
}

# Model processing settings
MODEL_CONFIG = {
    'point_cloud': {
        'voxel_size': 0.02,  # meters
        'outlier_removal': True,
        'radius_outlier': {
            'nb_points': 16,
            'radius': 0.05
        },
        'statistical_outlier': {
            'nb_neighbors': 20,
            'std_ratio': 2.0
        }
    },
    
    'mesh': {
        'reconstruction_method': 'poisson',  # or 'ball_pivoting'
        'poisson_depth': 9,
        'poisson_scale': 1.1,
        'poisson_linear_fit': False,
        'simplification_factor': 0.95,  # Reduce mesh complexity
    },
    
    'texture': {
        'enable': True,
        'resolution': 2048,
        'padding': 8,
    }
}

# API settings
API_CONFIG = {
    'max_session_age_hours': 24,
    'max_images_per_session': 200,
    'min_images_for_reconstruction': 10,
    'allowed_image_extensions': ['.jpg', '.jpeg', '.png'],
    'max_image_size_mb': 10,
}

# Crack overlay settings
CRACK_OVERLAY_CONFIG = {
    'marker_size': 0.05,  # meters
    'colors': {
        'Algae': [0, 255, 0],          # Green
        'Major Crack': [255, 0, 0],     # Red
        'Minor Crack': [255, 165, 0],   # Orange
        'Peeling': [128, 0, 128],       # Purple
        'Plain': [0, 0, 255],           # Blue
        'Spalling': [139, 69, 19],      # Brown
        'Stain': [255, 255, 0],         # Yellow
    }
}

# Create directories if they don't exist
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
