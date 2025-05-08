import os
import sys

def find_rel_path(start_file, end_file):
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # If start_file is 'src', we're looking for a file within the src directory
    if start_file == "src":
        # Just use the current directory (which is the src directory)
        base_dir = current_dir
    else:
        # Navigate up to the parent directory for other cases
        base_dir = os.path.dirname(current_dir)
    
    # Create the absolute path to the target file
    absolute_path = os.path.join(base_dir, end_file)
    
    print(f"Relative Path: {end_file}")
    return absolute_path
