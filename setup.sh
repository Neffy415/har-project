#!/bin/bash

# HAR Setup Script for macOS/Linux
# Usage: bash setup.sh

echo ""
echo "========================================"
echo " HAR (Human Activity Recognition) Setup"
echo "========================================"
echo ""

# Check Python version
echo "[1/5] Checking Python installation..."
if ! command -v python3.11 &> /dev/null; then
    echo "WARNING: Python 3.11 not found. Trying python3..."
    if ! command -v python3 &> /dev/null; then
        echo "ERROR: Python 3 is not installed"
        echo "Please install Python 3.11 from https://www.python.org/"
        exit 1
    fi
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python3.11"
fi

$PYTHON_CMD --version
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Using existing venv."
else
    $PYTHON_CMD -m venv venv
    echo "Virtual environment created."
fi

echo ""

# Activate venv and install dependencies
echo "[3/5] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""

# Run diagnostic
echo "[4/5] Verifying installation..."
python check_project.py

echo ""

# Final instructions
echo "[5/5] Setup complete!"
echo ""
echo "========================================"
echo " NEXT STEPS"
echo "========================================"
echo ""
echo "To activate the environment next time:"
echo "  source venv/bin/activate"
echo ""
echo "To run the project:"
echo "  1. Download videos:    python youtube_dataset.py"
echo "  2. Extract features:   python build_dataset.py (15-30 min)"
echo "  3. Train model:        python train_data.py (5-10 min)"
echo "  4. Run inference:      python main.py"
echo ""
echo "Press Enter to exit..."
read
