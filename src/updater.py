import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
import tempfile
import time
import logging
import shutil
import winreg
import ctypes
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
APP_NAME = "LT AIMBOT"
GITHUB_USERNAME = "shreksojoe"
GITHUB_REPO = "lt_aimbot"
VERSION_FILE = "version.json"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/releases/latest"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/main/{VERSION_FILE}"
USER_AGENT = "Mozilla/5.0"
TEMP_DIRECTORY = tempfile.gettempdir()


def show_message(title, message, is_question=False):
    """Show a message box to the user"""
    flags = 0x4 if is_question else 0x40  # 0x4 = Yes/No, 0x40 = Information
    result = ctypes.windll.user32.MessageBoxW(0, message, title, flags)
    return result == 6  # 6 = Yes


def is_admin():
    """Check if the current user has administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def get_install_location():
    """Get the installation location from the Windows registry"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"SOFTWARE\\{APP_NAME}") as key:
            install_path = winreg.QueryValueEx(key, "InstallLocation")[0]
            return install_path
    except:
        # If registry key not found, try to find the executable location
        return os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)))


def get_current_version():
    """Get the current version from the local version.json file"""
    try:
        install_dir = get_install_location()
        version_path = os.path.join(install_dir, VERSION_FILE)
        
        if not os.path.exists(version_path):
            return "0.0.0"  # Default if version file doesn't exist
            
        with open(version_path, 'r') as f:
            data = json.load(f)
            return data.get('version', '0.0.0')
    except Exception as e:
        logger.error(f"Error reading current version: {e}")
        return "0.0.0"


def compare_versions(current, latest):
    """Compare version numbers to determine if an update is needed"""
    if not latest:
        return False
        
    try:    
        current_parts = [int(p) for p in current.split('.')]
        latest_parts = [int(p) for p in latest.split('.')]
        
        # Pad with zeros if versions have different lengths
        while len(current_parts) < len(latest_parts):
            current_parts.append(0)
        while len(latest_parts) < len(current_parts):
            latest_parts.append(0)
        
        # Compare each part of the version
        for i in range(len(current_parts)):
            if latest_parts[i] > current_parts[i]:
                return True
            if latest_parts[i] < current_parts[i]:
                return False
    except ValueError:
        logger.error("Version format error - expecting numbers separated by dots")
        return False
        
    return False  # Versions are equal


def download_update(download_url):
    """Download the update file"""
    logger.info(f"Downloading update from: {download_url}")
    temp_file = os.path.join(TEMP_DIRECTORY, "lt_aimbot_update.exe")
    
    try:
        with urllib.request.urlopen(download_url) as response, open(temp_file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        logger.info(f"Download completed: {temp_file}")
        return temp_file
    except Exception as e:
        logger.error(f"Error downloading update: {e}")
        return None


def install_update(update_file):
    """Install the update"""
    try:
        # Run the installer silently
        logger.info(f"Running installer: {update_file}")
        subprocess.run(
            [update_file, '/VERYSILENT', '/NORESTART'], 
            check=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True
    except Exception as e:
        logger.error(f"Error installing update: {e}")
        return False


def check_for_updates(silent=False):
    """Check for updates and install if available"""
    logger.info("Starting update check...")
    
    # Get current version
    current_version = get_current_version()
    logger.info(f"Current version: {current_version}")
    
    # Get latest version from GitHub
    try:
        req = urllib.request.Request(GITHUB_API_URL, headers={"User-Agent": USER_AGENT})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                latest_version = data.get("tag_name", "").replace("v", "")
                download_url = None
                release_notes = data.get("body", "No release notes available.")
                
                # Find the installer asset
                for asset in data.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        break
                
                if not latest_version:
                    logger.warning("No version tag found in GitHub release")
                    if not silent:
                        show_message("Update Error", "No version information found in the latest release.")
                    return False
                    
                if not download_url:
                    logger.warning("No installer found in the latest release")
                    if not silent:
                        show_message("Update Error", 
                                  f"A new version {latest_version} is available, but no installer was found.\n\n" +
                                  "Please download the update manually from the project website.")
                    return False
                
                # Compare versions
                if compare_versions(current_version, latest_version):
                    logger.info(f"New version available: {latest_version}")
                    
                    if not silent:
                        if show_message("Update Available", 
                                     f"A new version {latest_version} is available.\n\n" +
                                     f"Current version: {current_version}\n\n" +
                                     f"Release notes:\n{release_notes}\n\n" +
                                     "Would you like to update now?", True):
                            
                            # Download and install
                            update_file = download_update(download_url)
                            if update_file:
                                if install_update(update_file):
                                    show_message("Update Complete", 
                                              f"Update to version {latest_version} completed successfully!\n\n" +
                                              "Please restart the application.")
                                    return True
                                else:
                                    show_message("Update Failed", 
                                              "Failed to install the update.\n\n" +
                                              "Please try again later or download the update manually.")
                                    return False
                            else:
                                show_message("Update Failed", 
                                          "Failed to download the update.\n\n" +
                                          "Please check your internet connection and try again.")
                                return False
                    else:
                        # Silent update
                        update_file = download_update(download_url)
                        if update_file:
                            return install_update(update_file)
                        return False
                else:
                    logger.info("You have the latest version.")
                    if not silent:
                        show_message("Up to Date", f"You have the latest version ({current_version}).")
                    return True
                    
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # 404 error - repository or releases not found
                logger.warning("GitHub repository or releases not found (404 error)")
                if not silent:
                    show_message("No Updates Available", 
                              "No updates found. You're using the initial version.\n\n" +
                              "This is normal if no releases have been published to GitHub yet.")
            else:
                # Other HTTP errors
                logger.error(f"HTTP Error {e.code}: {e.reason}")
                if not silent:
                    show_message("Update Error", 
                              f"Error checking for updates: HTTP {e.code}\n\n" +
                              "Please check your internet connection and try again later.")
            return False
            
    except Exception as e:
        # Any other error
        logger.error(f"Error checking for updates: {e}")
        if not silent:
            show_message("Update Error", 
                      f"An unexpected error occurred while checking for updates.\n\n" +
                      "Please check your internet connection and try again later.")
        return False
        
    return False


def main():
    """Main entry point"""
    # Parse command-line arguments
    silent_mode = "--silent" in sys.argv
    
    if "--help" in sys.argv:
        print("Usage: updater.py [--silent] [--help]")
        print("\nOptions:")
        print("  --silent  Run updater in silent mode (no user prompts)")
        print("  --help    Show this help message")
        return
    
    # Check if running with admin privileges for installation
    if not is_admin() and "--no-elevate" not in sys.argv:
        logger.info("Requesting administrator privileges...")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv + ["--no-elevate"]), None, 1)
            return
        except Exception as e:
            logger.error(f"Failed to elevate privileges: {e}")
            if not silent_mode:
                show_message("Permission Error", "Administrator privileges are required to install updates.")
            return
    
    # Run the update check
    check_for_updates(silent_mode)


if __name__ == "__main__":
    main()
