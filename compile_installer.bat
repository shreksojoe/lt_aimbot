@echo off
echo Compiling Inno Setup installer...

REM Try to find ISCC.exe in its default installation path
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "%~dp0installer.iss"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    "C:\Program Files\Inno Setup 6\ISCC.exe" "%~dp0installer.iss"
) else (
    echo ERROR: Could not find Inno Setup Compiler.
    echo Please install Inno Setup or check its installation path.
    exit /b 1
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Installer compilation completed successfully!
    echo Output should be in the "installer_output" folder.
) else (
    echo.
    echo Installer compilation failed with error code %ERRORLEVEL%.
)
echo.
