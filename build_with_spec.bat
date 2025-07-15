@echo off
echo Building LT Aimbot with spec file...

REM Clean previous builds if they exist
if exist "dist\lt_aimbot" rmdir /s /q "dist\lt_aimbot"
if exist "build" rmdir /s /q "build"

REM Run PyInstaller with the spec file
pyinstaller lt_aimbot.spec

echo.
if %ERRORLEVEL% EQU 0 (
    echo Build completed successfully!
    echo Output is in dist\lt_aimbot\
) else (
    echo Build failed with error code %ERRORLEVEL%
)
echo.
