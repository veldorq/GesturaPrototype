@echo off
title One-Click Distribution Builder
color 0A
cls
echo.
echo ========================================================================
echo                   ONE-CLICK DISTRIBUTION BUILDER
echo ========================================================================
echo.
echo  This creates a standalone .exe that customers can use with ZERO setup!
echo.
echo  What this does:
echo    ✓ Bundles Python + all libraries into ONE .exe file
echo    ✓ No installation needed for users
echo    ✓ Works on any Windows 10/11 PC with webcam
echo    ✓ Professional packaging with instructions
echo.
echo  Build time: 3-5 minutes (be patient!)
echo.
echo ========================================================================
pause
echo.

REM ===== STEP 1: Check Python Installation =====
echo [STEP 1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo.
    echo Please:
    echo   1. Install Python 3.10+ from python.org
    echo   2. Check "Add Python to PATH" during installation
    echo   3. Restart this script
    echo.
    pause
    exit /b 1
)
python --version
echo ✓ Python found!
echo.

REM ===== STEP 2: Setup Virtual Environment =====
echo [STEP 2/5] Setting up build environment...
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
    echo Upgrading pip...
    python -m pip install --upgrade pip --quiet
    echo Installing dependencies (this may take 2-3 minutes)...
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    call venv\Scripts\activate.bat
)
echo ✓ Environment ready!
echo.

REM ===== STEP 3: Install Build Tools =====
echo [STEP 3/5] Installing PyInstaller build tools...
pip install pyinstaller --quiet --upgrade
if errorlevel 1 (
    echo ❌ Failed to install PyInstaller
    pause
    exit /b 1
)
echo ✓ Build tools ready!
echo.

REM ===== STEP 4: Clean Previous Builds =====
echo [STEP 4/5] Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo ✓ Clean slate!
echo.

REM ===== STEP 5: Build Executable =====
echo [STEP 5/5] Building standalone application...
echo.
echo      ⏳ This takes 3-5 minutes - please wait...
echo      Building comprehensive package with all dependencies...
echo.

REM Build with console mode for better user feedback and debugging
pyinstaller --onefile ^
    --name "HandGestureControl" ^
    --console ^
    --add-data "requirements.txt;." ^
    --hidden-import="cv2" ^
    --hidden-import="mediapipe" ^
    --hidden-import="pyautogui" ^
    --hidden-import="numpy" ^
    --hidden-import="tensorflow" ^
    --hidden-import="sklearn" ^
    --hidden-import="filterpy" ^
    --hidden-import="scipy" ^
    --hidden-import="PIL" ^
    --collect-all mediapipe ^
    --collect-all cv2 ^
    --noconfirm ^
    --log-level ERROR ^
    PROTOTYPE.PY

if errorlevel 1 (
    color 0C
    echo.
    echo ❌ Build failed! Check errors above.
    pause
    exit /b 1
)

