@echo off
REM Grainger PO TXT to CSV Converter Launcher
REM This batch file runs the txt_to_csv.py script from the root folder

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Run the converter with interactive menu if no arguments provided
if "%~1"=="" (
    python src\txt_to_csv.py
) else (
    REM Pass all arguments to the script
    python src\txt_to_csv.py %*
)

pause
