# data_loader.py
import open3d as o3d
from typing import List

def load_point_clouds(file_paths: List[str]) -> List[o3d.geometry.PointCloud]:
    """Loads point clouds from a list of file paths."""
    pcds = []
    for file in file_paths:
        pcd = o3d.io.read_point_cloud(file)
        # Downsample to speed up processing (optional)
        pcd = pcd.voxel_down_sample(voxel_size=0.05)
        pcds.append(pcd)
    return pcds