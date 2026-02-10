@echo off
title One-Click Distribution Builder
color 0B
cls
echo.
echo ========================================
echo   ONE-CLICK DISTRIBUTION BUILDER
echo ========================================
echo.
echo This will create a single .exe that users
echo can just double-click and enjoy!
echo.
echo Building now... This takes 3-5 minutes.
echo.
pause

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Setting up environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Install PyInstaller
echo Installing build tools...
pip install pyinstaller pillow 2>nul

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

echo.
echo ========================================
echo   Building Standalone Application
echo ========================================
echo.

REM Build with maximum compatibility
pyinstaller --onefile ^
    --name "HandGestureControl" ^
    --windowed ^
    --add-data "requirements.txt;." ^
    --hidden-import="cv2" ^
    --hidden-import="mediapipe" ^
    --hidden-import="pyautogui" ^
    --hidden-import="numpy" ^
    --hidden-import="PIL" ^
    --collect-all mediapipe ^
    --collect-all cv2 ^
    --noconfirm ^
    PROTOTYPE.PY

if exist "dist\HandGestureControl.exe" (
    echo.
    echo ========================================
    echo   SUCCESS! Creating User Package
    echo ========================================
    echo.
    
    REM Create simple user folder
    set PKG=HandGestureControl_ReadyToShare
    if exist "%PKG%" rmdir /s /q "%PKG%"
    mkdir "%PKG%"
    
    REM Copy executable
    copy "dist\HandGestureControl.exe" "%PKG%\"
    
    REM Create ultra-simple instructions
    (
        echo ================================
        echo   HAND GESTURE CONTROL
        echo ================================
        echo.
        echo HOW TO USE:
        echo   1. Double-click HandGestureControl.exe
        echo   2. Allow camera access
        echo   3. Start making gestures!
        echo.
        echo BASIC GESTURES:
        echo   - Open palm = Scroll down
        echo   - Closed fist = Scroll up
        echo   - Index finger = Move cursor
        echo   - Three fingers = Click
        echo   - Press Q = Quit
        echo.
        echo REQUIREMENTS:
        echo   - Windows 10 or 11
        echo   - Webcam
        echo.
        echo First time? Practice gestures for
        echo 1-2 minutes until it feels natural.
        echo.
        echo Need help? The app shows gesture
        echo hints in the camera window.
        echo.
        echo Enjoy hands-free control!
        echo ================================
    ) > "%PKG%\README.txt"
    
    echo ✓ Package created: %PKG%
    echo.
    echo ========================================
    echo   READY TO SHARE!
    echo ========================================
    echo.
    echo YOUR PACKAGE: %PKG%
    echo FILE INSIDE: HandGestureControl.exe
    echo.
    echo NEXT STEPS:
    echo   1. Test it - open folder and run the .exe
    echo   2. Compress to ZIP - right-click folder
    echo   3. Share ZIP file with users
    echo.
    echo USERS JUST:
    echo   1. Extract ZIP
    echo   2. Double-click .exe
    echo   3. Enjoy!
    echo.
    echo No Python, no installation, just works!
    echo.
    
    REM Open the package folder
    start "" "%PKG%"
    
) else (
    echo.
    echo ========================================
    echo   BUILD FAILED
    echo ========================================
    echo.
    echo Something went wrong. Check:
    echo   - Python is installed
    echo   - All dependencies installed
    echo   - No errors above
    echo.
)

pause
