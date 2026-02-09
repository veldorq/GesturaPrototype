@echo off
REM Quick Setup Script for Windows
REM This ensures you're in the right directory and creates necessary folders

echo =====================================
echo   CNN TRAINING - QUICK SETUP
echo =====================================
echo.

REM Navigate to the correct directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Check if PROTOTYPE.PY exists
if not exist "PROTOTYPE.PY" (
    echo [ERROR] PROTOTYPE.PY not found!
    echo This script must be in the SOuvikmeet folder.
    echo.
    pause
    exit /b 1
)

echo [OK] In correct directory
echo.

REM Create necessary folders
if not exist "dataset" mkdir dataset
echo [OK] dataset folder created

if not exist "models" mkdir models
echo [OK] models folder created

echo.
echo =====================================
echo   SETUP COMPLETE!
echo =====================================
echo.
echo Now you can run:
echo   python train_now.py
echo.
echo Or manually:
echo   python quick_data_collector.py
echo   python train_gesture_model.py
echo.
pause
