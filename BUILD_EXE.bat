@echo off
echo ========================================
echo Building Executable Package
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run INSTALL.bat first
    pause
    exit /b 1
)

REM Activate environment
call venv\Scripts\activate.bat

REM Install PyInstaller if needed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building standalone executable...
echo This may take 2-5 minutes...
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
    main.py

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable location: dist\Gestura.exe
echo.
echo To create distribution package:
echo   1. Copy dist\Gestura.exe to release/
echo   2. Copy END_USER_INSTALL_GUIDE.md to release/README.txt
echo   3. Copy USER_GUIDE.md to release/
echo   4. ZIP the release/ folder
echo   5. Upload to GitHub Releases
echo.
echo Users will download the ZIP, extract, and run Gestura.exe
echo.
pause
