#!/bin/bash
# ============================================
# Gestura Speed Optimization Deployment
# ============================================

echo ""
echo "========================================"
echo "  Gestura Speed Optimization Deploy"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run setup.sh first."
    exit 1
fi

echo "[1/4] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[2/4] Installing Flask-Compress..."
pip install Flask-Compress==1.14

echo ""
echo "[3/4] Verifying installations..."
python -c "from flask_compress import Compress; print('✓ Flask-Compress installed successfully')"

echo ""
echo "[4/4] Testing web app..."
echo ""
echo "Starting web server on http://localhost:5000"
echo "Open your browser and run Lighthouse audit!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app_web.py
