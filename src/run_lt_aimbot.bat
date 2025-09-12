@echo off
REM Use bundled Python from dist\python
setlocal
set PYTHON_EXE=%~dp0python\python.exe

if not exist "%PYTHON_EXE%" (
    echo Bundled Python not found! Please reinstall the app.
    pause
    exit /b 1
)

echo Using bundled Python: %PYTHON_EXE%

if exist requirements.txt goto install

echo requirements.txt not found.
goto runmain

:install
echo requirements.txt found.
call "%PYTHON_EXE%" -m pip install --upgrade pip
call "%PYTHON_EXE%" -m pip install -r requirements.txt

:runmain
REM Run the main script
call "%PYTHON_EXE%" \main.py

endlocal
pause
