import cv2
import numpy as np
from ultralytics import YOLO
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model

from feature_extractor import extract_features

# ---------------------------
# LOAD MODELS
# ---------------------------
yolo = YOLO("yolov8n.pt")

base = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
cnn_model = Model(inputs=base.input, outputs=base.output)

SEQ_LEN = 30

X = []
y = []

labels_map = {
    "walking": 0,
    "running": 1,
    "sitting": 2,
    "dancing": 3,
    "jumping": 4,
    "drinking": 5
}

def process_video(video_path, label_id):
    cap = cv2.VideoCapture(video_path)
    buffer = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = yolo(frame, verbose=False)

        for r in results:
            for box in r.boxes:
                if int(box.cls[0]) == 0:  # person
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    person = frame[y1:y2, x1:x2]

                    if person.size == 0:
                        continue

                    feat = extract_features(person, cnn_model)
                    buffer.append(feat)

        if len(buffer) == SEQ_LEN:
            X.append(buffer)
            y.append(label_id)
            buffer = []

    cap.release()

# ---------------------------
# MANUAL VIDEO INPUTS
# ---------------------------
process_video("walking.mp4", labels_map["walking"])
process_video("running.mp4", labels_map["running"])
process_video("sitting.mp4", labels_map["sitting"])
process_video("dancing.mp4", labels_map["dancing"])
process_video("jumping.mp4", labels_map["jumping"])
process_video("drinking.mp4", labels_map["drinking"])

# ---------------------------
# SAVE DATASET
# ---------------------------
X = np.array(X)
y = np.array(y)

np.save("X.npy", X)
np.save("y.npy", y)

print("Dataset created!")
print("X shape:", X.shape)
print("y shape:", y.shape)