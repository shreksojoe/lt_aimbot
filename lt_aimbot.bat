@echo off
REM LT Aimbot Launcher
REM This batch file launches the application using the embedded Python

REM Set Python path to the installation directory
set PYTHONPATH=%~dp0

REM Launch the application with the embedded Python
"%~dp0python\python.exe" "%~dp0main.py" %*
