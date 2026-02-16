@echo off
REM ============================================
REM Gestura Speed Optimization Deployment
REM ============================================

echo.
echo ========================================
echo   Gestura Speed Optimization Deploy
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/4] Installing Flask-Compress...
pip install Flask-Compress==1.14

echo.
echo [3/4] Verifying installations...
python -c "from flask_compress import Compress; print('✓ Flask-Compress installed successfully')"

echo.
echo [4/4] Testing web app...
echo.
echo Starting web server on http://localhost:5000
echo Open your browser and run Lighthouse audit!
echo.
echo Press Ctrl+C to stop the server
echo.

python app_web.py

pause
