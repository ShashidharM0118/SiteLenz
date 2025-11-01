"""
3D Model Processing using Trimesh
Point cloud processing, mesh generation, crack overlay
Optimized for Python 3.13 compatibility
"""

import numpy as np
import trimesh
from plyfile import PlyData, PlyElement
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelProcessor:
    """Process and enhance 3D models using trimesh"""
    
    def __init__(self, model_path: str):
        """
        Initialize model processor
        
        Args:
            model_path: Path to input model file (PLY, OBJ, etc.)
        """
        self.model_path = Path(model_path)
        self.point_cloud = None
        self.mesh = None
        self.markers = []
        
        logger.info(f"Initialized ModelProcessor for {self.model_path}")
    
    def load_point_cloud(self) -> bool:
        """
        Load point cloud from PLY file
        
        Returns:
            True if successful
        """
        try:
            logger.info(f"Loading point cloud from {self.model_path}")
            
            # Load PLY file
            plydata = PlyData.read(str(self.model_path))
            vertex = plydata['vertex']
            
            # Extract coordinates
            points = np.vstack([
                vertex['x'],
                vertex['y'],
                vertex['z']
            ]).T
            
            # Extract colors if available
            colors = None
            if 'red' in vertex and 'green' in vertex and 'blue' in vertex:
                colors = np.vstack([
                    vertex['red'],
                    vertex['green'],
                    vertex['blue']
                ]).T
            
            self.point_cloud = {
                'points': points,
                'colors': colors
            }
            
            num_points = len(points)
            logger.info(f"Loaded point cloud with {num_points} points")
            
            return num_points > 0
            
        except Exception as e:
            logger.error(f"Failed to load point cloud: {e}")
            return False
    
    def load_mesh(self) -> bool:
        """
        Load mesh from file
        
        Returns:
            True if successful
        """
        try:
            logger.info(f"Loading mesh from {self.model_path}")
            
            self.mesh = trimesh.load(str(self.model_path))
            
            if isinstance(self.mesh, trimesh.Scene):
                # If it's a scene, combine all geometries
                self.mesh = trimesh.util.concatenate(
                    list(self.mesh.geometry.values())
                )
            
            logger.info(f"Loaded mesh: {len(self.mesh.vertices)} vertices, {len(self.mesh.faces)} faces")
            
            return len(self.mesh.vertices) > 0
            
        except Exception as e:
            logger.error(f"Failed to load mesh: {e}")
            return False
    
    def downsample_point_cloud(self, voxel_size: float = 0.02) -> bool:
        """
        Downsample point cloud using voxel grid
        
        Args:
            voxel_size: Size of voxel in meters
            
        Returns:
            True if successful
        """
        if self.point_cloud is None:
            logger.error("No point cloud loaded")
            return False
        
        try:
            logger.info(f"Downsampling with voxel size {voxel_size}")
            points = self.point_cloud['points']
            colors = self.point_cloud['colors']
            
            original_size = len(points)
            
            # Voxelize
            voxel_indices = np.floor(points / voxel_size).astype(int)
            
            # Get unique voxels
            _, unique_indices = np.unique(voxel_indices, axis=0, return_index=True)
            
            self.point_cloud['points'] = points[unique_indices]
            if colors is not None:
                self.point_cloud['colors'] = colors[unique_indices]
            
            new_size = len(self.point_cloud['points'])
            reduction = (1 - new_size / original_size) * 100
            logger.info(f"Reduced from {original_size} to {new_size} points ({reduction:.1f}% reduction)")
            
            return True
            
        except Exception as e:
            logger.error(f"Downsampling failed: {e}")
            return False
    
    def remove_outliers(self, method: str = 'statistical', **kwargs) -> bool:
        """
        Remove outlier points
        
        Args:
            method: 'statistical' or 'radius'
            **kwargs: Method-specific parameters
            
        Returns:
            True if successful
        """
        if self.point_cloud is None:
            logger.error("No point cloud loaded")
            return False
        
        try:
            logger.info(f"Removing outliers using {method} method")
            points = self.point_cloud['points']
            colors = self.point_cloud['colors']
            
            original_size = len(points)
            
            if method == 'statistical':
                nb_neighbors = kwargs.get('nb_neighbors', 20)
                std_ratio = kwargs.get('std_ratio', 2.0)
                
                # Compute distances to nearest neighbors
                from scipy.spatial import cKDTree
                tree = cKDTree(points)
                distances, _ = tree.query(points, k=nb_neighbors+1)
                avg_distances = np.mean(distances[:, 1:], axis=1)
                
                # Filter based on statistics
                mean_dist = np.mean(avg_distances)
                std_dist = np.std(avg_distances)
                threshold = mean_dist + std_ratio * std_dist
                
                mask = avg_distances < threshold
                
            elif method == 'radius':
                nb_points = kwargs.get('nb_points', 16)
                radius = kwargs.get('radius', 0.05)
                
                from scipy.spatial import cKDTree
                tree = cKDTree(points)
                counts = np.array([len(tree.query_ball_point(p, radius)) for p in points])
                
                mask = counts >= nb_points
            
            else:
                logger.error(f"Unknown outlier removal method: {method}")
                return False
            
            self.point_cloud['points'] = points[mask]
            if colors is not None:
                self.point_cloud['colors'] = colors[mask]
            
            new_size = len(self.point_cloud['points'])
            removed = original_size - new_size
            logger.info(f"Removed {removed} outlier points ({removed/original_size*100:.1f}%)")
            
            return True
            
        except Exception as e:
            logger.error(f"Outlier removal failed: {e}")
            return False
    
    def point_cloud_to_mesh(self, method: str = 'alpha_shape', **kwargs) -> bool:
        """
        Convert point cloud to mesh
        
        Args:
            method: 'alpha_shape' or 'convex_hull'
            **kwargs: Method-specific parameters
            
        Returns:
            True if successful
        """
        if self.point_cloud is None:
            logger.error("No point cloud loaded")
            return False
        
        try:
            logger.info(f"Creating mesh from point cloud using {method}...")
            
            points = self.point_cloud['points']
            
            if method == 'alpha_shape':
                # Alpha shape reconstruction
                alpha = kwargs.get('alpha', 0.1)
                from scipy.spatial import Delaunay
                
                # Simple alpha shape using Delaunay triangulation
                tri = Delaunay(points)
                
                # Create mesh from triangulation
                # This is a simplified version - full alpha shape is more complex
                self.mesh = trimesh.Trimesh(
                    vertices=points,
                    faces=tri.simplices
                )
                
            elif method == 'convex_hull':
                # Convex hull
                self.mesh = trimesh.convex.convex_hull(points)
            
            else:
                logger.error(f"Unknown mesh creation method: {method}")
                return False
            
            # Clean up mesh
            self.mesh.remove_duplicate_faces()
            self.mesh.remove_unreferenced_vertices()
            
            logger.info(f"Created mesh: {len(self.mesh.vertices)} vertices, {len(self.mesh.faces)} faces")
            
            return True
            
        except Exception as e:
            logger.error(f"Mesh creation failed: {e}")
            return False
    
    def simplify_mesh(self, target_faces: int = None, target_reduction: float = 0.95) -> bool:
        """
        Simplify mesh while preserving shape
        
        Args:
            target_faces: Target number of faces
            target_reduction: Target reduction factor (0.95 = keep 95% of faces)
            
        Returns:
            True if successful
        """
        if self.mesh is None:
            logger.error("No mesh loaded")
            return False
        
        try:
            logger.info(f"Simplifying mesh...")
            
            original_faces = len(self.mesh.faces)
            
            if target_faces is None:
                target_faces = int(original_faces * target_reduction)
            
            self.mesh = self.mesh.simplify_quadric_decimation(target_faces)
            
            new_faces = len(self.mesh.faces)
            logger.info(f"Reduced from {original_faces} to {new_faces} faces")
            
            return True
            
        except Exception as e:
            logger.error(f"Mesh simplification failed: {e}")
            return False
    
    def smooth_mesh(self, iterations: int = 5) -> bool:
        """
        Smooth mesh surface
        
        Args:
            iterations: Number of smoothing iterations
            
        Returns:
            True if successful
        """
        if self.mesh is None:
            logger.error("No mesh loaded")
            return False
        
        try:
            logger.info(f"Smoothing mesh ({iterations} iterations)...")
            
            trimesh.smoothing.filter_laplacian(self.mesh, iterations=iterations)
            
            logger.info("Mesh smoothed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Mesh smoothing failed: {e}")
            return False
    
    def add_crack_markers(self, annotations: List[Dict]) -> bool:
        """
        Add colored markers for crack locations
        
        Args:
            annotations: List of annotations with position and classification
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"Adding {len(annotations)} crack markers...")
            
            from ..config import CRACK_OVERLAY_CONFIG
            
            self.markers = []
            
            for ann in annotations:
                position = np.array(ann.get('position', [0, 0, 0]))
                classification = ann.get('classification', 'Unknown')
                
                # Get color for this classification
                color = CRACK_OVERLAY_CONFIG['colors'].get(
                    classification,
                    [128, 128, 128]  # Default gray
                )
                
                # Create sphere marker
                marker = trimesh.primitives.Sphere(
                    radius=CRACK_OVERLAY_CONFIG['marker_size'],
                    center=position
                )
                marker.visual.face_colors = color + [255]  # Add alpha
                
                self.markers.append(marker)
            
            logger.info(f"Added {len(self.markers)} markers")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add markers: {e}")
            return False
    
    def save_point_cloud(self, output_path: str) -> bool:
        """
        Save processed point cloud to PLY
        
        Args:
            output_path: Output file path
            
        Returns:
            True if successful
        """
        if self.point_cloud is None:
            logger.error("No point cloud to save")
            return False
        
        try:
            logger.info(f"Saving point cloud to {output_path}")
            
            points = self.point_cloud['points']
            colors = self.point_cloud['colors']
            
            # Prepare vertex data
            vertex_data = [
                (points[i, 0], points[i, 1], points[i, 2],
                 colors[i, 0] if colors is not None else 128,
                 colors[i, 1] if colors is not None else 128,
                 colors[i, 2] if colors is not None else 128)
                for i in range(len(points))
            ]
            
            vertex = np.array(vertex_data, dtype=[
                ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
                ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')
            ])
            
            el = PlyElement.describe(vertex, 'vertex')
            PlyData([el]).write(output_path)
            
            logger.info(f"Saved {len(points)} points")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save point cloud: {e}")
            return False
    
    def save_mesh(self, output_path: str, file_type: str = None) -> bool:
        """
        Save mesh
        
        Args:
            output_path: Output file path
            file_type: File type (PLY, OBJ, STL, etc.)
            
        Returns:
            True if successful
        """
        if self.mesh is None:
            logger.error("No mesh to save")
            return False
        
        try:
            logger.info(f"Saving mesh to {output_path}")
            
            # Combine mesh with markers if they exist
            if self.markers:
                combined = trimesh.util.concatenate([self.mesh] + self.markers)
                combined.export(output_path, file_type=file_type)
            else:
                self.mesh.export(output_path, file_type=file_type)
            
            logger.info("Mesh saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save mesh: {e}")
            return False
    
    def get_model_info(self) -> Dict:
        """
        Get information about the current model
        
        Returns:
            Dictionary with model statistics
        """
        info = {}
        
        if self.point_cloud is not None:
            points = self.point_cloud['points']
            info['point_cloud'] = {
                'num_points': len(points),
                'has_colors': self.point_cloud['colors'] is not None,
                'bounding_box': {
                    'min': points.min(axis=0).tolist(),
                    'max': points.max(axis=0).tolist(),
                }
            }
        
        if self.mesh is not None:
            info['mesh'] = {
                'num_vertices': len(self.mesh.vertices),
                'num_faces': len(self.mesh.faces),
                'has_colors': self.mesh.visual.kind == 'vertex',
                'is_watertight': self.mesh.is_watertight,
                'volume': float(self.mesh.volume) if self.mesh.is_watertight else None,
                'surface_area': float(self.mesh.area),
            }
        
        if self.markers:
            info['markers'] = {
                'count': len(self.markers)
            }
        
        return info
    
    def process_full_pipeline(self, config: Dict = None) -> Dict:
        """
        Run the full processing pipeline
        
        Args:
            config: Processing configuration
            
        Returns:
            Dictionary with results
        """
        results = {
            'success': False,
            'steps_completed': [],
            'errors': [],
            'model_info': {}
        }
        
        try:
            # Try to load as point cloud first
            if self.load_point_cloud():
                results['steps_completed'].append('load_point_cloud')
                
                # Downsample if configured
                if config and config.get('point_cloud', {}).get('voxel_size'):
                    voxel_size = config['point_cloud']['voxel_size']
                    if self.downsample_point_cloud(voxel_size):
                        results['steps_completed'].append('downsample')
                
                # Remove outliers
                if config and config.get('point_cloud', {}).get('outlier_removal'):
                    stats_config = config['point_cloud'].get('statistical_outlier', {})
                    if self.remove_outliers('statistical', **stats_config):
                        results['steps_completed'].append('outlier_removal')
                
                # Create mesh from point cloud
                if config and config.get('mesh'):
                    method = config['mesh'].get('reconstruction_method', 'alpha_shape')
                    if self.point_cloud_to_mesh(method):
                        results['steps_completed'].append('mesh_creation')
            
            # Or load as mesh directly
            elif self.load_mesh():
                results['steps_completed'].append('load_mesh')
            
            else:
                results['errors'].append('Failed to load model')
                return results
            
            # Simplify mesh if configured and mesh exists
            if self.mesh and config and config.get('mesh', {}).get('simplification_factor'):
                factor = config['mesh']['simplification_factor']
                if self.simplify_mesh(target_reduction=factor):
                    results['steps_completed'].append('simplification')
            
            # Smooth mesh if configured
            if self.mesh and config and config.get('mesh', {}).get('smooth'):
                iterations = config['mesh'].get('smooth_iterations', 5)
                if self.smooth_mesh(iterations):
                    results['steps_completed'].append('smoothing')
            
            results['model_info'] = self.get_model_info()
            results['success'] = True
            
            logger.info(f"Processing completed: {len(results['steps_completed'])} steps")
            return results
            
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            results['errors'].append(str(e))
            return results
