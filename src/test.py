import motion
import window

process_name = "Label Traxx Client.exe"
process_path = "C:\Program Files\LT Client\Label Traxx Client.exe"
hwnd = window.get_hwnd(process_name)

# -- WINDOW -- 
# window.launch_program(process_path) -- works
# print(window.get_pid(process_name)) -- works
# print(window.get_titles(process_name)) -- works
# print(window.get_hwnds_from_pid(process_name)) -- works
# print(window.get_title()) -- works
# print(window.get_hwnd(process_name)) -- works
# window.wait_on_program(process_name) -- works
# print(window.detect_process(process_name)) -- works
# window.highlight_window(process_name) -- works
# window.toggle_window(process_name) -- works
# print(window.title_contains("Home Page", process_name)) -- works
# print(window.title_is_empty(process_name))
# window.highlight_console() -- works
# print(window.get_title_hwnd(hwnd)) -- works
# print(window.mark_hwnd()) -- works

# -- MOTION --
# motion.maneuver(process_name) -- works
# motion.capture_mouse_relative(hwnd) -- works
# motion.move_rel(hwnd, 500, 425) -- works
# motion.move_abs(1690, 454)

print(window.get_title_hwnd(hwnd))

# motion.capture_mouse_absolute(hwnd)
motion.move_abs(1472, 490, process_name)

#  motion necesseties
#  move coordinates rel and abs
#  caputre coordinates rel and abs
#  scale coordinates baesd on window size
