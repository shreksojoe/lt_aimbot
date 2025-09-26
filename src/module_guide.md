## data.py
    standardize_date(date_str)
    - for standardizing date to %m/%d/%Y

    find_abs_path(filename, extra_paths=None):
    - input file, output absolute path for that file

    find_rel_path(filename):
    - input file name, get relative path to that file from the same directory the function is called from

## window.py
    get_pid(process_name)
    - input process name, output pid
    
    get_titles(process_name)
    - input process name, output all titles of jjthat process

    get_hwnds_from_pid(process_name)
    - input process name, output window handles (captured using pid)

    get_hwnd(process_name)  
    - get's the top-level hwnd from process_name

    launch_program(process_path)
    - input process path, it will launch the exe

    detect_process(process_name)
    - input process_name, return boolean

    highlight_window(process_name)
    - input process_name, highlight

    toggle_window(process_name, iterations=1)
    - default, is toggle between 2 windows of the same process, can change the iterations if there is more than 2 windows
    
    title_contians(process_name, text)
    - input process name, and text. Will return a boolean for whether or not that text is in the title of the process_name

    title_is_empty(process_name)
    - returns boolean for whether or not the title is empty (input process_name)

    get_title_hwnd(hwnd)
    - get the title of the hwnd, that is passed in

    mark_hwnd():
    - get the hwnd of the currently selected window


## motion.py

    menuever(process_name)
    - toggles between to console from the top window, to hit enter, and toggle back

    capture_mouse_relative(hwnd) 
    - HMMM one of the many captureing mouse coordinates functions that is rather suss imo

    move_abs(x, y, process_name, retries=2)
    - moving the mouse to absolute coords, with an attempt on the retry functionality

    move_rel(hwnd, x, y)
    - move the mouse relative to the window (presumably)

    adjust_to_screen(process_name, rel_x, rel_y)
    - takes relative coordinates, as well as the process name, and scales them based off of the screen

    coords_to_ratio(hwnd, x, y)
    - translates x, y coords to a ratio relative to the hwnd

    move_rel_normalized(hwnd, x_ratio, y_ratio)
    - relative, but to the client area of the window

    move_rel_pixels
    - another relative thing but something to do with pixels

    coords_from_screen_to_ratio
    - convets screen coords to ratios relative to the client area

    
