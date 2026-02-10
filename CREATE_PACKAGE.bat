@echo off
title Hand Gesture Control - One-Click Package
color 0A
cls
echo.
echo ========================================
echo   ONE-CLICK PACKAGE CREATOR
echo ========================================
echo.
echo Creating the SIMPLEST package for users...
echo Users will just: Extract → Double-click → Enjoy!
echo.

REM Create distribution folder
set DIST_FOLDER=HandGestureControl_OneClick
echo Creating package folder...
if exist "%DIST_FOLDER%" rmdir /s /q "%DIST_FOLDER%"
mkdir "%DIST_FOLDER%"

REM Check if .exe exists
if exist "dist\HandGestureControl.exe" (
    echo.
    echo ✓ Found standalone .exe
    echo   Creating ONE-CLICK package...
    echo.
    
    REM Copy just the exe
    copy "dist\HandGestureControl.exe" "%DIST_FOLDER%\"
    
    REM Create minimal quick start
    (
        echo ========================================
        echo   HAND GESTURE CONTROL - START HERE
        echo ========================================
        echo.
        echo DOUBLE-CLICK: HandGestureControl.exe
        echo.
        echo That's all! No installation needed.
        echo.
        echo ========================================
        echo   QUICK GESTURES
        echo ========================================
        echo.
        echo Open Palm = Scroll Down
        echo Closed Fist = Scroll Up
        echo Index Finger = Move Cursor
        echo Three Fingers = Click
        echo.
        echo Press Q = Quit
        echo.
        echo ========================================
        echo   TIPS
        echo ========================================
        echo.
        echo - Allow camera access when prompted
        echo - Keep hand visible in frame
        echo - Use good lighting
        echo - Practice for 2 minutes
        echo.
        echo The app shows gesture hints on screen!
        echo.
        echo ========================================
    ) > "%DIST_FOLDER%\START.txt"
    
    echo ✓ ONE-CLICK package ready!
    echo.
    echo Package: %DIST_FOLDER%
    echo Contains: Just the .exe + simple instructions
    echo.
    
) else (
    echo ✗ No .exe found!
    echo.
    echo Please run BUILD_ONE_CLICK.bat first to create the executable.
    echo.
    pause
    exit /b 1
)

echo ========================================
echo   READY TO SHARE!
echo ========================================
echo.
echo WHAT'S IN THE PACKAGE:
echo   ✓ HandGestureControl.exe (one file, works instantly)
echo   ✓ START.txt (simple instructions)
echo.
echo NEXT STEPS:
echo   1. Test: Open folder and run the .exe
echo   2. Compress: Right-click folder → "Compressed folder"
echo   3. Share: Email or upload ZIP to Google Drive
echo.
echo USERS WILL:
echo   1. Extract ZIP
echo   2. Double-click .exe
echo   3. Click "Allow" for camera
echo   4. Start gesturing!
echo.
echo NO Python, NO installation, NO complexity!
echo.
pause

REM Open the folder
start "" "%DIST_FOLDER%"
