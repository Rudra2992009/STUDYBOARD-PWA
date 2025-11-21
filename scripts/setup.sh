#!/bin/bash
# STUDYBOARD PWA - Setup Script for Linux/Mac

set -e

echo "======================================"
echo "STUDYBOARD PWA - Setup Script"
echo "======================================"
echo ""

# Check Python version
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Found Python $PYTHON_VERSION"

if [ "$(echo "$PYTHON_VERSION < 3.10" | bc)" -eq 1 ]; then
    echo "Error: Python 3.10 or higher required"
    exit 1
fi

# Create virtual environment
echo ""
echo "[2/6] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv venv
    echo "Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "[3/6] Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "[4/6] Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "[5/6] Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Create necessary directories
echo ""
echo "[6/6] Creating directories..."
mkdir -p generated_images
mkdir -p models

echo ""
echo "======================================"
echo "Setup completed successfully!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start backend: cd backend && python server.py"
echo "3. Open browser: http://localhost:5000"
echo ""
echo "Note: First run will download models (~4GB)"
echo "This may take 10-30 minutes depending on internet speed."
echo ""