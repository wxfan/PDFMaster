import os
import subprocess
import platform

def package():
    # Determine the operating system
    is_windows = platform.system() == "Windows"

    # Clean up old build and dist directories
    if os.path.exists("dist"):
        if is_windows:
            os.system("rmdir /s /q dist")
        else:
            os.system("rm -rf dist")

    if os.path.exists("build"):
        if is_windows:
            os.system("rmdir /s /q build")
        else:
            os.system("rm -rf build")

    # Execute the packaging command
    subprocess.run(["pyinstaller", "PDFMaster.spec"])

if __name__ == "__main__":
    package()