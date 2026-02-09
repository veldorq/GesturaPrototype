"""
Setup Helper - Ensure all folders exist and provide troubleshooting
"""

import os
import sys
from pathlib import Path

def check_and_create_folders():
    """Create required folders"""
    print("Checking project setup...")
    print("=" * 70)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"\nCurrent directory: {current_dir}")
    
    # Check if we're in the right place
    if not Path("PROTOTYPE.PY").exists():
        print("\n[ERROR] PROTOTYPE.PY not found!")
        print("\nYou need to run this from the SOuvikmeet folder:")
        print(f"  cd \"{Path(__file__).parent}\"")
        return False
    
    print("\n[OK] In correct directory")
    
    # Create necessary folders
    folders = ["dataset", "models"]
    for folder in folders:
        folder_path = Path(folder)
        folder_path.mkdir(exist_ok=True)
        print(f"[OK] {folder}/ folder ready")
    
    print("\n" + "=" * 70)
    print("Setup complete! All folders created.\n")
    return True

def show_quick_commands():
    """Show available commands"""
    print("Available commands:")
    print("-" * 70)
    print("\nFull automated training (recommended):")
    print("  python train_now.py")
    print("\nManual training steps:")
    print("  1. python quick_data_collector.py    # Fast data collection")
    print("  2. python train_gesture_model.py     # Train model")
    print("  3. Edit PROTOTYPE.PY: ENABLE_CNN_CLASSIFIER = True")
    print("\nTesting:")
    print("  python test_gesture_detection.py     # Test camera/hand detection")
    print("  python PROTOTYPE.PY                  # Run main system")
    print("\n" + "=" * 70)

def main():
    """Main setup"""
    print("\n" + "=" * 70)
    print("  CNN TRAINING - SETUP CHECKER")
    print("=" * 70 + "\n")
    
    if not check_and_create_folders():
        print("\n[ERROR] Setup failed!")
        print("\nMake sure you run this from the SOuvikmeet project folder.")
        print("\nNavigate to the folder first:")
        print("  cd \"c:\\Users\\Souvik\\Desktop\\Souvik project\\SOuvikmeet\"")
        return
    
    show_quick_commands()
    
    print("\n[SUCCESS] Setup complete!")
    print("\nReady to start training? Run:")
    print("  python train_now.py")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
