import os
import shutil

# FSCT Output File Organizer
# Author: Tomáš Hanousek, hanousek.t@czechglobe.cz
# This script moves segmented LAS files from FSCT output folders to a consolidated directory
# for easier access and organization of forest point cloud data

# Define source and destination folders
# Example: source_folder = r"C:\forest_data\PLOT1\LAS"
# Example: destination_folder = r"C:\forest_data\PLOT1\processed"
source_folder = ""      # Source directory containing FSCT output folders
destination_folder = ""  # Destination directory for organized files

# Create destination folder if it does not exist
os.makedirs(destination_folder, exist_ok=True)

# Process folders from Pos0_FSCT_output to Pos68_FSCT_output
# Note: Range is 69 to include positions 0-68 (69 total positions)
for i in range(69):
    # Construct folder name following FSCT naming convention
    folder_name = f"Pos{i}_FSCT_output"
    
    # Define source file path (segmented.las file within each FSCT output folder)
    source_file = os.path.join(source_folder, folder_name, "segmented.las")
    
    # Define destination file path with renamed file for clarity
    destination_file = os.path.join(destination_folder, f"Pos{i}_FSCT.las")
   
    # Check if the source file exists before attempting to move it
    if os.path.exists(source_file):
        # Move file from source to destination with new name
        shutil.move(source_file, destination_file)
        print(f"✓ Moved: {source_file} -> {destination_file}")
    else:
        # Log missing files for debugging purposes
        print(f"✗ File not found: {source_file}")

print("\n Process completed successfully!")
print(f"Organized files are now available in: {destination_folder}")