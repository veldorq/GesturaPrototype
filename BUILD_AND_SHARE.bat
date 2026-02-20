@echo off
echo ========================================
echo Quick Build - Gestura Distribution
echo ========================================
echo.
echo This will create a ready-to-distribute package
echo that you can share directly with users.
echo.
pause

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment if not exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
    pip install pyinstaller
) else (
    call venv\Scripts\activate.bat
)

echo.
echo ========================================
echo Building Gestura.exe...
echo ========================================
echo.

REM Build executable
pyinstaller --onefile ^
    --name "Gestura" ^
    --add-data "models;models" ^
    --add-data "config;config" ^
    --hidden-import="mediapipe" ^
    --hidden-import="cv2" ^
    --hidden-import="pyautogui" ^
    --hidden-import="numpy" ^
    --hidden-import="PIL" ^
    --hidden-import="dataclasses" ^
    --collect-all mediapipe ^
    --console ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Creating Distribution Package...
echo ========================================
echo.

REM Create distribution folder
if exist "Gestura-Release" rmdir /s /q "Gestura-Release"
mkdir "Gestura-Release"

REM Copy files
copy "dist\Gestura.exe" "Gestura-Release\"
copy "END_USER_INSTALL_GUIDE.md" "Gestura-Release\README.txt"
copy "LICENSE" "Gestura-Release\" 2>nul

REM Create simple user guide
(
echo Welcome to Gestura!
echo.
echo HOW TO RUN:
echo 1. Double-click Gestura.exe
echo 2. Allow camera permission when prompted
echo 3. Start using hand gestures!
echo.
echo BASIC GESTURES:
echo - Open Palm = Scroll Down
echo - Closed Fist = Scroll Up
echo - Index Finger = Move Mouse
echo - Peace Sign = Click
echo.
echo Press Q to quit
echo.
echo For detailed guide, see README.txt
) > "Gestura-Release\QUICKSTART.txt"

echo.
echo ========================================
echo SUCCESS!
echo ========================================
echo.
echo Distribution package created in: Gestura-Release\
echo.
echo WHAT'S INSIDE:
echo   - Gestura.exe (main application)
echo   - README.txt (detailed instructions)
echo   - QUICKSTART.txt (quick reference)
echo   - LICENSE (if available)
echo.
echo FILE SIZE: 
dir "Gestura-Release\Gestura.exe" | find "Gestura.exe"
echo.
echo ========================================
echo NEXT STEPS - Choose ONE option:
echo ========================================
echo.
echo OPTION 1: Share via Google Drive / Dropbox
echo   1. ZIP the Gestura-Release folder
echo   2. Upload to Google Drive or Dropbox
echo   3. Get sharing link (set to "Anyone with link can download")
echo   4. Update website download button with that link
echo.
echo OPTION 2: Create GitHub Release (Manual)
echo   1. Go to: https://github.com/veldorq/GesturaPrototype/releases/new
echo   2. Tag: v1.0.0
echo   3. Title: Gestura v1.0.0
echo   4. Drag and drop Gestura-Release folder (as ZIP)
echo   5. Click "Publish release"
echo   6. Downloads will work automatically!
echo.
echo OPTION 3: Host on your website
echo   1. ZIP the Gestura-Release folder
echo   2. Upload to your web hosting
echo   3. Update download link to: your-site.com/downloads/Gestura.zip
echo.
echo ========================================
echo.
pause
