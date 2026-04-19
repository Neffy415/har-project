#!/usr/bin/env python3
"""Real-time pipeline progress monitor"""

import time
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(r"C:\Users\titto\OneDrive\Desktop\amr\har")

def get_python_memory():
    try:
        result = subprocess.run(
            ["powershell", "-Command", 
             "Get-Process python* -ErrorAction SilentlyContinue | Measure-Object -Property Memory -Sum | Select-Object -ExpandProperty Sum"],
            capture_output=True,
            text=True,
            timeout=5
        )
        mb = int(result.stdout.strip()) / (1024*1024) if result.stdout.strip() else 0
        return round(mb, 1)
    except:
        return 0

def get_video_count():
    videos = list((PROJECT_DIR / "dataset").glob("**/*.mp4"))
    return len(videos)

def print_header():
    print("\n" + "="*70)
    print(f"{'Time':<10} {'Status':<25} {'Memory':<15} {'Files':<10}")
    print("="*70)

print(f"\n🚀 HAR Pipeline Running in Background\n")
print(f"📁 Project: {PROJECT_DIR}")
print(f"🐍 Python: {PROJECT_DIR / '.venv311/Scripts/python.exe'}\n")

print_header()

stage = "Starting"
start_time = time.time()

while True:
    elapsed = int(time.time() - start_time)
    elapsed_min = elapsed // 60
    elapsed_sec = elapsed % 60
    
    # Check file status
    x_exists = (PROJECT_DIR / "X.npy").exists()
    y_exists = (PROJECT_DIR / "y.npy").exists()
    model_exists = (PROJECT_DIR / "model.h5").exists()
    
    # Determine stage
    if model_exists:
        stage = "✓ COMPLETE - Ready for inference"
        status = stage
    elif x_exists and y_exists:
        stage = "Training model..."
        status = f"🔄 {stage}"
    elif x_exists:
        stage = "Processing features..."
        status = f"🔄 {stage}"
    else:
        stage = "Extracting features..."
        status = f"⏳ {stage}"
    
    # Get memory usage
    mem = get_python_memory()
    
    # File status
    files_created = sum([x_exists, y_exists, model_exists])
    file_status = f"{files_created}/3"
    
    # Print status line
    timestamp = datetime.now().strftime("%H:%M:%S")
    elapsed_str = f"{elapsed_min}m {elapsed_sec}s"
    
    print(f"{timestamp:<10} {status:<25} {mem:.1f} MB            {file_status:<10}")
    
    if model_exists:
        print("\n" + "="*70)
        print("✓ PIPELINE COMPLETE!")
        print("="*70)
        print(f"\nCreated files:")
        print(f"  ✓ X.npy ({(PROJECT_DIR / 'X.npy').stat().st_size / (1024*1024):.1f} MB)")
        print(f"  ✓ y.npy ({(PROJECT_DIR / 'y.npy').stat().st_size / (1024*1024):.1f} MB)")
        print(f"  ✓ model.h5 ({(PROJECT_DIR / 'model.h5').stat().st_size / (1024*1024):.1f} MB)")
        print(f"\nTotal time: {elapsed_min}m {elapsed_sec}s")
        print(f"\n🎉 Next: python main.py  (for real-time inference)\n")
        break
    
    time.sleep(5)  # Update every 5 seconds
