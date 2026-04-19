#!/usr/bin/env python
"""
HAR Complete Pipeline Runner
Executes: download → build → train → verify
"""

import subprocess
import sys
import os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
VENV_PYTHON = PROJECT_DIR / ".venv311" / "Scripts" / "python.exe"

def run_step(name, script_name, timeout_minutes=60):
    """Run a Python script with the venv Python."""
    script_path = PROJECT_DIR / script_name
    
    print()
    print("=" * 60)
    print(f"[→] {name}")
    print("=" * 60)
    print(f"Running: {script_path}")
    print(f"Timeout: {timeout_minutes} minutes")
    print()
    
    try:
        result = subprocess.run(
            [str(VENV_PYTHON), str(script_path)],
            cwd=str(PROJECT_DIR),
            timeout=timeout_minutes * 60,
            check=True,
            capture_output=False,
            text=True
        )
        print()
        print(f"[✓] {name} completed successfully!")
        return True
    except subprocess.TimeoutExpired:
        print(f"[!] {name} timed out after {timeout_minutes} minutes")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[✗] {name} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"[✗] {name} failed: {e}")
        return False

def verify_files():
    """Check if output files exist."""
    print()
    print("=" * 60)
    print("[→] Verifying output files")
    print("=" * 60)
    
    files = {
        "X.npy": "Training features",
        "y.npy": "Training labels",
        "label_names.npy": "Class names",
        "model.h5": "Trained model"
    }
    
    all_exist = True
    for filename, description in files.items():
        path = PROJECT_DIR / filename
        exists = path.exists()
        status = "✓" if exists else "✗"
        size = f" ({path.stat().st_size / (1024*1024):.1f} MB)" if exists else ""
        print(f"{status} {filename:20s} - {description}{size}")
        all_exist = all_exist and exists
    
    return all_exist

def main():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║  HAR - Complete Pipeline Runner                        ║")
    print("║  Download Videos → Extract Features → Train → Verify   ║")
    print("╚" + "═" * 58 + "╝")
    
    # Check venv Python exists
    if not VENV_PYTHON.exists():
        print(f"ERROR: venv Python not found: {VENV_PYTHON}")
        print("Run setup.bat first to create the virtual environment")
        sys.exit(1)
    
    print(f"Python: {VENV_PYTHON}")
    print()
    
    # Run pipeline steps
    os.chdir(PROJECT_DIR)
    
    steps = [
        ("Download Videos", "youtube_dataset.py", 30),
        ("Build Dataset", "build_dataset.py", 60),  # 15-40 minutes
        ("Train Model", "train_data.py", 30),
    ]
    
    results = []
    for name, script, timeout in steps:
        success = run_step(name, script, timeout)
        results.append((name, success))
        if not success:
            print()
            print(f"[!] Stopping - {name} failed")
            break
    
    # Verify files
    all_files_exist = verify_files()
    
    # Summary
    print()
    print("=" * 60)
    print("[SUMMARY]")
    print("=" * 60)
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    if all_files_exist:
        print()
        print("[✓] All output files created successfully!")
        print()
        print("NEXT STEPS:")
        print("  python main.py  - Start real-time inference")
    else:
        print()
        print("[!] Some output files are missing")
    
    print()

if __name__ == "__main__":
    main()
