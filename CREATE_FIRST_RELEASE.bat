@echo off
echo ========================================
echo Creating First Gestura Release
echo ========================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo Step 1: Committing all changes...
git add .
git commit -m "feat: Complete distribution infrastructure for external releases" 2>nul
if errorlevel 1 (
    echo No changes to commit or already committed
) else (
    echo Changes committed successfully
)

echo.
echo Step 2: Pushing to main branch...
git push origin main
if errorlevel 1 (
    echo Warning: Push failed. You may need to pull first.
    echo Run: git pull origin main
    pause
    exit /b 1
)

echo.
echo Step 3: Creating version tag v1.0.0...
git tag -a v1.0.0 -m "Release v1.0.0 - First Public Release"
if errorlevel 1 (
    echo Error: Failed to create tag
    pause
    exit /b 1
)

echo.
echo Step 4: Pushing tag to trigger GitHub Actions...
git push origin v1.0.0
if errorlevel 1 (
    echo Error: Failed to push tag
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Release Creation Started
echo ========================================
echo.
echo GitHub Actions is now building your release.
echo This will take about 15-20 minutes.
echo.
echo Monitor progress at:
echo https://github.com/veldorq/GesturaPrototype/actions
echo.
echo Once complete, your release will be available at:
echo https://github.com/veldorq/GesturaPrototype/releases
echo.
pause