if exist "dist\HandGestureControl.exe" (
    color 0A
    echo.
    echo ========================================================================
    echo                    ✓ BUILD SUCCESSFUL!
    echo ========================================================================
    echo.
    
    REM Get file size
    for %%A in ("dist\HandGestureControl.exe") do set SIZE=%%~zA
    set /a SIZE_MB=%SIZE% / 1048576
    echo Executable created: %SIZE_MB% MB
    echo.
    
    REM Create distribution package
    echo Creating customer package...
    set PKG=HandGestureControl_ReadyToShare
    if exist "%PKG%" rmdir /s /q "%PKG%"
    mkdir "%PKG%"
    
    REM Copy executable
    copy "dist\HandGestureControl.exe" "%PKG%\" >nul
    
    REM Create comprehensive user guide
    (
        echo ========================================================================
        echo                      HAND GESTURE CONTROL
        echo                  Touchless Browser Navigation System
        echo ========================================================================
        echo.
        echo QUICK START:
        echo   1. Double-click HandGestureControl.exe
        echo   2. Click "Allow" when asked for camera permission
        echo   3. Position your hand in front of the camera
        echo   4. Start making gestures - watch the magic happen!
        echo.
        echo ========================================================================
        echo GESTURE CONTROLS:
        echo ========================================================================
        echo.
        echo SCROLLING:
        echo   ✋ Open Palm          ^→  Scroll Down
        echo   ✊ Closed Fist        ^→  Scroll Up
        echo.
        echo POINTER CONTROL:
        echo   ☝️ Index Finger      ^→  Move Mouse Cursor
        echo   ✌️ Peace Sign        ^→  Left Click
        echo   🖖 Three Fingers     ^→  Left Click
        echo.
        echo NAVIGATION:
        echo   👈 Swipe Left        ^→  Browser Back
        echo   👉 Swipe Right       ^→  Browser Forward
        echo.
        echo OTHER ACTIONS:
        echo   👍 Thumb Up          ^→  Zoom In
        echo   🖐️ Four Fingers     ^→  Refresh Page
        echo   🤙 Pinky Only        ^→  Mute/Unmute
        echo.
        echo PROGRAM CONTROLS:
        echo   Press 'Q'            ^→  Quit Application
        echo   Press 'S'            ^→  Show Statistics
        echo   Press 'H'            ^→  Toggle Advanced UI
        echo.
        echo ========================================================================
        echo SYSTEM REQUIREMENTS:
        echo ========================================================================
        echo   ✓ Windows 10 or Windows 11
        echo   ✓ Webcam ^(built-in or USB^)
        echo   ✓ 4GB RAM minimum
        echo   ✓ Internet browser installed
        echo.
        echo ========================================================================
        echo TIPS FOR BEST EXPERIENCE:
        echo ========================================================================
        echo   • Good lighting helps detection ^(avoid dark rooms^)
        echo   • Keep hand 1-2 feet from camera
        echo   • Make clear, deliberate gestures
        echo   • Practice for 1-2 minutes to get comfortable
        echo   • Use one hand at a time
        echo   • Hold gestures briefly for recognition
        echo.
        echo ========================================================================
        echo TROUBLESHOOTING:
        echo ========================================================================
        echo.
        echo Problem: "Camera not found"
        echo   Solution: 
        echo     - Check camera is connected
        echo     - Go to Windows Settings ^> Privacy ^> Camera
        echo     - Enable camera access for desktop apps
        echo     - Close other apps using camera ^(Zoom, Skype, etc.^)
        echo.
        echo Problem: "Gestures not detected"
        echo   Solution:
        echo     - Ensure good lighting
        echo     - Move hand closer to camera
        echo     - Make more distinct gestures
        echo     - Try holding gesture for 1 second
        echo.
        echo Problem: "Application won't start"
        echo   Solution:
        echo     - Right-click .exe ^> Run as Administrator
        echo     - Disable antivirus temporarily
        echo     - Re-extract from ZIP file
        echo.
        echo Problem: "Too sensitive / Not responsive"
        echo   Solution:
        echo     - Adjust distance from camera
        echo     - Check lighting conditions
        echo     - Make clearer hand poses
        echo.
        echo ========================================================================
        echo PRIVACY NOTE:
        echo ========================================================================
        echo   This application runs completely on YOUR computer.
        echo   • No data is sent to the internet
        echo   • Camera feed stays on your device
        echo   • No personal information collected
        echo   • No tracking or analytics
        echo.
        echo ========================================================================
        echo.
        echo   Ready to experience hands-free control?
        echo   Double-click HandGestureControl.exe to begin!
        echo.
        echo ========================================================================
    ) > "%PKG%\START_HERE.txt"
    
    REM Create quick reference card
    (
        echo ======================================
        echo       QUICK REFERENCE CARD
        echo ======================================
        echo.
        echo ✋ Open Palm      = Scroll Down
        echo ✊ Closed Fist    = Scroll Up
        echo ☝️ Index Finger  = Move Cursor
        echo ✌️ Peace Sign    = Click
        echo 👈 Swipe Left    = Browser Back
        echo 👉 Swipe Right   = Browser Forward
        echo.
        echo Press Q to Quit
        echo ======================================
    ) > "%PKG%\QUICK_REFERENCE.txt"
    
    echo ✓ Package created: %PKG%
    echo ✓ User guide created: START_HERE.txt
    echo ✓ Quick reference created: QUICK_REFERENCE.txt
    echo.
    echo ========================================================================
    echo                     📦 READY TO DISTRIBUTE!
    echo ========================================================================
    echo.
    echo YOUR PACKAGE FOLDER: %PKG%
    echo    Contains: HandGestureControl.exe ^(%SIZE_MB% MB^)
    echo              START_HERE.txt ^(full instructions^)
    echo              QUICK_REFERENCE.txt ^(gesture list^)
    echo.
    echo ========================================================================
    echo NEXT STEPS FOR DISTRIBUTION:
    echo ========================================================================
    echo.
    echo 1. TEST IT FIRST:
    echo    ^> Open the folder that just opened
    echo    ^> Double-click HandGestureControl.exe
    echo    ^> Make sure everything works perfectly
    echo.
    echo 2. CREATE ZIP FILE:
    echo    ^> Right-click "%PKG%" folder
    echo    ^> Send to ^> Compressed ^(zipped^) folder
    echo    ^> You'll get: HandGestureControl_ReadyToShare.zip
    echo.
    echo 3. SHARE WITH CUSTOMERS:
    echo    Option A: Upload to Google Drive / Dropbox
    echo    Option B: Send via WeTransfer ^(wetransfer.com^)
    echo    Option C: Email ^(if under 25MB^)
    echo    Option D: GitHub Releases
    echo.
    echo ========================================================================
    echo WHAT CUSTOMERS DO:
    echo ========================================================================
    echo    1. Download the ZIP file
    echo    2. Right-click ^> Extract All
    echo    3. Read START_HERE.txt
    echo    4. Double-click HandGestureControl.exe
    echo    5. Enjoy! ✨
    echo.
    echo    NO Python installation needed!
    echo    NO setup required!
    echo    NO technical knowledge needed!
    echo    Just extract and run!
    echo.
    echo ========================================================================
    echo.
    
    REM Open the package folder for testing
    echo Opening package folder for you to test...
    start "" "%PKG%"
    
) else (
    color 0C
    echo.
    echo ========================================================================
    echo                         ❌ BUILD FAILED
    echo ========================================================================
    echo.
    echo The .exe file was not created. Possible reasons:
    echo.
    echo   • Python not properly installed
    echo   • Missing dependencies ^(run: pip install -r requirements.txt^)
    echo   • Antivirus blocking PyInstaller
    echo   • Insufficient disk space
    echo   • PROTOTYPE.PY has syntax errors
    echo.
    echo Please fix the errors above and try again.
    echo.
)

echo.
echo Press any key to close...
pause >nul
