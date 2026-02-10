@echo off
echo ========================================
echo Hand Gesture Control - Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

echo [1/3] Python detected
echo.

REM Create virtual environment
echo [2/3] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate and install dependencies
echo [3/3] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Double-click RUN.bat
echo   or
echo   2. Run: venv\Scripts\activate.bat
echo          python PROTOTYPE.PY
echo.
pause
