import os
import sys
import json
import time
import shutil
import tempfile
import subprocess
import traceback
import logging
from pathlib import Path
import urllib.request
import zipfile
import hashlib
import ctypes
from datetime import datetime

# Setup logging
log_dir = Path(os.environ.get('APPDATA')) / "LT Aimbot" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"updater_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Constants
APP_NAME = "LT Aimbot"
GITHUB_REPO = "yourusername/lt_aimbot"  # Replace with your actual GitHub username/repo
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
BACKUP_DIR = Path(os.environ.get('APPDATA')) / APP_NAME / "backups"
INSTALL_DIR = Path(os.path.dirname(os.path.abspath(sys.executable)))
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    INSTALL_DIR = Path(os.path.dirname(os.path.abspath(sys.executable)))
else:
    # Running as script
    INSTALL_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

VERSION_FILE = INSTALL_DIR / "version.json"
MAIN_EXE = INSTALL_DIR / "main.exe"
UPDATE_FLAG_FILE = INSTALL_DIR / "update_in_progress.flag"
SILENT_MODE = "--silent" in sys.argv

def is_admin():
    """Check if the script is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def run_as_admin():
    """Re-run the script with admin privileges"""
    if not is_admin():
        logging.info("Requesting admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)

def show_message(title, message, style=0):
    """Show a message box to the user"""
    if not SILENT_MODE:
        return ctypes.windll.user32.MessageBoxW(0, message, title, style)
    else:
        logging.info(f"{title}: {message}")
        return 1  # Simulate "OK" button press

def get_current_version():
    """Get the current installed version from version.json"""
    try:
        if VERSION_FILE.exists():
            with open(VERSION_FILE, 'r') as f:
                data = json.load(f)
                return data.get('version', '0.0.0')
        return '0.0.0'
    except Exception as e:
        logging.error(f"Error reading current version: {e}")
        return '0.0.0'

def get_latest_version_info():
    """Get the latest version info from GitHub releases"""
    try:
        headers = {'User-Agent': 'LT-Aimbot-Updater/1.0'}
        req = urllib.request.Request(GITHUB_API_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            version = data['tag_name'].lstrip('v')
            download_url = None
            
            # Find the asset that contains our executable
            for asset in data['assets']:
                if asset['name'].endswith('.zip'):
                    download_url = asset['browser_download_url']
                    break
            
            return {
                'version': version,
                'download_url': download_url,
                'release_notes': data['body'],
                'published_at': data['published_at']
            }
    except Exception as e:
        logging.error(f"Error checking for updates: {e}")
        return None

def version_is_newer(current, latest):
    """Compare version strings to determine if latest is newer than current"""
    def parse_version(v):
        return [int(x) for x in v.split('.')]
    
    try:
        current_parts = parse_version(current)
        latest_parts = parse_version(latest)
        
        for i in range(max(len(current_parts), len(latest_parts))):
            current_part = current_parts[i] if i < len(current_parts) else 0
            latest_part = latest_parts[i] if i < len(latest_parts) else 0
            
            if latest_part > current_part:
                return True
            elif latest_part < current_part:
                return False
        
        return False  # Versions are equal
    except Exception as e:
        logging.error(f"Error comparing versions: {e}")
        return False

def backup_current_version():
    """Create a backup of the current installation"""
    try:
        current_version = get_current_version()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{current_version}_{timestamp}"
        backup_path = BACKUP_DIR / backup_name
        
        # Create backup directory
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup_path.mkdir(exist_ok=True)
        
        # Copy all files except the updater itself
        for item in INSTALL_DIR.iterdir():
            if item.name != "updater.exe" and item.name != "updater":
                if item.is_file():
                    shutil.copy2(item, backup_path / item.name)
                elif item.is_dir():
                    shutil.copytree(item, backup_path / item.name)
        
        logging.info(f"Backup created at {backup_path}")
        return backup_path
    except Exception as e:
        logging.error(f"Error creating backup: {e}")
        return None

def download_update(url, version):
    """Download the update package from the provided URL"""
    try:
        temp_dir = Path(tempfile.mkdtemp())
        zip_path = temp_dir / f"update_{version}.zip"
        
        logging.info(f"Downloading update from {url}...")
        
        # Download with progress reporting
        with urllib.request.urlopen(url) as response, open(zip_path, 'wb') as out_file:
            total_size = int(response.info().get('Content-Length', 0))
            downloaded = 0
            block_size = 8192
            
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                
                downloaded += len(buffer)
                out_file.write(buffer)
                
                # Update progress
                if total_size > 0 and not SILENT_MODE:
                    done = int(50 * downloaded / total_size)
                    sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded}/{total_size} bytes")
                    sys.stdout.flush()
        
        if not SILENT_MODE:
            print()  # New line after progress bar
        
        logging.info(f"Download completed: {zip_path}")
        return temp_dir, zip_path
    except Exception as e:
        logging.error(f"Error downloading update: {e}")
        return None, None

def verify_update_package(zip_path):
    """Verify the integrity of the downloaded update package"""
    try:
        if not zipfile.is_zipfile(zip_path):
            logging.error("Downloaded file is not a valid ZIP archive")
            return False
        
        # Check if the zip contains the expected files
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            # Check for main executable or folder structure
            if not any(f.endswith('.exe') for f in file_list) and not any('main.exe' in f for f in file_list):
                logging.error("Update package does not contain expected executable")
                return False
        
        logging.info("Update package verification passed")
        return True
    except Exception as e:
        logging.error(f"Error verifying update package: {e}")
        return False

def install_update(zip_path, version):
    """Extract and install the update from the ZIP file"""
    try:
        # Create a flag file to indicate update in progress
        with open(UPDATE_FLAG_FILE, 'w') as f:
            f.write(f"Update to version {version} started at {datetime.now().isoformat()}")
        
        extract_dir = Path(tempfile.mkdtemp())
        
        # Extract the update package
        logging.info(f"Extracting update to {extract_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find the main directory in the extracted content
        main_dir = extract_dir
        for item in extract_dir.iterdir():
            if item.is_dir() and any((item / subdir).exists() for subdir in ['main.exe', 'dist']):
                main_dir = item
                break
        
        # Copy files to installation directory
        logging.info(f"Installing files to {INSTALL_DIR}...")
        for item in main_dir.iterdir():
            target = INSTALL_DIR / item.name
            
            # Skip updater files to prevent replacing the running executable
            if item.name == "updater.exe" or item.name == "updater":
                continue
                
            if item.is_file():
                # Try multiple times in case of file locks
                for attempt in range(3):
                    try:
                        shutil.copy2(item, target)
                        break
                    except PermissionError:
                        if attempt < 2:
                            time.sleep(1)
                        else:
                            raise
            elif item.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(item, target)
        
        # Update version file
        with open(VERSION_FILE, 'r') as f:
            version_data = json.load(f)
        
        version_data['version'] = version
        version_data['releaseDate'] = datetime.now().strftime("%Y-%m-%d")
        
        with open(VERSION_FILE, 'w') as f:
            json.dump(version_data, f, indent=2)
        
        # Remove the update flag file
        if UPDATE_FLAG_FILE.exists():
            UPDATE_FLAG_FILE.unlink()
        
        logging.info(f"Update to version {version} completed successfully")
        return True
    except Exception as e:
        logging.error(f"Error installing update: {e}")
        traceback.print_exc()
        return False

def restore_backup(backup_path):
    """Restore from backup if update fails"""
    try:
        logging.info(f"Restoring from backup {backup_path}...")
        
        for item in backup_path.iterdir():
            target = INSTALL_DIR / item.name
            
            # Skip updater files
            if item.name == "updater.exe" or item.name == "updater":
                continue
                
            if item.is_file():
                shutil.copy2(item, target)
            elif item.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(item, target)
        
        logging.info("Backup restoration completed")
        return True
    except Exception as e:
        logging.error(f"Error restoring backup: {e}")
        return False

def cleanup(temp_dir):
    """Clean up temporary files"""
    try:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)
    except Exception as e:
        logging.error(f"Error cleaning up: {e}")

def check_for_updates(silent=False):
    """Main function to check for and apply updates"""
    global SILENT_MODE
    SILENT_MODE = silent
    
    try:
        logging.info("Starting update check...")
        
        # Check if an update is already in progress
        if UPDATE_FLAG_FILE.exists():
            logging.warning("Update already in progress. Exiting.")
            show_message("Update in Progress", 
                         "Another update is already in progress. Please wait for it to complete.", 
                         0x30)  # MB_ICONWARNING
            return False
        
        current_version = get_current_version()
        logging.info(f"Current version: {current_version}")
        
        latest_info = get_latest_version_info()
        if not latest_info or not latest_info.get('download_url'):
            logging.error("Could not retrieve latest version information")
            if not silent:
                show_message("Update Error", 
                             "Could not check for updates. Please check your internet connection.", 
                             0x10)  # MB_ICONERROR
            return False
        
        latest_version = latest_info['version']
        logging.info(f"Latest version: {latest_version}")
        
        if not version_is_newer(current_version, latest_version):
            logging.info("Already running the latest version")
            if not silent:
                show_message("No Updates Available", 
                             f"You are already running the latest version ({current_version}).", 
                             0x40)  # MB_ICONINFORMATION
            return False
        
        # Ask user if they want to update
        if not silent:
            user_choice = show_message("Update Available", 
                                      f"A new version ({latest_version}) is available. Your current version is {current_version}.\n\n" +
                                      f"Release notes:\n{latest_info['release_notes'][:500]}...\n\n" +
                                      "Would you like to update now?", 
                                      0x24)  # MB_YESNO | MB_ICONQUESTION
            
            if user_choice != 6:  # IDYES = 6
                logging.info("User declined the update")
                return False
        
        # Create backup
        backup_path = backup_current_version()
        if not backup_path:
            if not silent:
                show_message("Update Error", 
                             "Failed to create backup. Update aborted.", 
                             0x10)  # MB_ICONERROR
            return False
        
        # Download update
        temp_dir, zip_path = download_update(latest_info['download_url'], latest_version)
        if not zip_path:
            if not silent:
                show_message("Update Error", 
                             "Failed to download update. Update aborted.", 
                             0x10)  # MB_ICONERROR
            return False
        
        # Verify update package
        if not verify_update_package(zip_path):
            if not silent:
                show_message("Update Error", 
                             "The downloaded update package is invalid or corrupted. Update aborted.", 
                             0x10)  # MB_ICONERROR
            cleanup(temp_dir)
            return False
        
        # Install update
        success = install_update(zip_path, latest_version)
        if not success:
            logging.error("Update installation failed, attempting to restore from backup")
            restore_success = restore_backup(backup_path)
            
            if not silent:
                if restore_success:
                    show_message("Update Failed", 
                                 "Update installation failed. Your previous version has been restored.", 
                                 0x30)  # MB_ICONWARNING
                else:
                    show_message("Critical Error", 
                                 "Update failed and backup restoration also failed. The application may be in an inconsistent state.", 
                                 0x10)  # MB_ICONERROR
            
            cleanup(temp_dir)
            return False
        
        # Clean up
        cleanup(temp_dir)
        
        if not silent:
            show_message("Update Complete", 
                         f"Update to version {latest_version} completed successfully. The application will now restart.", 
                         0x40)  # MB_ICONINFORMATION
        
        # Restart the main application
        try:
            subprocess.Popen([str(MAIN_EXE)])
        except Exception as e:
            logging.error(f"Failed to restart application: {e}")
        
        return True
        
    except Exception as e:
        logging.error(f"Unexpected error during update: {e}")
        traceback.print_exc()
        
        if not silent:
            show_message("Update Error", 
                         f"An unexpected error occurred during the update process: {str(e)}", 
                         0x10)  # MB_ICONERROR
        return False

if __name__ == "__main__":
    try:
        # Check if admin rights are needed for the update
        if "--admin" in sys.argv:
            run_as_admin()
        
        silent_mode = "--silent" in sys.argv
        check_for_updates(silent_mode)
        
    except Exception as e:
        logging.error(f"Critical error: {e}")
        traceback.print_exc()
        if not silent_mode:
            show_message("Critical Error", 
                         f"A critical error occurred in the updater: {str(e)}", 
                         0x10)  # MB_ICONERROR
