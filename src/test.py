import motion
import window
import data

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
# motion.capture_mouse_relative(hwnd)
# motion.move_rel(hwnd, 912, 654) -- works
# motion.move_abs(1571, 842) -- works
# motion.capture_mouse_absolute(hwnd) -- works

# -- DATA --
# print(data.find_rel_path("run_lt_aimbot.bat")) -- works

# print(data.find_abs_path(process_name)) -- works
data.address_search("Grainger Dropship Acct")

# dates = ["2025-09-29", "29-09-2025", "09/29/2025", "2025-09-29 14:35:07", "2025-09-29T14:35:07Z", "2025-09-29T14:35:07+00:00", "09/29/2025 2:35 PM", "29-09-2025 14:35"]
# 
# for date in dates:
#     # print("before date: ", date)
#     after_date = data.standardize_date(date) -- works
#     print("after date: ", after_date)
