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

### For Windows:
1. Clone this repository: `git clone https://github.com/amlan478/amr.git`
2. Open the folder: `cd amr`
3. Double-click `setup.bat` (or run it in terminal). This will install everything automatically.
4. Run: `python execute_all.py`

### For macOS / Linux:
1. Clone this repository: `git clone https://github.com/amlan478/amr.git`
2. Open the folder: `cd amr`
3. Make the setup script executable: `chmod +x setup.sh`
4. Run it: `./setup.sh`
5. Run: `python3 execute_all.py`

The pipeline takes about 20-40 minutes to download files, build sequences, and train. Once done, your webcam will pop up with the real-time activity tracker! Press 'Q' to exit the camera window.

Enjoy! 🎉