#!/usr/bin/env python3
"""
Automatic Pipeline Monitor & Executor
Waits for feature extraction, then trains model
"""

import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(r"C:\Users\titto\OneDrive\Desktop\amr\har")
VENV_PYTHON = PROJECT_DIR / ".venv311" / "Scripts" / "python.exe"

def log(msg, status=""):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status == "ok":
        symbol = "✓"
    elif status == "wait":
        symbol = "⏳"
    elif status == "error":
        symbol = "✗"
    else:
        symbol = "→"
    print(f"[{timestamp}] {symbol} {msg}")

def check_files():
    """Check which files exist."""
    files = {
        "X.npy": PROJECT_DIR / "X.npy",
        "y.npy": PROJECT_DIR / "y.npy",
        "model.h5": PROJECT_DIR / "model.h5",
    }
    return {name: path.exists() for name, path in files.items()}

def get_file_size_mb(path):
    """Get file size in MB."""
    if path.exists():
        return round(path.stat().st_size / (1024*1024), 2)
    return None

def main():
    log("HAR Pipeline Automatic Executor", "ok")
    log(f"Project: {PROJECT_DIR}")
    log(f"Python: {VENV_PYTHON}")
    
    # Step 1: Wait for feature extraction to complete
    log("Waiting for build_dataset.py to complete...", "wait")
    while True:
        files = check_files()
        if files["X.npy"] and files["y.npy"]:
            x_size = get_file_size_mb(PROJECT_DIR / "X.npy")
            y_size = get_file_size_mb(PROJECT_DIR / "y.npy")
            log(f"Feature extraction complete! X.npy ({x_size}MB), y.npy ({y_size}MB)", "ok")
            break
        else:
            elapsed = int(time.time()) % 60
            log(f"Still processing features...", "wait")
            time.sleep(30)  # Check every 30 seconds
    
    # Step 2: Train model
    log("Starting model training...", "")
    try:
        result = subprocess.run(
            [str(VENV_PYTHON), str(PROJECT_DIR / "train_data.py")],
            cwd=str(PROJECT_DIR),
            timeout=30*60,  # 30 minute timeout
            check=True
        )
        log("Model training complete!", "ok")
    except Exception as e:
        log(f"Training failed: {e}", "error")
        return False
    
    # Step 3: Verify files
    log("Verifying output files...", "")
    files = check_files()
    
    if files["model.h5"]:
        model_size = get_file_size_mb(PROJECT_DIR / "model.h5")
        log(f"✓ model.h5 created ({model_size}MB)", "ok")
    else:
        log("✗ model.h5 not found", "error")
    
    # Summary
    print()
    print("=" * 60)
    print("PIPELINE COMPLETE!")
    print("=" * 60)
    for name, exists in files.items():
        status = "✓" if exists else "✗"
        print(f"{status} {name}")
    
    print()
    print("Next: Run 'python main.py' for real-time inference")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
