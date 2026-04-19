import cv2
import numpy as np
import os
import glob
from ultralytics import YOLO
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model

from feature_extractor import extract_features

# ---------------------------
# LOAD MODELS
# ---------------------------
print("[*] Loading YOLO model...")
yolo = YOLO("yolov8n.pt")

print("[*] Loading MobileNetV2 (first time may take 1-2 minutes to download weights)...")
base = MobileNetV2(weights="imagenet", include_top=False, pooling="avg", input_shape=(224, 224, 3))
cnn_model = Model(inputs=base.input, outputs=base.output)
print("[✓] Models loaded!")

SEQ_LEN = 30

X = []
y = []

labels_map = {
    "walking": 0,
    "resting": 1,
    "talking": 2,
    "standing": 3,
}

def process_video(video_path, label_id):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"      ✗ Cannot open video: {video_path}")
            return
        
        buffer = []
        frame_count = 0
        person_found_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            results = yolo(frame, verbose=False)

            best_person = None
            best_area = 0

            for r in results:
                for box in r.boxes:
                    if int(box.cls[0]) == 0:  # person
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        area = max(0, x2 - x1) * max(0, y2 - y1)
                        if area > best_area:
                            best_area = area
                            best_person = (x1, y1, x2, y2)

            if best_person is not None:
                person_found_count += 1
                x1, y1, x2, y2 = best_person
                person = frame[y1:y2, x1:x2]

                if person.size != 0:
                    feat = extract_features(person, cnn_model)
                    buffer.append(feat)

            if len(buffer) >= SEQ_LEN:
                X.append(buffer[:SEQ_LEN])
                y.append(label_id)
                buffer = buffer[SEQ_LEN:]

        cap.release()
        print(f"      ✓ Processed: {frame_count} frames, {person_found_count} with person, {len([i for i in range(len(y)) if y[i] == label_id])} sequences")
        
    except Exception as e:
        print(f"      ✗ Error processing {video_path}: {e}")

# ---------------------------
# READ VIDEOS FROM DATASET FOLDER
# ---------------------------
print("\n[*] Starting feature extraction from videos...")
dataset_root = "dataset"

for label_name, label_id in labels_map.items():
    label_dir = os.path.join(dataset_root, label_name)
    video_paths = sorted(glob.glob(os.path.join(label_dir, "*.mp4")))

    if not video_paths:
        print(f"⚠ Warning: no videos found in {label_dir}")
        continue

    print(f"\n[→] {label_name.upper()}: {len(video_paths)} videos")
    for idx, video_path in enumerate(video_paths, 1):
        print(f"   [{idx}/{len(video_paths)}] Processing {os.path.basename(video_path)}...")
        try:
            process_video(video_path, label_id)
        except Exception as e:
            print(f"   [!] Error: {e}")
            continue

# ---------------------------
# SAVE DATASET
# ---------------------------
X = np.array(X)
y = np.array(y)

if len(X) == 0:
    raise RuntimeError("No sequences were created. Check your downloaded videos in dataset/ folders.")

print(f"\n[✓] Dataset created!")
print(f"    X shape: {X.shape} (sequences, frames, features)")
print(f"    y shape: {y.shape}")
print(f"    Total sequences: {len(X)}")

np.save("X.npy", X)
np.save("y.npy", y)
np.save("label_names.npy", np.array(list(labels_map.keys())))

print(f"[✓] Saved X.npy, y.npy, label_names.npy")