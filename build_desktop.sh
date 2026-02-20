#!/bin/bash

echo "========================================"
echo "Building Gestura Executable"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install pyinstaller
else
    source venv/bin/activate
fi

# Install PyInstaller if needed
if ! pip show pyinstaller > /dev/null 2>&1; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

echo ""
echo "Building standalone executable..."
echo "This may take 2-5 minutes..."
echo ""

# Determine OS for path separator
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macOS"
    PATH_SEP=":"
else
    OS_TYPE="Linux"
    PATH_SEP=":"
fi

# Build executable
pyinstaller --onefile \
    --name "Gestura" \
    --add-data "models${PATH_SEP}models" \
    --add-data "config${PATH_SEP}config" \
    --hidden-import="mediapipe" \
    --hidden-import="cv2" \
    --hidden-import="pyautogui" \
    --hidden-import="numpy" \
    --hidden-import="PIL" \
    --hidden-import="dataclasses" \
    --collect-all mediapipe \
    --console \
    main.py

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Executable location: dist/Gestura"
echo ""
echo "To create distribution package:"
echo "  1. mkdir release"
echo "  2. cp dist/Gestura release/"
echo "  3. cp END_USER_INSTALL_GUIDE.md release/README.txt"
echo "  4. cp USER_GUIDE.md release/"
echo "  5. cd release && zip -r ../Gestura-${OS_TYPE}-x64.zip . && cd .."
echo "  6. Upload to GitHub Releases"
echo ""
echo "Users will download the ZIP, extract, and run ./Gestura"
echo ""
