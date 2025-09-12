import requests
import io
import os
import shutil
import sys
import zipfile

# git configuration

USERNAME = "shreksojoe"
REPO = "lt_aimbot"
LOCAL_COMMIT_FILE = ".current_commit"
EXTRACT_DIR = "repo_update_temp"

GITHUB_API_COMMIT = f"https://api.github.com/repos/shreksojoe/lt_aimbot/commits/master"
GITHUB_ZIP_URL = f"https://github.com/shreksojoe/lt_aimbot/archive/refs/heads/master.zip"

# ------------------- Functions -------------------
def get_latest_commit():
    """Get the SHA of the latest commit on main."""
    r = requests.get(GITHUB_API_COMMIT)
    r.raise_for_status()
    return r.json()["sha"]

def get_local_commit():
    if os.path.exists(LOCAL_COMMIT_FILE):
        with open(LOCAL_COMMIT_FILE, "r") as f:
            return f.read().strip()
    return None

def save_local_commit(commit_sha):
    with open(LOCAL_COMMIT_FILE, "w") as f:
        f.write(commit_sha)

def download_and_extract():
    """Download the ZIP and replace current files."""
    print("Downloading latest code...")
    r = requests.get(GITHUB_ZIP_URL)
    r.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall(EXTRACT_DIR)

    # GitHub ZIP adds repo-branch to folder name
    extracted_folder = next(
        name for name in os.listdir(EXTRACT_DIR)
        if os.path.isdir(os.path.join(EXTRACT_DIR, name))
    )
    extracted_path = os.path.join(EXTRACT_DIR, extracted_folder)

    # Copy over files
    for item in os.listdir(extracted_path):
        s = os.path.join(extracted_path, item)
        d = os.path.join(".", item)
        if os.path.isdir(s):
            if os.path.exists(d):
                try:
                    shutil.rmtree(d)
                except PermissionError:
                    print("can't update")
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    shutil.rmtree(EXTRACT_DIR)

def auto_update():
    """Check for updates and apply them automatically."""
    print("Checking for updates...")
    latest_commit = get_latest_commit()
    local_commit = get_local_commit()

    if local_commit != latest_commit:
        print("New version detected! Updating...")
        download_and_extract()
        save_local_commit(latest_commit)
        print("Update complete. Restarting...")
        # Restart the script
        python = sys.executable
        os.execv(python, [python] + sys.argv)
    else:
        print("Already up to date.")

