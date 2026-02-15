@echo off
REM Gestura Web Dashboard - Quick Start Script
REM Double-click this file to start the web server

echo.
echo ========================================
echo   GESTURA WEB DASHBOARD
echo   Starting Server...
echo ========================================
echo.

REM Check if dependencies are installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [!] Flask not found. Installing web dependencies...
    pip install -r requirements_web.txt
    echo.
)

REM Start the Flask server
echo [*] Starting Flask server on http://localhost:5000
echo [*] Press Ctrl+C to stop the server
echo.
echo [!] Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5000

python app.py

pause
