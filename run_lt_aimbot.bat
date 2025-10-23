@echo off
REM LT Aimbot Launcher - Runs main.py with proper Python environment
setlocal

cd /d "%~dp0"

REM Try bundled Python first
set PYTHON_EXE=%~dp0python\python.exe

REM If bundled Python doesn't exist, try .venv
if not exist "%PYTHON_EXE%" (
    set PYTHON_EXE=%~dp0.venv\Scripts\python.exe
)

REM If .venv doesn't exist, try system Python
if not exist "%PYTHON_EXE%" (
    where python >nul 2>&1
    if errorlevel 1 (
        echo Error: Python not found!
        echo Please install Python or set up the virtual environment.
        pause
        exit /b 1
    )
    set PYTHON_EXE=python
)

echo Using Python: %PYTHON_EXE%

REM Install requirements if needed
if exist requirements.txt (
    echo Checking requirements...
    "%PYTHON_EXE%" -m pip install -q -r requirements.txt
)

REM Run the main script
echo Starting LT Aimbot...
"%PYTHON_EXE%" src\main.py

endlocal
pause
