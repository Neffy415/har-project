# 🎯 Human Activity Recognition (HAR) - Real-time Video Classification

A deep learning project that detects and classifies human activities in real-time using YOLO, MobileNetV2 CNN, and LSTM neural networks.

## **Activities Recognized**
- 🚶 **Walking** - Person moving on foot
- 🧘 **Resting** - Person sitting or stationary  
- 💬 **Talking** - Person speaking/communicating
- 🪑 **Standing** - Person standing still

---

## **System Requirements**

- **Python**: 3.10 or 3.11 (NOT 3.14+, TensorFlow compatibility)
- **OS**: Windows, macOS, or Linux
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5GB free space (for models + videos)
- **GPU**: Optional (NVIDIA CUDA for faster training, but CPU works fine)

---

## **Quick Start (5 minutes)**

### **1. Clone & Setup**
```bash
# Clone repository
git clone https://github.com/your-username/har.git
cd har

# Create Python 3.11 virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Download Training Videos**
```bash
python youtube_dataset.py
```
This downloads 12 YouTube videos (~5-10 MB) for the 4 activity classes.

### **3. Extract Features & Train Model**
```bash
# Extract CNN features from videos (takes 15-30 minutes)
python build_dataset.py

# Train LSTM model (takes 5-10 minutes)
python train_data.py
```

### **4. Run Real-time Detection**
```bash
# Start webcam activity recognition
python main.py
```
Press **'q'** to quit.

---

## **Project Structure**

```
har/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .gitignore                     # Ignore large files
├── youtube_dataset.py             # Download training videos
├── build_dataset.py               # Extract CNN features
├── train_data.py                  # Train LSTM model
├── main.py                        # Real-time inference
├── feature_extractor.py           # Feature extraction utility
├── check_project.py               # Status checker
├── dataset/                       # Downloaded videos
│   ├── walking/
│   ├── resting/
│   ├── talking/
│   └── standing/
├── X.npy                          # Training features (generated)
├── y.npy                          # Training labels (generated)
├── model.h5                       # Trained model (generated)
└── label_names.npy               # Class names (generated)
```

---

## **How It Works**

### **Pipeline Overview**

```
YouTube Videos
    ↓
[build_dataset.py] - Extracts 1280-D features per frame using MobileNetV2
    ↓
X.npy (sequences of 30 frames, each 1280-D)
    ↓
[train_data.py] - Trains LSTM model to classify sequences
    ↓
model.h5 (trained LSTM neural network)
    ↓
[main.py] - Real-time webcam inference
    ↓
Activity Labels (walking, resting, talking, standing)
```

### **Technical Details**

1. **Object Detection**: YOLO v8 Nano detects people in each frame
2. **Feature Extraction**: MobileNetV2 (pre-trained on ImageNet) extracts visual features
3. **Temporal Modeling**: LSTM processes 30-frame sequences to classify activities
4. **Architecture**:
   - Input: 30 frames × 1280 features
   - LSTM layers: 128 → 64 units with Dropout
   - Output: 4 activity classes (softmax)

---

## **File Descriptions**

| File | Purpose |
|------|---------|
| `youtube_dataset.py` | Downloads videos from YouTube for each activity class |
| `build_dataset.py` | Processes videos: YOLO detection → MobileNetV2 features → datasets |
| `train_data.py` | Trains LSTM model on extracted features |
| `main.py` | Real-time webcam inference with activity labels & confidence |
| `feature_extractor.py` | Helper function to extract CNN features from image crops |
| `check_project.py` | Diagnostic tool to verify setup and pipeline status |

---

## **Troubleshooting**

### **Issue: "No module named 'tensorflow'"**
```bash
# Make sure you're using Python 3.11 (not 3.14+)
python --version

# Reinstall TensorFlow
pip install --upgrade tensorflow
```

### **Issue: "YOLOv8 model not found"**
YOLO automatically downloads on first run (~100MB). If it fails:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### **Issue: "No webcam detected"**
```bash
# Check available cameras
python -c "import cv2; print(cv2.VideoCapture(0).get(cv2.CAP_PROP_FRAME_WIDTH))"

# Try different camera indices (0, 1, 2...)
# Edit main.py: cap = cv2.VideoCapture(1)  # Change 0 to 1, 2, etc.
```

### **Issue: Low accuracy or wrong predictions**
- Ensure good lighting and clear person visibility
- Train on more videos (add more YouTube links in `youtube_dataset.py`)
- Increase training epochs in `train_data.py`

---

## **Performance Notes**

| Component | Time | Hardware |
|-----------|------|----------|
| Download videos | 5-10 min | Internet speed |
| Extract features | 15-30 min | GPU (2-5 min), CPU (15-30 min) |
| Train model | 5-10 min | GPU (1-2 min), CPU (5-10 min) |
| Real-time inference | 25-30 FPS | GPU (60 FPS), CPU (25-30 FPS) |

---

## **Customization**

### **Add Your Own Videos**
Edit `youtube_dataset.py`:
```python
video_links = {
    "activity_name": [
        "https://youtube.com/watch?v=VIDEO_ID",
        # Add more links...
    ]
}
```

### **Use Local Videos Instead**
Create folders in `dataset/`:
```
dataset/
├── activity1/
│   ├── video1.mp4
│   ├── video2.mp4
│   └── ...
└── activity2/
    ├── video1.mp4
    └── ...
```

### **Increase Training Quality**
In `train_data.py`:
```python
model.fit(X, y, 
    epochs=50,           # Increase from 10
    batch_size=4,        # Decrease from 8 (smaller batch = slower but better)
    validation_split=0.2
)
```

---

## **Advanced: GPU Acceleration**

If you have NVIDIA GPU:
```bash
# Install CUDA-enabled TensorFlow
pip install tensorflow[and-cuda]

# Verify GPU detection
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

---

## **License**

MIT License - Feel free to use for learning and projects!

---

## **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Commit changes: `git commit -m "Add new feature"`
4. Push to branch: `git push origin feature/my-improvement`
5. Open a Pull Request

---

## **Future Improvements**

- [ ] Support for multi-person tracking
- [ ] Add more activity classes
- [ ] Export model to ONNX/TensorFlow Lite for mobile
- [ ] Web interface with Flask/Streamlit
- [ ] Gesture recognition integration
- [ ] Pose estimation overlay

---

## **Authors**

Created for human activity recognition education and research.

---

## **Questions & Support**

For issues or questions, please open a GitHub issue or email: your-email@example.com

---

**Last Updated**: April 2026
