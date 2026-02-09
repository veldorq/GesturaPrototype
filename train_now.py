"""
QUICK CNN TRAINING WORKFLOW
============================
This script guides you through training a CNN model in 3 easy steps.

Total time: ~15-20 minutes
Results: Much better gesture recognition with fewer errors
"""

import os
import sys
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def check_environment():
    """Check if all required packages are installed"""
    print_header("STEP 0: Checking Environment")
    
    import sys
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version.split()[0]}\n")
    
    missing = []
    errors = []
    
    try:
        import cv2
        print(f"[OK] OpenCV {cv2.__version__}")
    except ImportError as e:
        missing.append("opencv-python")
        errors.append(str(e))
    except Exception as e:
        print(f"[WARN] OpenCV import error: {e}")
    
    try:
        import mediapipe
        print(f"[OK] MediaPipe {mediapipe.__version__}")
    except ImportError as e:
        missing.append("mediapipe")
        errors.append(str(e))
    except Exception as e:
        print(f"[WARN] MediaPipe import error: {e}")
    
    try:
        import tensorflow
        print(f"[OK] TensorFlow {tensorflow.__version__}")
    except ImportError as e:
        missing.append("tensorflow")
        errors.append(str(e))
    except Exception as e:
        print(f"[WARN] TensorFlow import error: {e}")
    
    try:
        import sklearn
        print(f"[OK] scikit-learn {sklearn.__version__}")
    except ImportError as e:
        missing.append("scikit-learn")
        errors.append(str(e))
    except Exception as e:
        print(f"[WARN] scikit-learn import error: {e}")
    
    if missing:
        print(f"\n[ERROR] Cannot import: {', '.join(missing)}")
        print("\nThis usually means:")
        print("  1. Packages not installed in the current Python environment")
        print("  2. Running from wrong Python interpreter")
        print(f"\nCurrent Python: {sys.executable}")
        print("\nTo fix, run this command in PowerShell:")
        print(f'  "{sys.executable}" -m pip install {" ".join(missing)}')
        print("\nOr if using virtual environment:")
        print("  .venv\\Scripts\\Activate.ps1")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print("\n[SUCCESS] All required packages installed!")
    return True

def step1_collect_data():
    """Guide user through data collection"""
    print_header("STEP 1: Collect Gesture Data (10-15 minutes)")
    
    # Create dataset folder if it doesn't exist
    dataset_path = Path("dataset")
    dataset_path.mkdir(exist_ok=True)
    print(f"✓ Dataset folder ready: {dataset_path.absolute()}\n")
    
    print("You'll collect images for 7 gestures:")
    print("  1. scroll_up (closed fist)")
    print("  2. scroll_down (open palm)")
    print("  3. swipe_left")
    print("  4. swipe_right")
    print("  5. pinch_zoom")
    print("  6. thumb_down_close")
    print("  7. mute_toggle (pinky finger)")
    print("\nTarget: ~100-200 images per gesture (can do more for better accuracy)")
    print("\nControls:")
    print("  's' - Start/Stop capturing")
    print("  'n' - Next gesture")
    print("  'q' - Quit (after collecting all)")
    
    print("\n" + "-"*70)
    response = input("Ready to start data collection? (y/n): ").strip().lower()
    
    if response == 'y':
        print("\nStarting data collector...")
        result = os.system("python collect_gesture_dataset.py")
        if result != 0:
            print("\n⚠ Data collector exited with errors")
            return False
        
        # Check if dataset was created
        dataset_path = Path("dataset")
        if dataset_path.exists():
            gesture_folders = list(dataset_path.glob("*"))
            if len(gesture_folders) >= 7:
                print("\n✓ Dataset collection complete!")
                return True
            else:
                print(f"\n⚠ Only {len(gesture_folders)} gesture folders found.")
                print("You may want to collect more data.")
                response = input("Continue anyway? (y/n): ").strip().lower()
                return response == 'y'
        else:
            print("\n❌ Dataset folder not found. Data collection may have failed.")
            return False
    else:
        print("\nData collection skipped. You can run it manually:")
        print("  python collect_gesture_dataset.py")
        return False

