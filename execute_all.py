#!/usr/bin/env python3
"""
HAR - Complete Automated Pipeline Executor
Runs the entire project from start to finish
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(r"C:\Users\titto\OneDrive\Desktop\amr\har")
VENV_PYTHON = str(PROJECT_DIR / ".venv311" / "Scripts" / "python.exe")

def log(msg, level="info"):
    """Print formatted log messages."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if level == "success":
        print(f"\n✓ [{timestamp}] {msg}")
    elif level == "error":
        print(f"\n✗ [{timestamp}] {msg}")
    elif level == "wait":
        print(f"⏳ [{timestamp}] {msg}", end="", flush=True)
    elif level == "info":
        print(f"→ [{timestamp}] {msg}")
    else:
        print(f"  {msg}")

def run_script(script_name, description, timeout_minutes=60):
    """Execute a Python script and wait for completion."""
    script_path = PROJECT_DIR / script_name
    
    log(f"\n{'='*70}", "info")
    log(f"STEP: {description}", "info")
    log(f"Script: {script_name}", "info")
    log(f"Timeout: {timeout_minutes} minutes", "info")
    log(f"{'='*70}\n", "info")
    
    start_time = time.time()
    
    try:
        # Run the script
        process = subprocess.Popen(
            [VENV_PYTHON, str(script_path)],
            cwd=str(PROJECT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Print output in real-time
        for line in process.stdout:
            print(line.rstrip())
        
        # Wait for completion
        returncode = process.wait(timeout=timeout_minutes * 60)
        
        elapsed = time.time() - start_time
        elapsed_min = int(elapsed) // 60
        elapsed_sec = int(elapsed) % 60
        
        if returncode == 0:
            log(f"{description} completed successfully! ({elapsed_min}m {elapsed_sec}s)", "success")
            return True
        else:
            log(f"{description} failed with exit code {returncode}", "error")
            return False
            
    except subprocess.TimeoutExpired:
        process.kill()
        log(f"{description} timed out after {timeout_minutes} minutes", "error")
        return False
    except Exception as e:
        log(f"{description} failed: {e}", "error")
        return False

def verify_files():
    """Check if all output files exist."""
    required_files = {
        "X.npy": "Training features",
        "y.npy": "Training labels",
        "label_names.npy": "Label names",
        "model.h5": "Trained model"
    }
    
    log(f"\n{'='*70}", "info")
    log("VERIFICATION: Output Files", "info")
    log(f"{'='*70}\n", "info")
    
    all_exist = True
    for filename, description in required_files.items():
        path = PROJECT_DIR / filename
        exists = path.exists()
        if exists:
            size_mb = round(path.stat().st_size / (1024*1024), 2)
            log(f"✓ {filename:<20} - {description} ({size_mb} MB)", "success")
        else:
            log(f"✗ {filename:<20} - {description} (MISSING)", "error")
            all_exist = False
    
    return all_exist

def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  HAR - COMPLETE AUTOMATED PIPELINE EXECUTOR".center(68) + "║")
    print("║" + "  Running: Download → Build → Train → Inference".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    log(f"Project Directory: {PROJECT_DIR}", "info")
    log(f"Python Executable: {VENV_PYTHON}", "info")
    
    # Check if Python exists
    if not Path(VENV_PYTHON).exists():
        log(f"Python executable not found: {VENV_PYTHON}", "error")
        return False
    
    log(f"Python version check...", "wait")
    result = subprocess.run([VENV_PYTHON, "--version"], capture_output=True, text=True)
    print(f" {result.stdout.strip()}")
    
    start_time = time.time()
    
    # STEP 1: Check/Download Videos
    log("\n" + "="*70, "info")
    log("STEP 1: Video Status Check", "info")
    log("="*70 + "\n", "info")
    
    video_count = len(list((PROJECT_DIR / "dataset").glob("**/*.mp4")))
    if video_count >= 12:
        log(f"✓ All {video_count} videos already downloaded", "success")
    else:
        log(f"Found {video_count}/12 videos. Downloading remaining...", "info")
        if not run_script("youtube_dataset.py", "Download Videos from YouTube", 30):
            log("Video download failed. Continuing anyway...", "error")
    
    # STEP 2: Build Dataset (Extract Features)
    if not run_script("build_dataset.py", "Extract CNN Features from Videos", 60):
        log("Feature extraction failed!", "error")
        return False
    
    # STEP 3: Train Model
    if not run_script("train_data.py", "Train LSTM Model", 30):
        log("Model training failed!", "error")
        return False
    
    # STEP 4: Verification
    if not verify_files():
        log("Some output files are missing!", "error")
        return False
    
    # STEP 5: Summary
    total_time = time.time() - start_time
    total_min = int(total_time) // 60
    total_sec = int(total_time) % 60
    
    log(f"\n{'='*70}", "info")
    log("PIPELINE COMPLETE!", "success")
    log(f"{'='*70}", "info")
    log(f"Total execution time: {total_min}m {total_sec}s\n", "info")
    
    log("✓ Ready for real-time inference!", "success")
    log("Next step: python main.py\n", "info")
    
    # STEP 6: Run Inference
    log(f"{'='*70}", "info")
    log("STEP 5: Starting Real-time Inference", "info")
    log(f"{'='*70}\n", "info")
    log("Opening webcam for real-time activity recognition...", "info")
    log("Press 'q' to quit inference\n", "info")
    
    # Run inference
    if not run_script("main.py", "Real-time Webcam Inference", 120):
        log("Inference completed or was interrupted", "info")
    
    # Final message
    log(f"\n{'='*70}", "info")
    log("PROJECT EXECUTION COMPLETE!", "success")
    log(f"{'='*70}\n", "info")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log("\n\nExecution interrupted by user", "error")
        sys.exit(1)
    except Exception as e:
        log(f"Fatal error: {e}", "error")
        sys.exit(1)
