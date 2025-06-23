import laspy
import numpy as np
import os
import open3d as o3d
import pandas as pd
import re

# LAS Point Cloud Processor
# Author: Tomáš Hanousek, hanousek.t@czechglobe.cz
# This script processes LAS files to separate wood and leaves points from forest point clouds,
# applies filtering and centering, and exports them in multiple formats

def apply_sor_filter(points, nb_neighbors=6, std_ratio=1.0):
    """
    Apply Statistical Outlier Removal filter to clean point cloud
    
    Args:
        points: Numpy array of points (N, 3)
        nb_neighbors: Number of neighbors to consider for filtering
        std_ratio: Standard deviation ratio threshold
        
    Returns:
        Filtered points array
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    return np.asarray(pcd.select_by_index(ind).points)

def calculate_shift_from_trunk_base(points, num_base_points=100):
    """
    Calculate shift vector based on the lowest Z points (trunk base)
    This centers the tree at the origin based on the trunk base position
    
    Args:
        points: Numpy array of points (N, 3)
        num_base_points: Number of lowest points to use for base calculation
        
    Returns:
        shift_vector: Numpy array (3,) containing the shift to apply
    """
    # Sort points by Z value (3rd column, index 2)
    sorted_indices = np.argsort(points[:, 2])
    
    # Take the first num_base_points (these will be the lowest Z values)
    # Make sure we don't try to use more points than available
    num_points_to_use = min(num_base_points, len(points))
    base_points = points[sorted_indices[:num_points_to_use]]
    
    # Calculate center of trunk base (mean of X and Y coordinates)
    base_center_x = np.mean(base_points[:, 0])
    base_center_y = np.mean(base_points[:, 1])
    
    # Use the minimum Z from all points as the base Z
    min_z = np.min(points[:, 2])
    
    # Create shift vector to move trunk base to origin
    shift_vector = np.array([base_center_x, base_center_y, min_z])
    
    return shift_vector

def shift_points(points, shift):
    """
    Shift points by subtracting the shift vector
    This effectively moves the point cloud so trunk base is at origin
    
    Args:
        points: Input points array
        shift: Shift vector to subtract
        
    Returns:
        Shifted points array
    """
    return points - shift

def reorder_columns(points):
    """
    Reorder XYZ coordinates if needed
    Currently maintains XYZ order, but can be modified for different coordinate systems
    
    Args:
        points: Input points array
        
    Returns:
        Reordered points array
    """
    return points[:, [0, 1, 2]]  # Keep XYZ order
    #return points[:, [0, 2, 1]]  # Alternative: Reorder XYZ → XZY

def subsample_points(points, num_points=100000):
    """
    Subsample points if there are more than the specified number
    Useful for reducing file size and processing time
    
    Args:
        points: Input points array
        num_points: Maximum number of points to keep
        
    Returns:
        Subsampled points array
    """
    if len(points) > num_points:
        indices = np.random.choice(len(points), num_points, replace=False)
        return points[indices]
    return points

def filter_leaves_above_height(points, height_threshold=2.0):
    """
    Filter leaves to keep only those above the specified height threshold
    Removes low vegetation and focuses on canopy leaves
    
    Args:
        points: Input leaf points array
        height_threshold: Minimum height to keep leaves (in meters)
        
    Returns:
        Filtered leaf points array
    """
    return points[points[:, 2] >= height_threshold]

def process_las_files(directory, wood_output_dir, leaves_output_dir):
    """
    Process LAS files to extract wood and leaves points
    Separates points based on label classification and applies various filters
    
    Args:
        directory: Directory containing input LAS files
        wood_output_dir: Output directory for processed wood points
        leaves_output_dir: Output directory for processed leaves points
    """
    # Create output directories if they don't exist
    os.makedirs(wood_output_dir, exist_ok=True)
    os.makedirs(leaves_output_dir, exist_ok=True)

    # Process each LAS file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.las'):
            filepath = os.path.join(directory, filename)
            print(f"Reading {filepath}")
            
            try:
                # Read LAS file
                las = laspy.read(filepath)

                # Extract points coordinates and classification labels
                points = np.vstack((las.x, las.y, las.z)).T
                labels = las.label  # Extract scalar field "label"

                # Separate wood and leaves points based on classification
                wood_points = points[labels == 3]  # Wood = label 3
                leaves_points = points[labels == 1]  # Leaves = label 1

                print(f"Processing {filename} - Wood: {wood_points.shape[0]}, Leaves: {leaves_points.shape[0]}")

                # Extract tree ID from filename (assuming it contains numbers)
                file_id_match = re.findall(r'\d+', filename)
                file_id = file_id_match[0] if file_id_match else "unknown"

                # Process wood points if available
                if len(wood_points) > 0:
                    # Apply outlier filter to clean wood points
                    wood_points = apply_sor_filter(wood_points)
                    
                    # Calculate shift based on trunk base (lowest 100 points)
                    shift_vector = calculate_shift_from_trunk_base(wood_points, num_base_points=100)
                    
                    # Center wood points at origin
                    wood_points = shift_points(wood_points, shift_vector)
                    reordered_wood_points = reorder_columns(wood_points)
                    subsampled_wood_points = subsample_points(reordered_wood_points, num_points=100000)

                    # Save wood points in first format (XYZ only)
                    wood_output_file = os.path.join(wood_output_dir, f"T{file_id}-F-1-k")
                    pd.DataFrame(reordered_wood_points).to_csv(wood_output_file, sep=' ', index=False, header=False, float_format='%.6f')

                    # Save wood points in second format with label column (XYZL)
                    wood_with_label = np.hstack((wood_points, np.ones((wood_points.shape[0], 1))))  # Add 4th column with 1s
                    wood_output_file_v2 = os.path.join(wood_output_dir, f"T{file_id}.txt")
                    pd.DataFrame(wood_with_label).to_csv(wood_output_file_v2, sep=' ', index=False, header=False, float_format='%.6f')

                # Process leaves points if available
                if len(leaves_points) > 0:
                    # Apply the same centering shift to leaves
                    leaves_points = shift_points(leaves_points, shift_vector)
                    # Filter leaves to keep only those above height threshold
                    leaves_points = filter_leaves_above_height(leaves_points)
                    leaves_points = reorder_columns(leaves_points)

                    # Save leaves points
                    leaves_output_file = os.path.join(leaves_output_dir, f"T{file_id}-F-1-j")
                    pd.DataFrame(leaves_points).to_csv(leaves_output_file, sep=' ', index=False, header=False, float_format='%.6f')

                print(f"Finished processing {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue

# Define input and output directories
# Example: directory_path = r'C:\forest_data\input_las_files'
# Example: wood_output_dir = r'C:\forest_data\output\wood'
# Example: leaves_output_dir = r'C:\forest_data\output\leaves'
directory_path = ''  # Directory containing input LAS files
wood_output_dir = ''  # Output directory for wood points
leaves_output_dir = ''  # Output directory for leaves points

# Run processing
if __name__ == "__main__":
    print("Starting LAS file processing...")
    process_las_files(directory_path, wood_output_dir, leaves_output_dir)
    print("Processing complete!")