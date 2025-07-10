python -m venv venv
venv\Scripts\activate
pip install pyinstaller
pyinstaller --onefile src\main.py
