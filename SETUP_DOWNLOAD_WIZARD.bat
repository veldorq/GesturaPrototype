@echo off
REM ============================================
REM  SUPER SIMPLE - Make Download Work
REM ============================================

echo.
echo ============================================
echo   GESTURA - QUICK DOWNLOAD FIX
echo ============================================
echo.
echo This wizard will help you set up downloads
echo for your users in just a few steps.
echo.
echo Press any key to start...
pause >nul

:MENU
cls
echo.
echo ============================================
echo   CHOOSE YOUR METHOD
echo ============================================
echo.
echo   You only need to do ONE of these:
echo.
echo   [1] Google Drive Upload (EASIEST - 5 min)
echo.
echo   [2] Manual GitHub Release (Medium - 10 min)
echo.
echo   [3] Show me the instructions (Read first)
echo.
echo   [Q] Quit
echo.
set /p choice="Enter your choice (1, 2, 3, or Q): "

if /i "%choice%"=="1" goto GOOGLE_DRIVE
if /i "%choice%"=="2" goto GITHUB_MANUAL
if /i "%choice%"=="3" goto INSTRUCTIONS
if /i "%choice%"=="Q" goto END
goto MENU

:GOOGLE_DRIVE
cls
echo.
echo ============================================
echo   METHOD 1: GOOGLE DRIVE (Easiest)
echo ============================================
echo.
echo STEP 1: First, let's build Gestura.exe
echo.
echo Press any key to start building...
pause >nul

echo.
echo Building Gestura executable...
echo (This takes 2-5 minutes)
echo.
call BUILD_AND_SHARE.bat

if errorlevel 1 (
    echo.
    echo ERROR: Build failed. Check the errors above.
    pause
    goto MENU
)

echo.
echo ============================================
echo   BUILD COMPLETE!
echo ============================================
echo.
echo STEP 2: Upload to Google Drive
echo.
echo   1. Open Windows Explorer
echo   2. Find "Gestura-Release" folder (created above)
echo   3. Right-click → Send to → Compressed (zipped) folder
echo   4. Open browser: https://drive.google.com
echo   5. Click "New" → "File upload"
echo   6. Upload the Gestura-Release.zip file
echo   7. After upload, right-click the file → Share
echo   8. Set to "Anyone with the link"
echo   9. Copy the link
echo.
pause

echo.
echo STEP 3: Convert to direct download link
echo.
echo Your Google Drive link looks like:
echo https://drive.google.com/file/d/1xYz789ABC/view?usp=sharing
echo.
echo You need to change it to:
echo https://drive.google.com/uc?export=download^&id=1xYz789ABC
echo.
echo Just copy the FILE_ID (the part between /d/ and /view)
echo.
echo Now, enter your FILE_ID (the random characters):
set /p fileid="FILE_ID: "

if "%fileid%"=="" (
    echo ERROR: You must enter a FILE_ID
    pause
    goto GOOGLE_DRIVE
)

set "DOWNLOAD_URL=https://drive.google.com/uc?export=download&id=%fileid%"

echo.
echo Your direct download URL is:
echo %DOWNLOAD_URL%
echo.
echo STEP 4: Update website code
echo.
echo Opening the file you need to edit...
echo.
pause

notepad "gestura-web\src\components\DownloadButtons.tsx"

echo.
echo Find this line (around line 35):
echo   const CUSTOM_DOWNLOAD_URL = '';
echo.
echo Change it to:
echo   const CUSTOM_DOWNLOAD_URL = '%DOWNLOAD_URL%';
echo.
echo Save the file and close Notepad.
echo.
pause

echo.
echo STEP 5: Deploy the website
echo.
echo Press any key to deploy (requires git)...
pause >nul

cd gestura-web
git add .
git commit -m "Add working download link"
git push

if errorlevel 1 (
    echo.
    echo Warning: Git push failed.
    echo You may need to manually deploy your website.
) else (
    echo.
    echo SUCCESS! Website deployed.
)

cd ..

echo.
echo ============================================
echo   DONE!
echo ============================================
echo.
echo Your download is now live!
echo.
echo TEST IT:
echo   1. Open your website in Incognito mode
echo   2. Click Download button
echo   3. Verify file downloads directly
echo.
pause
goto END

:GITHUB_MANUAL
cls
echo.
echo ============================================
echo   METHOD 2: MANUAL GITHUB RELEASE
echo ============================================
echo.
echo STEP 1: Building executable...
echo.
call BUILD_AND_SHARE.bat

if errorlevel 1 (
    echo.
    echo ERROR: Build failed.
    pause
    goto MENU
)

echo.
echo ============================================
echo   BUILD COMPLETE!
echo ============================================
echo.
echo STEP 2: Create GitHub Release
echo.
echo   1. Open: https://github.com/veldorq/GesturaPrototype/releases/new
echo.
echo   2. Fill in:
echo      - Tag: v1.0.0
echo      - Title: Gestura v1.0.0
echo.
echo   3. Drag and drop the Gestura-Release folder (as ZIP)
echo      Or upload Gestura-Release.zip if you created it
echo.
echo   4. Click "Publish release"
echo.
echo   5. After publishing, right-click the uploaded ZIP file
echo.
echo   6. Copy the download link
echo.
echo   7. It should look like:
echo      https://github.com/USER/REPO/releases/download/v1.0.0/file.zip
echo.
start https://github.com/veldorq/GesturaPrototype/releases/new
echo.
echo Browser opened. Complete the steps above, then come back here.
echo.
pause

echo.
echo Now enter your release download URL:
set /p release_url="GitHub Release URL: "

echo.
echo Updating website code with: %release_url%
echo.

REM Update the download URL in DownloadButtons.tsx
powershell -Command "(Get-Content 'gestura-web\src\components\DownloadButtons.tsx') -replace \"const CUSTOM_DOWNLOAD_URL = '';\", \"const CUSTOM_DOWNLOAD_URL = '%release_url%';\" | Set-Content 'gestura-web\src\components\DownloadButtons.tsx'"

echo Done! Deploying website...
cd gestura-web
git add .
git commit -m "Add GitHub release download link"
git push
cd ..

echo.
echo ============================================
echo   SUCCESS!
echo ============================================
pause
goto END

:INSTRUCTIONS
cls
type QUICK_START_CARD.txt
echo.
echo.
echo For more details, see: EASY_DOWNLOAD_SETUP.md
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:END
echo.
echo Thanks for using Gestura!
echo.
