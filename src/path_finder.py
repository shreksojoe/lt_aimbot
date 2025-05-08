import os
import sys

def find_rel_path(start_file, end_file):
    # Convert to absolute paths if they aren't already
    start_file = os.path.abspath(start_file)
    end_file = os.path.abspath(end_file)
    
    # Get the directory of the start file
    start_dir = os.path.dirname(start_file)
    
    # Calculate the relative path FROM start_dir TO end_file
    relative_path = os.path.relpath(end_file, start=start_dir)
    
    print(f"Relative Path: {relative_path}")
    return relative_path
