"""
Fix Environment - Install Missing Packages
===========================================
This script ensures all packages are installed in the correct Python environment.
"""

import subprocess
import sys

def install_packages():
    """Install all required packages"""
    print("=" * 70)
    print("  INSTALLING REQUIRED PACKAGES")
    print("=" * 70)
    print(f"\nUsing Python: {sys.executable}")
    print(f"Python version: {sys.version.split()[0]}\n")
    
    packages = [
        "opencv-python>=4.8.0",
        "mediapipe>=0.10.0",
        "tensorflow>=2.13.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.0",
        "numpy>=1.24.0",
        "protobuf>=5.28.0"
    ]
    
    print("Installing packages (this may take a few minutes)...\n")
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package, "--quiet"
            ])
            print(f"  [OK] {package}")
        except subprocess.CalledProcessError as e:
            print(f"  [ERROR] Failed to install {package}: {e}")
            return False
    
    print("\n" + "=" * 70)
    print("  VERIFYING INSTALLATIONS")
    print("=" * 70 + "\n")
    
    # Verify imports
    imports_ok = True
    
    try:
        import cv2
        print(f"[OK] OpenCV {cv2.__version__}")
    except Exception as e:
        print(f"[FAIL] OpenCV: {e}")
        imports_ok = False
    
    try:
        import mediapipe
        print(f"[OK] MediaPipe {mediapipe.__version__}")
    except Exception as e:
        print(f"[FAIL] MediaPipe: {e}")
        imports_ok = False
    
    try:
        import tensorflow
        print(f"[OK] TensorFlow {tensorflow.__version__}")
    except Exception as e:
        print(f"[FAIL] TensorFlow: {e}")
        imports_ok = False
    
    try:
        import sklearn
        print(f"[OK] scikit-learn {sklearn.__version__}")
    except Exception as e:
        print(f"[FAIL] scikit-learn: {e}")
        imports_ok = False
    
    try:
        import numpy
        print(f"[OK] NumPy {numpy.__version__}")
    except Exception as e:
        print(f"[FAIL] NumPy: {e}")
        imports_ok = False
    
    print("\n" + "=" * 70)
    
    if imports_ok:
        print("  SUCCESS - ALL PACKAGES INSTALLED AND WORKING!")
        print("=" * 70)
        print("\nYou can now run:")
        print("  python train_now.py")
        print("\nOr proceed directly with:")
        print("  python quick_data_collector.py")
        return True
    else:
        print("  SOME IMPORTS FAILED")
        print("=" * 70)
        print("\nTry running this script again, or install manually:")
        print(f'  "{sys.executable}" -m pip install opencv-python mediapipe tensorflow scikit-learn')
        return False

if __name__ == "__main__":
    print("\n")
    try:
        success = install_packages()
        print("\n")
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
