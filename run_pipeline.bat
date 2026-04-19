@echo off
REM Complete HAR Pipeline - Batch Script
REM This script runs the entire pipeline: download, build, train, infer

setlocal enabledelayedexpansion

cd /d "C:\Users\titto\OneDrive\Desktop\amr\har"

echo.
echo ========================================
echo HAR - Complete Pipeline Execution
echo ========================================
echo.

REM Step 1: Check venv Python
echo [1/4] Checking venv Python...
"C:\Users\titto\OneDrive\Desktop\amr\har\.venv311\Scripts\python.exe" --version
if errorlevel 1 (
    echo ERROR: venv Python not found
    pause
    exit /b 1
)

REM Step 2: Download videos (already done, but can re-run)
echo.
echo [2/4] Checking if videos are downloaded...
if exist "dataset\walking\walking_0.mp4" (
    echo Videos already present. Skipping download.
) else (
    echo Downloading videos...
    "C:\Users\titto\OneDrive\Desktop\amr\har\.venv311\Scripts\python.exe" youtube_dataset.py
)

REM Step 3: Build dataset (extract features)
echo.
echo [3/4] Extracting features from videos...
echo This may take 15-40 minutes. Please wait...
"C:\Users\titto\OneDrive\Desktop\amr\har\.venv311\Scripts\python.exe" build_dataset.py
if errorlevel 1 (
    echo ERROR: Feature extraction failed
    pause
    exit /b 1
)

REM Step 4: Train model
echo.
echo [4/4] Training LSTM model...
echo This may take 5-15 minutes...
"C:\Users\titto\OneDrive\Desktop\amr\har\.venv311\Scripts\python.exe" train_data.py
if errorlevel 1 (
    echo ERROR: Model training failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo PIPELINE COMPLETE!
echo ========================================
echo.
echo Files created:
echo   X.npy         - Training features
echo   y.npy         - Training labels
echo   model.h5      - Trained model
echo.
echo Next: Run 'python main.py' to start inference
echo.
pause
