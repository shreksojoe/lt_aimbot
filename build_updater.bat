@echo off
echo Building updater executable...

REM Navigate to the installation directory (current directory when run by installer)
cd %~dp0

REM Build the updater executable using PyInstaller with optimizations
python -m pip install pyinstaller
python -m PyInstaller --onedir --windowed --clean --name updater --strip --hide-console=hide-early src\updater.py

REM Move the built folder to the app directory
xcopy /E /I dist\updater %~dp0updater\

REM Create a shortcut to the updater executable
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%~dp0updater.lnk'); $Shortcut.TargetPath = '%~dp0updater\updater.exe'; $Shortcut.Save()"

echo Updater build completed successfully!
