import os
import sys

def find_rel_path(start_file, end_file):

    start_dir = os.path.dirname(start_file)
    end_dir = os.path.dirname(os.path.abspath(end_file))
    
    start_path = os.path.abspath(start_file)
    end_path = os.path.abspath(end_file)
    
    relative_path = os.path.relpath(start_dir, start=start_path)


    final_result = os.path.join(end_dir, end_file)

find_rel_path()
