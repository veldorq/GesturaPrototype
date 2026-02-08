"""
Quick setup script for AccessAble.
Verifies dependencies and provides helpful setup guidance.
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version meets requirements."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'pyautogui': 'pyautogui',
        'numpy': 'numpy'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} not found")
            missing.append(package)
    
    return missing


def install_dependencies(missing):
    """Install missing dependencies."""
    if not missing:
        return True
    
    print("\nInstalling missing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', *missing
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def verify_structure():
    """Verify project structure."""
    required_dirs = [
        'camera',
        'hand_tracking',
        'gestures',
        'actions',
        'ui',
        'config'
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print(f"✓ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ not found")
            all_exist = False
    
    return all_exist


def main():
    print("=" * 60)
    print("AccessAble - Setup Verification")
    print("=" * 60)
    print()
    
    # Check Python version
    print("Checking Python version...")
    if not check_python_version():
        print("\nPlease upgrade Python to 3.10 or higher")
        print("Download from: https://www.python.org/downloads/")
        return
    
    print()
    
    # Check project structure
    print("Verifying project structure...")
    if not verify_structure():
        print("\nError: Project structure incomplete")
        print("Please ensure all module directories exist")
        return
    
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print()
        response = input("Install missing packages? (y/n): ").lower()
        if response == 'y':
            if not install_dependencies(missing):
                return
        else:
            print("\nTo install manually, run:")
            print(f"  pip install {' '.join(missing)}")
            return
    
    print()
    print("=" * 60)
    print("✓ Setup complete!")
    print("=" * 60)
    print()
    print("To run AccessAble:")
    print("  python main.py")
    print()
    print("Controls:")
    print("  ESC   - Pause/Resume")
    print("  Q     - Quit")
    print("  Space - Toggle pause")
    print()


if __name__ == "__main__":
    main()
