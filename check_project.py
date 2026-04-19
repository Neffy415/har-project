#!/usr/bin/env python3
import os
import glob
import sys

print("=" * 70)
print("PROJECT STATUS CHECK - HAR (Human Activity Recognition)")
print("=" * 70)

# 1. Check video files
print("\n[1] VIDEOS DOWNLOADED")
walking_vids = glob.glob("dataset/walking/*.mp4")
resting_vids = glob.glob("dataset/resting/*.mp4")
print(f"    Walking videos: {len(walking_vids)} files")
if walking_vids:
    for v in sorted(walking_vids):
        size_mb = os.path.getsize(v) / (1024*1024)
        print(f"      - {os.path.basename(v)} ({size_mb:.1f} MB)")

print(f"    Resting videos: {len(resting_vids)} files")
if resting_vids:
    for v in sorted(resting_vids):
        size_mb = os.path.getsize(v) / (1024*1024)
        print(f"      - {os.path.basename(v)} ({size_mb:.1f} MB)")

if len(walking_vids) >= 2 and len(resting_vids) >= 2:
    print("    ✓ PASS: Sufficient video data")
else:
    print("    ✗ FAIL: Need at least 2 videos per class")

# 2. Check Python dependencies
print("\n[2] PYTHON DEPENDENCIES")
deps = {
    "cv2": "OpenCV",
    "numpy": "NumPy",
    "ultralytics": "YOLO v8",
    "tensorflow": "TensorFlow",
    "yt_dlp": "yt-dlp",
}

all_ok = True
for module, name in deps.items():
    try:
        __import__(module)
        print(f"    ✓ {name:20s} - installed")
    except ImportError as e:
        print(f"    ✗ {name:20s} - MISSING")
        all_ok = False

if all_ok:
    print("    ✓ PASS: All dependencies available")
else:
    print("    ✗ FAIL: Some dependencies missing")

# 3. Check code files
print("\n[3] SOURCE CODE FILES")
files = {
    "youtube_dataset.py": "Dataset downloader",
    "build_dataset.py": "Feature extractor",
    "train_data.py": "Model trainer",
    "main.py": "Real-time inference",
    "feature_extractor.py": "Feature utility",
}

all_exist = True
for fname, desc in files.items():
    if os.path.exists(fname):
        size = os.path.getsize(fname)
        print(f"    ✓ {fname:25s} - {size} bytes")
    else:
        print(f"    ✗ {fname:25s} - MISSING")
        all_exist = False

if all_exist:
    print("    ✓ PASS: All code files present")
else:
    print("    ✗ FAIL: Missing code files")

# 4. Check dataset generation status
print("\n[4] DATASET PIPELINE")
if os.path.exists("X.npy") and os.path.exists("y.npy"):
    import numpy as np
    X = np.load("X.npy")
    y = np.load("y.npy")
    print(f"    ✓ X.npy exists: shape {X.shape}")
    print(f"    ✓ y.npy exists: shape {y.shape}")
    print(f"    ✓ PASS: Feature dataset ready")
else:
    print(f"    ✗ X.npy missing")
    print(f"    ✗ y.npy missing")
    print(f"    ⚠ INFO: Run build_dataset.py to generate training data")

# 5. Check trained model
print("\n[5] TRAINED MODEL")
if os.path.exists("model.h5"):
    size_mb = os.path.getsize("model.h5") / (1024*1024)
    print(f"    ✓ model.h5 exists ({size_mb:.1f} MB)")
    print("    ✓ PASS: Model ready for inference")
else:
    print(f"    ✗ model.h5 missing")
    print(f"    ⚠ INFO: Run train_data.py to generate trained model")

# 6. Project readiness
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

ready_for = []
if len(walking_vids) >= 2 and len(resting_vids) >= 2:
    ready_for.append("Download/re-download videos")

if all_exist:
    ready_for.append("Run code scripts")

if os.path.exists("X.npy") and os.path.exists("y.npy") and all_ok:
    ready_for.append("Train model")
    
if os.path.exists("model.h5") and all_ok:
    ready_for.append("Run inference (webcam)")

if ready_for:
    print("✓ PROJECT IS READY FOR:")
    for item in ready_for:
        print(f"  • {item}")
else:
    print("✗ PROJECT INCOMPLETE - NEXT STEPS:")
    print("  1. Ensure Python 3.11+ is active")
    print("  2. Install: pip install tensorflow ultralytics opencv-python yt-dlp numpy")
    print("  3. Run: python build_dataset.py")
    print("  4. Run: python train_data.py")
    print("  5. Run: python main.py")

print("=" * 70)
