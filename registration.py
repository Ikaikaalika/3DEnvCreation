# registration.py
import open3d as o3d
import numpy as np
from typing import List

def pairwise_registration(source: o3d.geometry.PointCloud, 
                         target: o3d.geometry.PointCloud, 
                         max_correspondence_distance: float = 0.1) -> np.ndarray:
    """Performs ICP registration to align source to target point cloud."""
    print("Performing ICP registration...")
    init_transform = np.identity(4)
    
    # Estimate normals for better alignment
    source.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    target.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    
    # Use Point-to-Plane ICP
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance, init_transform,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    
    return reg_p2p.transformation

def register_point_clouds(pcds: List[o3d.geometry.PointCloud]) -> List[np.ndarray]:
    """Registers all point clouds to the first one, returning transformations."""
    if len(pcds) <= 1:
        return [np.identity(4)]  # No registration needed for one cloud
    
    transformations = []
    for i in range(len(pcds) - 1):
        transform = pairwise_registration(pcds[i + 1], pcds[0])
        transformations.append(transform)
    return transformations