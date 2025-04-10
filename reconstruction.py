# reconstruction.py
import open3d as o3d
import numpy as np
import copy
from typing import List

def combine_point_clouds(pcds: List[o3d.geometry.PointCloud], 
                        transformations: List[np.ndarray]) -> o3d.geometry.PointCloud:
    """Combines multiple point clouds into one using given transformations."""
    combined = o3d.geometry.PointCloud()
    for i, pcd in enumerate(pcds):
        if i == 0:
            combined.points = pcd.points
            combined.colors = pcd.colors
        else:
            pcd_transformed = copy.deepcopy(pcd).transform(transformations[i - 1])
            combined += pcd_transformed
    return combined

def reconstruct_surface(pcd: o3d.geometry.PointCloud) -> o3d.geometry.TriangleMesh:
    """Reconstructs a surface mesh from a point cloud using Poisson reconstruction."""
    print("Reconstructing surface...")
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)
    
    # Clean up low-density vertices
    vertices_to_remove = densities < np.quantile(densities, 0.01)
    mesh.remove_vertices_by_mask(vertices_to_remove)
    return mesh