def step2_train_model():
    """Train the CNN model"""
    print_header("STEP 2: Train CNN Model (5-10 minutes)")
    
    # Create models folder if it doesn't exist
    models_path = Path("models")
    models_path.mkdir(exist_ok=True)
    print(f"✓ Models folder ready: {models_path.absolute()}\n")
    
    dataset_path = Path("dataset")
    if not dataset_path.exists():
        print("❌ Dataset folder not found!")
        print("Please run data collection first (Step 1)")
        return False
    
    # Count images
    gesture_counts = {}
    for gesture_folder in dataset_path.glob("*"):
        if gesture_folder.is_dir():
            count = len(list(gesture_folder.glob("*.png")))
            gesture_counts[gesture_folder.name] = count
    
    if gesture_counts:
        print("Dataset summary:")
        total = 0
        for gesture, count in sorted(gesture_counts.items()):
            print(f"  {gesture}: {count} images")
            total += count
        print(f"\nTotal images: {total}")
        
        if total < 500:
            print("\n⚠ Warning: Less than 500 total images")
            print("  Recommended: 700-1400 images for good accuracy")
            print("  Minimum: 350-500 images will work but with lower accuracy")
            response = input("\nContinue training anyway? (y/n): ").strip().lower()
            if response != 'y':
                return False
    else:
        print("❌ No gesture folders with images found!")
        return False
    
    print("\n" + "-"*70)
    print("Training will take 5-10 minutes depending on your CPU/GPU")
    print("You'll see progress bars and accuracy metrics")
    response = input("\nStart training? (y/n): ").strip().lower()
    
    if response == 'y':
        print("\nStarting model training...")
        result = os.system("python train_gesture_model.py")
        
        if result == 0:
            # Check if model was created
            model_path = Path("models/gesture_cnn_model.h5")
            if model_path.exists():
                print("\n✓ Model training complete!")
                return True
            else:
                print("\n❌ Model file not found after training")
                return False
        else:
            print("\n❌ Training failed with errors")
            return False
    else:
        print("\nTraining skipped. You can run it manually:")
        print("  python train_gesture_model.py")
        return False

def step3_enable_cnn():
    """Enable CNN in PROTOTYPE.PY"""
    print_header("STEP 3: Enable CNN Recognition")
    
    model_path = Path("models/gesture_cnn_model.h5")
    if not model_path.exists():
        print("❌ Trained model not found!")
        print("Please complete training first (Step 2)")
        return False
    
    print("Model found! Now enabling CNN recognition in PROTOTYPE.PY...")
    
    # Read PROTOTYPE.PY
    prototype_path = Path("PROTOTYPE.PY")
    if not prototype_path.exists():
        print("❌ PROTOTYPE.PY not found!")
        return False
    
    content = prototype_path.read_text()
    
    # Check if CNN is already enabled
    if "ENABLE_CNN_CLASSIFIER = True" in content:
        print("✓ CNN is already enabled in PROTOTYPE.PY")
        return True
    
    # Enable CNN
    content = content.replace(
        "ENABLE_CNN_CLASSIFIER = False",
        "ENABLE_CNN_CLASSIFIER = True"
    )
    
    prototype_path.write_text(content)
    print("✓ CNN enabled in PROTOTYPE.PY")
    
    return True

def main():
    """Main training workflow"""
    print_header("CNN TRAINING QUICK START")
    print("This will guide you through:")
    print("  1. Collecting gesture data (~10-15 min)")
    print("  2. Training CNN model (~5-10 min)")
    print("  3. Enabling CNN recognition")
    print("\nTotal time: ~15-25 minutes")
    print("Result: Much better gesture accuracy!")
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please install missing packages.")
        return
    
    # Step 1: Collect data
    if not step1_collect_data():
        print("\n❌ Data collection incomplete. Exiting...")
        return
    
    # Step 2: Train model
    if not step2_train_model():
        print("\n❌ Model training incomplete. Exiting...")
        return
    
    # Step 3: Enable CNN
    if not step3_enable_cnn():
        print("\n❌ Failed to enable CNN. You can enable it manually.")
        print("In PROTOTYPE.PY, change:")
        print("  ENABLE_CNN_CLASSIFIER = False")
        print("  to")
        print("  ENABLE_CNN_CLASSIFIER = True")
        return
    
    # Success!
    print_header("🎉 TRAINING COMPLETE!")
    print("✓ Gesture dataset collected")
    print("✓ CNN model trained and saved")
    print("✓ CNN recognition enabled")
    print("\nYour system is now ready with improved gesture recognition!")
    print("\nRun the system:")
    print("  python PROTOTYPE.PY")
    print("\nThe CNN model will provide:")
    print("  • Higher accuracy gesture detection")
    print("  • Better handling of lighting conditions")
    print("  • More reliable recognition")
    print("  • No more CNN error messages")
    print("\nEnjoy your enhanced gesture control system! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Training interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
