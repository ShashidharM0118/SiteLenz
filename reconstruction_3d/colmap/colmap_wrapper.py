"""
COLMAP Wrapper for 3D Reconstruction
Handles feature extraction, matching, sparse and dense reconstruction
"""

import os
import subprocess
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class COLMAPWrapper:
    """Wrapper for COLMAP reconstruction pipeline"""
    
    def __init__(self, workspace_path: str, colmap_exe: str = "colmap"):
        """
        Initialize COLMAP wrapper
        
        Args:
            workspace_path: Path to workspace directory
            colmap_exe: Path to COLMAP executable (or 'colmap' if in PATH)
        """
        self.workspace = Path(workspace_path)
        self.colmap_exe = colmap_exe
        
        # Create workspace structure
        self.images_path = self.workspace / "images"
        self.database_path = self.workspace / "database.db"
        self.sparse_path = self.workspace / "sparse"
        self.dense_path = self.workspace / "dense"
        
        self.images_path.mkdir(parents=True, exist_ok=True)
        self.sparse_path.mkdir(parents=True, exist_ok=True)
        self.dense_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized COLMAP workspace at {self.workspace}")
    
    def run_command(self, cmd: List[str]) -> bool:
        """
        Run a COLMAP command
        
        Args:
            cmd: Command as list of strings
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                logger.error(f"Command failed: {result.stderr}")
                return False
            
            logger.info(f"Command succeeded")
            return True
            
        except Exception as e:
            logger.error(f"Error running command: {e}")
            return False
    
    def feature_extraction(self, config: Dict = None) -> bool:
        """
        Extract SIFT features from images
        
        Args:
            config: COLMAP configuration options
            
        Returns:
            True if successful
        """
        logger.info("Starting feature extraction...")
        
        cmd = [
            self.colmap_exe, "feature_extractor",
            "--database_path", str(self.database_path),
            "--image_path", str(self.images_path),
        ]
        
        # Add configuration options
        if config:
            for key, value in config.get('feature_extractor', {}).items():
                cmd.extend([f"--{key}", str(value)])
        
        return self.run_command(cmd)
    
    def feature_matching(self, config: Dict = None) -> bool:
        """
        Match features between images
        
        Args:
            config: COLMAP configuration options
            
        Returns:
            True if successful
        """
        logger.info("Starting feature matching...")
        
        cmd = [
            self.colmap_exe, "exhaustive_matcher",
            "--database_path", str(self.database_path),
        ]
        
        # Add configuration options
        if config:
            for key, value in config.get('feature_matcher', {}).items():
                cmd.extend([f"--{key}", str(value)])
        
        return self.run_command(cmd)
    
    def sparse_reconstruction(self, config: Dict = None) -> bool:
        """
        Perform sparse reconstruction (Structure from Motion)
        
        Args:
            config: COLMAP configuration options
            
        Returns:
            True if successful
        """
        logger.info("Starting sparse reconstruction...")
        
        cmd = [
            self.colmap_exe, "mapper",
            "--database_path", str(self.database_path),
            "--image_path", str(self.images_path),
            "--output_path", str(self.sparse_path),
        ]
        
        # Add configuration options
        if config:
            for key, value in config.get('mapper', {}).items():
                cmd.extend([f"--{key}", str(value)])
        
        return self.run_command(cmd)
    
    def image_undistortion(self) -> bool:
        """
        Undistort images for dense reconstruction
        
        Returns:
            True if successful
        """
        logger.info("Undistorting images...")
        
        # Find the sparse model (usually in sparse/0)
        model_path = self.sparse_path / "0"
        if not model_path.exists():
            logger.error("No sparse model found")
            return False
        
        cmd = [
            self.colmap_exe, "image_undistorter",
            "--image_path", str(self.images_path),
            "--input_path", str(model_path),
            "--output_path", str(self.dense_path),
            "--output_type", "COLMAP",
        ]
        
        return self.run_command(cmd)
    
    def dense_reconstruction(self, config: Dict = None) -> bool:
        """
        Perform dense reconstruction (Multi-View Stereo)
        
        Args:
            config: COLMAP configuration options
            
        Returns:
            True if successful
        """
        logger.info("Starting dense reconstruction...")
        
        # Stereo matching
        cmd_stereo = [
            self.colmap_exe, "patch_match_stereo",
            "--workspace_path", str(self.dense_path),
        ]
        
        if config:
            for key, value in config.get('dense', {}).items():
                if key.startswith('filter_'):
                    continue  # Filter params are for stereo fusion
                cmd_stereo.extend([f"--PatchMatchStereo.{key}", str(value)])
        
        if not self.run_command(cmd_stereo):
            return False
        
        # Stereo fusion
        cmd_fusion = [
            self.colmap_exe, "stereo_fusion",
            "--workspace_path", str(self.dense_path),
            "--output_path", str(self.dense_path / "fused.ply"),
        ]
        
        if config:
            for key, value in config.get('dense', {}).items():
                if key.startswith('filter_'):
                    filter_key = key.replace('filter_', '')
                    cmd_fusion.extend([f"--StereoFusion.{filter_key}", str(value)])
        
        return self.run_command(cmd_fusion)
    
    def export_model(self, output_format: str = "PLY") -> Optional[Path]:
        """
        Export the reconstruction model
        
        Args:
            output_format: Output format (PLY, OBJ, etc.)
            
        Returns:
            Path to exported model file
        """
        logger.info(f"Exporting model as {output_format}...")
        
        # Check if dense reconstruction exists
        dense_model = self.dense_path / "fused.ply"
        if dense_model.exists():
            logger.info(f"Dense model available at {dense_model}")
            return dense_model
        
        # Otherwise export sparse model
        sparse_model = self.sparse_path / "0"
        if not sparse_model.exists():
            logger.error("No model found to export")
            return None
        
        output_file = self.workspace / f"model.{output_format.lower()}"
        
        cmd = [
            self.colmap_exe, "model_converter",
            "--input_path", str(sparse_model),
            "--output_path", str(output_file),
            "--output_type", output_format,
        ]
        
        if self.run_command(cmd):
            return output_file
        
        return None
    
    def full_reconstruction(self, config: Dict = None) -> Dict:
        """
        Run the full reconstruction pipeline
        
        Args:
            config: COLMAP configuration
            
        Returns:
            Dictionary with results and status
        """
        results = {
            'success': False,
            'steps_completed': [],
            'errors': [],
            'output_files': {}
        }
        
        try:
            # Step 1: Feature extraction
            if self.feature_extraction(config):
                results['steps_completed'].append('feature_extraction')
            else:
                results['errors'].append('Feature extraction failed')
                return results
            
            # Step 2: Feature matching
            if self.feature_matching(config):
                results['steps_completed'].append('feature_matching')
            else:
                results['errors'].append('Feature matching failed')
                return results
            
            # Step 3: Sparse reconstruction
            if self.sparse_reconstruction(config):
                results['steps_completed'].append('sparse_reconstruction')
            else:
                results['errors'].append('Sparse reconstruction failed')
                return results
            
            # Step 4: Image undistortion
            if self.image_undistortion():
                results['steps_completed'].append('image_undistortion')
            else:
                results['errors'].append('Image undistortion failed')
                return results
            
            # Step 5: Dense reconstruction
            if self.dense_reconstruction(config):
                results['steps_completed'].append('dense_reconstruction')
            else:
                results['errors'].append('Dense reconstruction failed')
                # Continue anyway - sparse model might be useful
            
            # Export model
            model_path = self.export_model()
            if model_path:
                results['output_files']['model'] = str(model_path)
                results['success'] = True
            
            logger.info(f"Reconstruction completed: {len(results['steps_completed'])} steps")
            return results
            
        except Exception as e:
            logger.error(f"Reconstruction failed: {e}")
            results['errors'].append(str(e))
            return results
    
    def get_reconstruction_stats(self) -> Dict:
        """
        Get statistics about the reconstruction
        
        Returns:
            Dictionary with reconstruction statistics
        """
        stats = {
            'num_images': 0,
            'num_cameras': 0,
            'num_points_sparse': 0,
            'num_points_dense': 0,
        }
        
        # Count images
        if self.images_path.exists():
            stats['num_images'] = len(list(self.images_path.glob('*.jpg'))) + \
                                 len(list(self.images_path.glob('*.png')))
        
        # Try to read sparse model stats
        sparse_model = self.sparse_path / "0"
        if sparse_model.exists():
            points_file = sparse_model / "points3D.bin"
            cameras_file = sparse_model / "cameras.bin"
            
            if points_file.exists():
                # Rough estimate based on file size
                stats['num_points_sparse'] = points_file.stat().st_size // 43  # bytes per point
            
            if cameras_file.exists():
                stats['num_cameras'] = cameras_file.stat().st_size // 80  # rough estimate
        
        # Check dense model
        dense_model = self.dense_path / "fused.ply"
        if dense_model.exists():
            # Will be calculated in model_processor
            stats['has_dense_model'] = True
        
        return stats
