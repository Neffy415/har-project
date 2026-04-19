@echo off
REM Windows Setup Script for HAR Project
REM Author: HAR Team
REM This script sets up the HAR project on Windows

echo.
echo ========================================
echo  HAR (Human Activity Recognition) Setup
echo ========================================
echo.

REM Check Python version
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python: %PYTHON_VERSION%

REM Create virtual environment
echo.
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Using existing venv.
) else (
    python -m venv venv
    echo Virtual environment created.
)

REM Activate venv and install dependencies
echo.
echo [3/5] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Run diagnostic
echo.
echo [4/5] Verifying installation...
python check_project.py

REM Final instructions
echo.
echo [5/5] Setup complete!
echo.
echo ========================================
echo  NEXT STEPS
echo ========================================
echo.
echo To activate the environment next time:
echo   venv\Scripts\activate.bat
echo.
echo To run the project:
echo   1. Download videos:    python youtube_dataset.py
echo   2. Extract features:   python build_dataset.py (15-30 min)
echo   3. Train model:        python train_data.py (5-10 min)
echo   4. Run inference:      python main.py
echo.
echo Press any key to exit...
pause
