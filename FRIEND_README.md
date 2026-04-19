# HAR Project Setup Guide 🚀

Hey! This repository contains a fully automated end-to-end Human Activity Recognition pipeline.

It tracks 4 activities from live webcam video: **Walking, Resting, Talking, Standing**.

## What it does:
1. **Downloads** YouTube videos automatically 
2. **Extracts features** using YOLOv8 Nano & MobileNetV2
3. **Trains** an LSTM Neural Network on those sequences
4. **Runs** real-time webcam inference

## 🔧 How to run this on your machine

You only need **Python 3.11** installed. That's it!

### ⚡ QUICK START (5 minutes to working webcam!)

#### For Windows:
```
1. git clone https://github.com/Neffy415/har-project.git
2. cd har-project
3. Double-click setup.bat
4. python main.py
```

#### For macOS / Linux:
```
1. git clone https://github.com/Neffy415/har-project.git
2. cd har-project
3. chmod +x setup.sh
4. ./setup.sh
5. python3 main.py
```

---

## 📋 Step-by-Step Instructions

### Step 1: Clone the Repository
Extract this repository to your computer:
```bash
git clone https://github.com/Neffy415/har-project.git
cd har-project
```

### Step 2: Install Python Dependencies
The repository includes a pre-trained model, so NO training needed!

**Windows Users:**
- Double-click `setup.bat` 
- Or run in PowerShell: `python setup.bat`

**Mac/Linux Users:**
- Run: `chmod +x setup.sh && ./setup.sh`

This will automatically:
- Create a Python 3.11 virtual environment
- Install TensorFlow, OpenCV, YOLO, and all dependencies

### Step 3: Run Real-Time Activity Recognition
Once setup completes, launch the webcam inference:

**Windows:**
```bash
python main.py
```

**Mac/Linux:**
```bash
python3 main.py
```

A webcam window will open showing:
- 🟢 **Green bounding box** around detected people
- 📝 **Activity label** (Walking / Resting / Talking / Standing)
- 📊 **Confidence percentage** (e.g., "WALKING (94%)")

### Step 4: Exit
Press **'Q'** on your keyboard to close the camera window.

---

## ✨ What's Different from Other HAR Projects?

- ✅ **Pre-trained model included** - No waiting 20-40 minutes for training
- ✅ **Features already extracted** - Just run `main.py` and see it work
- ✅ **Fully automated setup** - One script does everything
- ✅ **Real-time on CPU** - Runs smoothly on any laptop

---

## 🎯 That's it!

Your activity recognition system is ready to use immediately after cloning! 🎉