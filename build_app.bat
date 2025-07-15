@echo off
echo Building LT Aimbot application in one-folder mode...

REM Clean previous builds
if exist dist\lt_aimbot rmdir /s /q dist\lt_aimbot
if exist build rmdir /s /q build

REM Build the application using PyInstaller one-folder mode
python -m PyInstaller ^
  --name lt_aimbot ^
  --onedir ^
  --windowed ^
  --clean ^
  --strip ^
  --hide-console=hide-early ^
  --exclude-module=pytest ^
  --exclude-module=unittest ^
  --exclude-module=doctest ^
  --exclude-module=pdb ^
  --exclude-module=tkinter.test ^
  --exclude-module=matplotlib ^
  --exclude-module=IPython ^
  --exclude-module=PIL.ImageQt ^
  --add-data "version.json;." ^
  --additional-hooks-dir=hooks ^
  main.py

REM Copy version.json to dist folder (just to be sure)
copy version.json dist\lt_aimbot\

echo Build completed! Output in dist\lt_aimbot
