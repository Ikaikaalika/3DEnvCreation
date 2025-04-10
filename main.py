# main.py
import os
from data_loader import load_point_clouds
from registration import register_point_clouds
from reconstruction import combine_point_clouds, reconstruct_surface
from visualizer import visualize

def main():
    # Define the data directory
    data_dir = "data/"
    
    # Check if the data directory exists
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' not found.")
        return
    
    # Get all .ply files in the data directory
    file_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) 
                  if f.endswith('.ply')]
    
    # Check if any .ply files were found
    if not file_paths:
        print(f"No .ply files found in '{data_dir}'.")
        return
    
    # Sort files to ensure consistent order (optional)
    file_paths.sort()
    print(f"Found {len(file_paths)} point cloud files: {file_paths}")

    # Load point clouds
    point_clouds = load_point_clouds(file_paths)
    print(f"Loaded {len(point_clouds)} point clouds.")

    # Register point clouds
    transformations = register_point_clouds(point_clouds)

    # Combine into a single point cloud
    combined_pcd = combine_point_clouds(point_clouds, transformations)
    combined_pcd = combined_pcd.voxel_down_sample(voxel_size=0.05)  # Downsample again if needed

    # Visualize combined point cloud
    print("Visualizing combined point cloud...")
    visualize(combined_pcd)

    # Reconstruct surface
    mesh = reconstruct_surface(combined_pcd)

    # Visualize the reconstructed environment
    print("Visualizing reconstructed environment...")
    visualize(combined_pcd, mesh)

if __name__ == "__main__":
    main()