import os

# OBJ Coordinate System Converter
# Author: Tomáš Hanousek, hanousek.t@czechglobe.cz
# This script converts OBJ files from XYZ to XZY coordinate system and centers them at origin
# Useful for preparing 3D tree models for analysis or visualization in different coordinate systems

def convert_obj_xyz_to_xzy(input_path, output_path):
    """
    Convert OBJ file from XYZ to XZY coordinate system and center at origin
    
    Args:
        input_path: Path to input OBJ file
        output_path: Path to output OBJ file
    """
    vertices = []
    faces = []
    
    with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
        # Write standard OBJ header to the output file
        output_file.write("# Blender v4.3 (sub 0) OBJ File: ''\n")
        output_file.write("# www.blender.org\n")
        output_file.write("g AdQSM_wooden_skeleton\n")
        
        # Process each line of the input file
        for line in input_file:
            # Split the line into parts to process vertices and faces
            parts = line.strip().split()
           
            # Process vertex lines that start with 'v'
            if len(parts) > 0 and parts[0] == 'v':
                # Extract the x, y, z coordinates
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
               
                # Store the reordered coordinates (x, z, y) - converting XYZ to XZY
                vertices.append((x, z, y))
            elif len(parts) > 0 and parts[0] == 'f':
                # Store face definitions unchanged
                faces.append(parts)
           
        # Apply transformations to center the model
        # Move the vertices so that the bottom is at the origin (Y=0)
        move_bottom_to_origin(vertices)
       
        # Move the vertices so that the lowest point is centered at XZ (0,0)
        move_lowest_xz_to_origin(vertices)
       
        # Write the modified vertices to the output file
        for vertex in vertices:
            output_file.write(f'v {vertex[0]} {vertex[1]} {vertex[2]}\n')
       
        # Write the faces to the output file unchanged
        for face in faces:
            output_file.write(' '.join(face) + '\n')

def move_bottom_to_origin(vertices):
    """
    Move all vertices so that the bottom (minimum Y) is at Y=0
    
    Args:
        vertices: List of vertex tuples (x, y, z) to modify in-place
    """
    if not vertices:
        return
   
    # Find the minimum y value (since the y coordinate is now in the second position after XZY conversion)
    min_y = min(vertex[1] for vertex in vertices)
   
    # Shift all vertices so that the bottom is at y = 0
    for i in range(len(vertices)):
        vertices[i] = (
            vertices[i][0],
            vertices[i][1] - min_y,  # Subtract minimum Y to move bottom to origin
            vertices[i][2]
        )

def move_lowest_xz_to_origin(vertices):
    """
    Move all vertices so that the lowest point (trunk base) is centered at X=0, Z=0
    
    Args:
        vertices: List of vertex tuples (x, y, z) to modify in-place
    """
    if not vertices:
        return
   
    # Find the vertex with the lowest y value (trunk base)
    lowest_vertex = min(vertices, key=lambda v: v[1])
    lowest_x = lowest_vertex[0]
    lowest_z = lowest_vertex[2]
   
    # Shift all vertices so that the lowest point is centered at x = 0, z = 0
    for i in range(len(vertices)):
        vertices[i] = (
            vertices[i][0] - lowest_x,  # Center X coordinate
            vertices[i][1],             # Keep Y unchanged
            vertices[i][2] - lowest_z   # Center Z coordinate
        )

def process_folder(input_folder_path, output_folder_path):
    """
    Process all OBJ files in the specified folders
    
    Args:
        input_folder_path: Path to folder containing input OBJ files
        output_folder_path: Path to folder for output OBJ files
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder_path, exist_ok=True)
    
    # Process all OBJ files in the input folder
    processed_count = 0
    for file_name in os.listdir(input_folder_path):
        if file_name.endswith('.obj'):
            input_file_path = os.path.join(input_folder_path, file_name)
            output_file_path = os.path.join(output_folder_path, file_name)
            
            try:
                convert_obj_xyz_to_xzy(input_file_path, output_file_path)
                processed_count += 1
                print(f"Converted: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")
   
    print(f"Conversion complete! Processed {processed_count} files.")

# Define input and output directories
# Example: input_folder = r"C:\3D_models\input_obj_files"
# Example: output_folder = r"C:\3D_models\converted_obj_files"
input_folder = ""   # Directory containing input OBJ files
output_folder = ""  # Directory for converted OBJ files

# Run the conversion
if __name__ == "__main__":
    if input_folder and output_folder:
        print("Starting OBJ file conversion...")
        process_folder(input_folder, output_folder)
    else:
        print("Please set the input_folder and output_folder paths in the script.")