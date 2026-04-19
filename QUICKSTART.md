# Quick Start Guide (5 Minutes)

## **For Windows Users**

### **Option 1: Automated Setup (Easiest)**
```bash
# 1. Double-click setup.bat
setup.bat

# 2. After setup completes, run:
python youtube_dataset.py

# 3. Wait 20-30 minutes for feature extraction + training
python build_dataset.py
python train_data.py

# 4. Run inference
python main.py
```

### **Option 2: Manual Setup**
```bash
# 1. Open Command Prompt in project folder

# 2. Create environment
python -m venv venv
venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download videos
python youtube_dataset.py

# 5. Extract features & train
python build_dataset.py
python train_data.py

# 6. Run webcam inference
python main.py
```

---

## **For macOS/Linux Users**

### **Option 1: Automated Setup**
```bash
bash setup.sh
python youtube_dataset.py
python build_dataset.py
python train_data.py
python main.py
```

### **Option 2: Manual Setup**
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python youtube_dataset.py
python build_dataset.py
python train_data.py
python main.py
```

---

## **Monitoring Progress**

### **Check if Build is Running** (Windows)
```powershell
# Open new terminal and run:
Get-Process python* | Select-Object Name, CPU, Memory
```

### **Check if Files Were Generated**
```bash
# Check for created files
ls -la *.npy *.h5

# If you see X.npy, y.npy, model.h5 → SUCCESS!
```

---

## **Real-time Inference**

Once `main.py` is running:

- **Your webcam** will show detected person with activity label
- **Press 'Q'** to quit
- **Press 'S'** to save a screenshot
- **Confidence score** shown in green text

---

## **Still Having Issues?**

See [README.md](README.md) **Troubleshooting** section.

### **Quick Checks**

```bash
# Verify Python version
python --version  # Should be 3.10 or 3.11

# Verify dependencies installed
pip list | grep -E "tensorflow|ultralytics|opencv"

# Test YOLO
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Test TensorFlow
python -c "import tensorflow as tf; print(tf.__version__)"
```

---

**Estimated Total Time**: 45-60 minutes (mostly waiting for processing)
- Download videos: 5-10 min
- Extract features: 15-30 min
- Train model: 5-10 min
- First inference: < 1 sec per frame

Enjoy! 🎉
