import platform
import subprocess
import re
import shutil
import os
import sys

if platform.system() == "Windows":
    import winreg

def get_chrome_version():
    """
    Returns the installed Google Chrome version as a string, e.g. "115.0.5790.110".
    Raises RuntimeError if Chrome is not found or version cannot be parsed.
    """
    os_name = platform.system()
    version_output = ""

    if os_name == "Windows":
        # 1) Try registry lookup
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Google\Chrome\BLBeacon"
            )
            version_output, _ = winreg.QueryValueEx(key, "version")
        except Exception:
            # 2) Fallback: run executable directly
            for path in (
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ):
                if os.path.exists(path):
                    version_output = subprocess.check_output(
                        [path, "--version"], text=True
                    ).strip()
                    break

    elif os_name == "Darwin":
        chrome_path = (
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
        if os.path.exists(chrome_path):
            version_output = subprocess.check_output(
                [chrome_path, "--version"], text=True
            ).strip()

    else:  # Linux / Chromium
        for cmd in (
            "google-chrome",
            "google-chrome-stable",
            "chrome",
            "chromium-browser",
            "chromium",
        ):
            path = shutil.which(cmd)
            if path:
                try:
                    version_output = subprocess.check_output(
                        [path, "--version"], text=True
                    ).strip()
                    break
                except subprocess.SubprocessError:
                    continue

    if not version_output:
        raise RuntimeError("Could not locate or invoke Chrome executable.")

    # Extract semantic version
    match = re.search(r"(\d+\.\d+\.\d+\.\d+)", version_output)
    if not match:
        raise RuntimeError(f"Unexpected version format: {version_output}")

    return match.group(1)

# Direct invocation without using a main-guard
print("Google Chrome Version:", get_chrome_version())
