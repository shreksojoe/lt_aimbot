# LT Aimbot Module Documentation

This document provides comprehensive documentation for the core modules of the LT Aimbot project: `motion.py`, `window.py`, and `data.py`. Each function has been analyzed for its actual implementation behavior, not just its comments.

## Table of Contents
- [motion.py](#motionpy)
- [window.py](#windowpy) 
- [data.py](#datapy)
- [Issues and Inconsistencies](#issues-and-inconsistencies)

---

## motion.py

#### `menuever(process_name)`
**Purpose**: Performs a sequence of window highlighting and input operations.
**Parameters**: `process_name` (str): Name of the target process

#### `capture_mouse_relative(hwnd)`
**Purpose**: Interactive coordinate capture tool for getting mouse positions relative to a window.
**Parameters**: `hwnd` (int): Window handle for coordinate reference
**Note**: Uses `keyboard.wait()` which blocks execution until key press.

#### `move_abs(x, y, process_name, retries=2)`
**Purpose**: Moves cursor to absolute screen coordinates and performs a click.
**Parameters**:
- `x, y` (int): Absolute screen coordinates
- `process_name` (str): Target process name
- `retries` (int): Number of retry attempts

**⚠️ Issue**: The function presses Enter before clicking, which may interfere with the intended click operation.

#### `move_rel(hwnd, x, y)`
**Purpose**: Moves cursor to coordinates relative to a window's position.
**Parameters**:
- `hwnd` (int): Window handle
- `x, y` (int): Coordinates relative to window's top-left corner

#### `adjust_to_screen(process_name, rel_x, rel_y)`
**Purpose**: Converts relative coordinates to absolute screen coordinates for the foreground window.

**Implementation**:
- Gets foreground window using `GetForegroundWindow()`
- Calculates absolute coordinates by adding window position to relative offset
- Returns the calculated absolute coordinates (does not move cursor)

**Parameters**:
- `process_name` (str): Process name (not actually used in implementation)
- `rel_x, rel_y` (int): Relative coordinates

**Returns**: Tuple of (abs_x, abs_y)

**⚠️ Issue**: The `process_name` parameter is not used in the function.

### Coordinate Conversion Functions

#### `coords_to_ratio(hwnd, x, y)`
**Purpose**: Converts pixel coordinates within a window's client area to normalized ratios (0.0-1.0).

**Implementation**:
- Gets client area dimensions using `GetClientRect()`
- Calculates ratios by dividing coordinates by client dimensions
- Validates window dimensions to prevent division by zero

**Parameters**:
- `hwnd` (int): Window handle
- `x, y` (int): Pixel coordinates within client area

**Returns**: Tuple of (x_ratio, y_ratio) as floats

#### `move_rel_normalized(hwnd, x_ratio, y_ratio)`
**Purpose**: Moves cursor to normalized position within a window's client area.

**Implementation**:
- Converts normalized ratios (0.0-1.0) to client pixel coordinates
- Applies global `OFFSET_Y_PX` vertical offset if set
- Converts client coordinates to screen coordinates using `ClientToScreen()`
- Brings target window to foreground before movement
- Uses `SetCursorPos()` for final movement

**Parameters**:
- `hwnd` (int): Window handle
- `x_ratio, y_ratio` (float): Normalized coordinates (0.0-1.0)

#### `move_rel_pixels(hwnd, x, y)`
**Purpose**: Moves cursor to specific pixel coordinates within a window's client area.

**Implementation**:
- Converts client coordinates to screen coordinates using `ClientToScreen()`
- Uses `SetCursorPos()` for movement
- Simple wrapper around Windows API calls

**Parameters**:
- `hwnd` (int): Window handle  
- `x, y` (int): Client area pixel coordinates

#### `coords_from_screen_to_ratio(hwnd, screen_x, screen_y)`
**Purpose**: Converts absolute screen coordinates to normalized ratios relative to a window's client area.

**Implementation**:
- Gets client area dimensions and origin in screen space
- Converts screen coordinates to client coordinates using `ScreenToClient()`
- Normalizes to ratios by dividing by client dimensions
- Includes detailed diagnostic output

**Parameters**:
- `hwnd` (int): Window handle
- `screen_x, screen_y` (int): Absolute screen coordinates

**Returns**: Tuple of (x_ratio, y_ratio) as floats

### Interactive Coordinate Collection

#### `collect_coords(hwnd)`
**Purpose**: Interactive tool for collecting multiple coordinate points with keyboard input.

**Implementation**:
- Uses pynput library for keyboard/mouse event handling
- Captures coordinates on Enter key press
- Exits on Escape key press
- Stores both screen coordinates and normalized ratios
- Returns list of captured coordinate pairs

**Parameters**:
- `hwnd` (int): Window handle for coordinate reference

**Returns**: List of tuples containing ((screen_x, screen_y), (ratio_x, ratio_y))

### Utility Functions

#### `get_client_size(hwnd)`
**Purpose**: Gets the dimensions of a window's client area.

**Implementation**:
- Uses `GetClientRect()` Windows API call
- Returns width and height as tuple

**Parameters**:
- `hwnd` (int): Window handle

**Returns**: Tuple of (width, height) in pixels

#### `get_window_rect(hwnd)`
**Purpose**: Gets the outer window rectangle including title bar and borders.

**Implementation**:
- Uses `GetWindowRect()` Windows API call
- Returns full window bounds

**Parameters**:
- `hwnd` (int): Window handle

**Returns**: Tuple of (left, top, right, bottom) coordinates

#### `get_client_origin_in_screen(hwnd)`
**Purpose**: Gets the screen coordinates of a window's client area top-left corner.

**Implementation**:
- Uses `ClientToScreen()` to convert (0,0) client coordinate to screen space
- Useful for calculating offsets between window and client areas

**Parameters**:
- `hwnd` (int): Window handle

**Returns**: Tuple of (x, y) screen coordinates

### Window Waiting Functions

#### `wait_for_window_title_contains(title_substring, timeout_seconds=30.0, poll_seconds=0.5)`
**Purpose**: Waits for the foreground window to have a title containing specific text.

**Implementation**:
- Polls foreground window title at specified intervals
- Uses `GetForegroundWindow()` and `GetWindowText()`
- Returns window handle when match found, None on timeout

**Parameters**:
- `title_substring` (str): Text that must be in window title
- `timeout_seconds` (float): Maximum wait time
- `poll_seconds` (float): Polling interval

**Returns**: Window handle (int) or None

#### `select_window_by_title(title_substring, timeout_seconds=30.0, focus_delay=0.25)`
**Purpose**: Waits for and selects a window by title substring with stability delay.

**Implementation**:
- Calls `wait_for_window_title_contains()`
- Adds configurable delay after window is found for UI stability
- Useful for waiting for dialogs to finish loading

**Parameters**:
- `title_substring` (str): Text that must be in window title
- `timeout_seconds` (float): Maximum wait time  
- `focus_delay` (float): Delay after window found

**Returns**: Window handle (int) or None

#### `set_current_window_by_title(title_substring, timeout_seconds=30.0)`
**Purpose**: Waits for a window by title and raises exception on timeout.

**Implementation**:
- Wrapper around `select_window_by_title()`
- Prints helpful status messages
- Raises `TimeoutError` if window not found within timeout

**Parameters**:
- `title_substring` (str): Text that must be in window title
- `timeout_seconds` (float): Maximum wait time

**Returns**: Window handle (int)
**Raises**: TimeoutError if window not found

### Advanced Coordinate Handling

#### `coords_to_ratios_general(hwnd, x, y, input_mode="auto")`
**Purpose**: Flexible coordinate conversion supporting multiple input formats.

**Implementation**:
- Supports multiple input modes: "auto", "ratio", "screen", "client", "window"
- Auto mode attempts to intelligently detect coordinate type
- Handles window chrome offsets for "window" mode
- Returns both converted ratios and detected/used mode

**Parameters**:
- `hwnd` (int): Window handle
- `x, y` (int/float): Input coordinates
- `input_mode` (str): Coordinate interpretation mode

**Returns**: Tuple of ((x_ratio, y_ratio), mode_used)

**Modes**:
- "ratio": Input already normalized (0.0-1.0)
- "client": Pixels relative to client area
- "screen": Absolute screen coordinates  
- "window": Pixels relative to outer window
- "auto": Automatic detection

#### `move_window_pixels(hwnd, x, y)`
**Purpose**: Moves cursor to coordinates relative to outer window (including title bar).

**Implementation**:
- Gets window rectangle and adds offset to window's top-left
- Allows targeting title bar and border areas
- Uses `SetCursorPos()` for movement

**Parameters**:
- `hwnd` (int): Window handle
- `x, y` (int): Coordinates relative to window's outer rectangle

#### `move_screen_pixels(hwnd, screen_x, screen_y)`
**Purpose**: Moves cursor to absolute screen coordinates.

**Implementation**:
- Direct wrapper around `SetCursorPos()`
- hwnd parameter ignored (kept for API consistency)
- Includes error checking and diagnostic output

**Parameters**:
- `hwnd` (int): Window handle (unused)
- `screen_x, screen_y` (int): Absolute screen coordinates

#### `move_to_input_coords(hwnd, x, y, input_mode="auto")`
**Purpose**: Universal coordinate movement function supporting all input types.

**Implementation**:
- Handles special modes "window_abs" and "screen_abs" directly
- For other modes, converts to ratios then calls `move_rel_normalized()`
- Provides unified interface for all coordinate movement operations

**Parameters**:
- `hwnd` (int): Window handle
- `x, y` (int/float): Input coordinates
- `input_mode` (str): Coordinate interpretation mode

**Special Modes**:
- "window_abs": Direct window-relative pixels
- "screen_abs": Direct screen coordinates
- All other modes converted via `coords_to_ratios_general()`

---

## window.py

This module provides window management functionality, including process detection, window enumeration, and window manipulation using Windows API calls.

### Process Information Functions

#### `get_pid(process_name)`
**Purpose**: Retrieves the process ID for a given process name.
**Parameters**: `process_name` (str): Name of the process executable
**Returns**: Process ID (int) or False if not found

#### `get_titles(process_name)`
**Purpose**: Gets all window titles for a given process.
**Parameters**: `process_name` (str): Name of the process executable
**Returns**: List of window titles (strings) or error message if process not running

#### `get_hwnds_from_pid(process_name)`
**Purpose**: Gets all window handles for a given process.
**Parameters**: `process_name` (str): Name of the process executable
**Returns**: List of window handles (integers)

#### `get_title(process_name)`
**Purpose**: Gets the title of the currently foreground window.
**Returns**: Current foreground window title (string)

#### `get_hwnd(process_name)`
**Purpose**: Gets a representative window handle for a process.
**Parameters**: `process_name` (str): Name of the process executable
**Returns**: Window handle (int) or None if not found

#### `wait_on_program(process_name)`
**Purpose**: Waits for a program to finish loading (when foreground window title becomes empty).
**Parameters**: `process_name` (str): Process name (not actually used in implementation)

#### `launch_program(process_path)`
**Purpose**: Launches a program and waits for it to finish loading.
**Parameters**: `process_path` (str): Full path to executable

#### `detect_process(process_name)`
**Purpose**: Checks if a process is currently running.
**Parameters**: `process_name` (str): Name of the process executable
**Returns**: Boolean (True if running, False if not)

### Window Manipulation Functions

#### `highlight_window(process_name)`
**Purpose**: Brings a process window to the foreground and restores it if minimized.
**Parameters**: `process_name` (str): Name of the process executable
**Returns**: False if process not running or window can't be toggled

#### `toggle_window(process_name, iterations=1)`
**Purpose**: Switches between multiple windows of the same process.
**Parameters**:
- `process_name` (str): Name of the process executable
- `iterations` (int): Index of window to switch to (default 1)
**Returns**: False if not enough windows or window can't be toggled
**Note**: Only works if windows have different titles.

#### `title_contains(process_name, text)`
**Purpose**: Checks if the current foreground window title contains specific text.
**Parameters**:
- `process_name` (str): Process name (passed to `get_title()` but not used)
- `text` (str): Text to search for in title
**Returns**: Boolean (True if text found in title)

#### `title_is_empty(process_name)`
**Purpose**: Checks if the window title is empty after removing spaces.
**Parameters**: `process_name` (str): Name of the process executable
**Returns**: Boolean (True if title exists after space removal, False if empty)

#### `highlight_console(hwnd=None)`
**Purpose**: Brings the console window to the foreground.
**Parameters**: `hwnd` (int, optional): Console window handle (auto-detected if None)

#### `get_title_hwnd(hwnd)`
**Purpose**: Gets and prints the title of a specific window handle.
**Parameters**: `hwnd` (int): Window handle
**Returns**: Window title (string)

#### `mark_hwnd()`
**Purpose**: Gets and prints the handle of the current foreground window.
**Returns**: Current foreground window handle (int)

---

## data.py

This module provides data processing and file management utilities, focusing on date standardization and intelligent file path resolution.

### Date Processing Functions

#### `standardize_date(date_str)`
**Purpose**: Converts various date formats to standardized MM/DD/YYYY format.

**Implementation**:
- Handles None input by returning empty string
- Normalizes ISO-like formats by replacing 'T' with space and taking date part only
- Tries multiple date formats with different separators ('/', '-', '.', ' ')
- Supports both 2-digit and 4-digit years
- Supports different date component orders (MM/DD/YYYY, DD/MM/YYYY, YYYY/MM/DD)
- Uses comprehensive format list with explicit common formats
- Returns original input if no format matches (prevents pipeline breakage)

**Parameters**:
- `date_str` (str/None): Input date string in various formats

**Returns**: Standardized date string in MM/DD/YYYY format or original input if unparseable

**Supported Formats**:
- ISO format: 2025-09-26
- US format: 09/26/2025, 09/26/25  
- European format: 26/09/2025, 26/09/25
- Various separators: /, -, ., space
- With or without time components (time is stripped)

### File Path Resolution Functions

#### `_search_same_drive(filename, base_path)`
**Purpose**: Last-resort search for a file anywhere on the same drive as base_path.

**Implementation**:
- Determines drive root from base_path (e.g., 'C:\\')
- Performs recursive directory traversal using `os.walk()`
- Prunes common system directories to improve performance:
  - Windows, Program Files, Program Files (x86), ProgramData
  - $Recycle.Bin, System Volume Information, AppData, Microsoft OneDrive
- Performs case-insensitive filename matching
- Returns first match found

**Parameters**:
- `filename` (str): Name of file to search for
- `base_path` (Path): Path object to determine drive for search

**Returns**: Path object of found file or None if not found

**Note**: This is a performance-intensive operation and should only be used as a last resort.

#### `find_abs_path(filename, extra_paths=None)`
**Purpose**: Comprehensive file resolution that searches multiple locations in priority order.

**Implementation**:
Searches in the following order:
1. **Absolute path**: If filename is absolute and exists, return it
2. **Current working directory**: Check if file exists in CWD
3. **Script directory**: Same directory as the current Python script
4. **Extra paths**: Any additional paths provided via parameter
5. **System install paths**: Program Files directories on Windows
   - Also searches one level deeper in subdirectories
6. **Drive search**: Last resort full drive search using `_search_same_drive()`

**Parameters**:
- `filename` (str): Name or path of file to find
- `extra_paths` (list, optional): Additional directories to search

**Returns**: Absolute Path object if file found, None otherwise

**Platform-specific behavior**:
- Windows: Searches Program Files and Program Files (x86)
- Uses environment variables to locate system directories
- Handles cases where environment variables don't exist

#### `find_rel_path(filename)`
**Purpose**: Finds a file and returns its path relative to the current working directory.

**Implementation**:
- Uses `find_abs_path()` to locate the file
- Converts absolute path to relative path using `relative_to()`
- Falls back to `os.path.relpath()` if file is on different drive or outside CWD tree
- Handles cross-drive scenarios gracefully

**Parameters**:
- `filename` (str): Name of file to find

**Returns**: Relative Path object from CWD to file, or None if file not found

**Note**: The commented-out code at the end shows an alternative implementation using `os.walk()` that was replaced by the more robust `find_abs_path()` approach.

---

## Issues and Inconsistencies

### Critical Issues Found

1. **motion.py - `move_abs()` function**:
   - **Issue**: Presses Enter key before performing click, which may interfere with the intended click operation
   - **Location**: Line 150 - `pyautogui.press("enter")`
   - **Impact**: Could cause unexpected behavior in automated clicking sequences

2. **window.py - `get_title()` function**:
   - **Issue**: `process_name` parameter is not used; always returns foreground window title
   - **Location**: Lines 63-71
   - **Impact**: Function doesn't behave as name suggests; misleading API

3. **window.py - `wait_on_program()` function**:
   - **Issue**: `process_name` parameter is not used; only checks foreground window
   - **Location**: Lines 109-117  
   - **Impact**: Function doesn't actually wait for specific program

4. **window.py - `title_is_empty()` function**:
   - **Issue**: Function name is misleading; returns True when title is NOT empty
   - **Location**: Lines 185-193
   - **Impact**: Confusing API that could lead to logic errors

5. **motion.py - `adjust_to_screen()` function**:
   - **Issue**: `process_name` parameter is not used in implementation
   - **Location**: Lines 180-192
   - **Impact**: Misleading function signature

### Design Concerns

1. **Inconsistent Error Handling**: Some functions return False/None on error, others raise exceptions
2. **Mixed Coordinate Systems**: Multiple coordinate systems (screen, client, window, normalized) without clear documentation of which functions expect which
3. **Global State**: `OFFSET_Y_PX` global variable affects coordinate calculations without clear indication
4. **Blocking Operations**: Some functions use blocking keyboard input that could hang the application

### Recommendations

1. **Fix Parameter Usage**: Remove unused parameters or implement their intended functionality
2. **Standardize Error Handling**: Use consistent error handling patterns across all functions
3. **Add Input Validation**: Validate coordinate ranges and window handle validity
4. **Improve Function Names**: Rename misleading functions like `title_is_empty()`
5. **Add Type Hints**: Include proper type annotations for better code maintainability
6. **Document Coordinate Systems**: Clearly document which coordinate system each function expects and returns

---

*Documentation generated by analyzing actual code implementation, not just comments.*
