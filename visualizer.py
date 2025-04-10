# visualizer.py
import open3d as o3d

def visualize(pcd: o3d.geometry.PointCloud, mesh: o3d.geometry.TriangleMesh = None):
    """Visualizes a point cloud and optionally a mesh."""
    geometries = [pcd]
    if mesh:
        geometries.append(mesh)
    o3d.visualization.draw_geometries(geometries, window_name="3D Environment")