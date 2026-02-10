@echo off
echo ========================================
echo Starting Hand Gesture Control System
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run INSTALL.bat first
    pause
    exit /b 1
)

REM Activate and run
call venv\Scripts\activate.bat
python PROTOTYPE.PY

pause
