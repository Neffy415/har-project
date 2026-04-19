#!/usr/bin/env python3
"""Quick diagnostic to check project status"""
import os
import glob
from pathlib import Path

print("\n" + "="*70)
print("HAR PROJECT DIAGNOSTIC")
print("="*70)

PROJECT_DIR = Path(__file__).parent
print(f"\n📍 Project Directory: {PROJECT_DIR}")
print(f"   Exists: {PROJECT_DIR.exists()}")

# Check dataset
print("\n📹 DATASET CHECK:")
dataset_dir = PROJECT_DIR / "dataset"
if dataset_dir.exists():
    video_files = list(dataset_dir.glob("*/*.mp4"))
    print(f"   Dataset folder: ✓ EXISTS")
    print(f"   Total MP4 files: {len(video_files)}")
    
    # Group by activity
    activities = {}
    for video_path in video_files:
        activity = video_path.parent.name
        if activity not in activities:
            activities[activity] = []
        size_mb = video_path.stat().st_size / (1024 * 1024)
        activities[activity].append((video_path.name, size_mb))
    
    for activity in sorted(activities.keys()):
        print(f"   └─ {activity}: {len(activities[activity])} videos")
        for name, size_mb in sorted(activities[activity])[:2]:
            print(f"      • {name}: {size_mb:.1f} MB")
else:
    print(f"   Dataset folder: ✗ NOT FOUND")

# Check output files
print("\n💾 OUTPUT FILES:")
output_files = ["X.npy", "y.npy", "label_names.npy", "model.h5"]
for fname in output_files:
    fpath = PROJECT_DIR / fname
    if fpath.exists():
        size_mb = fpath.stat().st_size / (1024 * 1024)
        print(f"   ✓ {fname}: {size_mb:.2f} MB")
    else:
        print(f"   ✗ {fname}: NOT FOUND")

# Check venv
print("\n🐍 PYTHON ENVIRONMENT:")
venv_dir = PROJECT_DIR / ".venv311"
if venv_dir.exists():
    python_exe = venv_dir / "Scripts" / "python.exe"
    if python_exe.exists():
        print(f"   Virtual env: ✓ EXISTS")
        print(f"   Python exe: ✓ {python_exe}")
    else:
        print(f"   Virtual env: ✗ BROKEN (python.exe missing)")
else:
    print(f"   Virtual env: ✗ NOT FOUND")

# Check models
print("\n🧠 PRETRAINED MODELS:")
yolo_model = PROJECT_DIR / "yolov8n.pt"
if yolo_model.exists():
    size_mb = yolo_model.stat().st_size / (1024 * 1024)
    print(f"   ✓ yolov8n.pt: {size_mb:.1f} MB")
else:
    print(f"   ✗ yolov8n.pt: NOT FOUND")

print("\n" + "="*70)
print("END DIAGNOSTIC")
print("="*70 + "\n")
