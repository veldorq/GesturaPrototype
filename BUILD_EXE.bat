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
    --name "HandGestureControl" ^
    --add-data "requirements.txt;." ^
    --hidden-import="mediapipe" ^
    --hidden-import="cv2" ^
    --hidden-import="pyautogui" ^
    --hidden-import="numpy" ^
    PROTOTYPE.PY

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable location: dist\HandGestureControl.exe
echo.
echo To distribute:
echo   1. Copy dist\HandGestureControl.exe
echo   2. Include USER_GUIDE.md
echo   3. Users just double-click the .exe file!
echo.
pause
