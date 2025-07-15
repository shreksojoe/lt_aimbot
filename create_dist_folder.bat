@echo off
echo Creating manual distribution folder structure...

REM Create distribution folder structure
mkdir dist\lt_aimbot 2>nul

REM Copy the main script
copy main.py dist\lt_aimbot\

REM Copy the version file (important for updater)
copy version.json dist\lt_aimbot\

REM Copy the source folder (containing xlsx_to_csv.py)
mkdir dist\lt_aimbot\src 2>nul
copy src\*.py dist\lt_aimbot\src\

REM Create a simple batch launcher
echo @echo off > dist\lt_aimbot\lt_aimbot.bat
echo python main.py %%* >> dist\lt_aimbot\lt_aimbot.bat

echo.
echo Distribution folder created at dist\lt_aimbot
echo.
