import cv2
import numpy as np
import os
from ultralytics import YOLO
from tensorflow.keras.models import load_model

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from feature_extractor import extract_features

# -----------------------------
# LOAD MODELS
# -----------------------------
yolo = YOLO("yolov8n.pt")
model = load_model("model.h5")

# CNN (MUST MATCH TRAINING)
base = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
cnn_model = Model(inputs=base.input, outputs=base.output)

# -----------------------------
# SETTINGS
# -----------------------------
SEQ_LEN = 30
feature_buffer = []

if os.path.exists("label_names.npy"):
    labels = np.load("label_names.npy", allow_pickle=True).tolist()
else:
    labels = ["walking", "resting", "talking", "standing"]

if model.output_shape[-1] != len(labels):
    raise RuntimeError(
        f"Model output classes ({model.output_shape[-1]}) do not match labels ({len(labels)}). Retrain with train_data.py."
    )

# -----------------------------
# CAMERA
# -----------------------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = yolo(frame, verbose=False)

    # -----------------------------
    # DETECT PEOPLE
    # -----------------------------
    best_person = None
    best_area = 0

    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # person class
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = max(0, x2 - x1) * max(0, y2 - y1)
                if area > best_area:
                    best_area = area
                    best_person = (x1, y1, x2, y2)

    if best_person is not None:
        x1, y1, x2, y2 = best_person
        person_crop = frame[y1:y2, x1:x2]

        if person_crop.size != 0:
            # extract CNN features
            feat = extract_features(person_crop, cnn_model)
            feature_buffer.append(feat)

            # keep last 30 frames
            if len(feature_buffer) > SEQ_LEN:
                feature_buffer.pop(0)

            # -----------------------------
            # PREDICT
            # -----------------------------
            if len(feature_buffer) == SEQ_LEN:
                seq = np.array(feature_buffer)
                seq = np.expand_dims(seq, axis=0)

                pred = model.predict(seq, verbose=0)[0]
                class_id = int(np.argmax(pred))
                label = labels[class_id]
                confidence = float(pred[class_id])

                # draw result
                cv2.putText(frame, f"{label} ({confidence:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imshow("HAR - CNN + LSTM + YOLO", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()