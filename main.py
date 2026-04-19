import cv2
import numpy as np
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
feature_buffers = {}  # for multiple people tracking

labels = ["walking", "running", "sitting", "dancing", "jumping", "drinking"]

# -----------------------------
# CAMERA
# -----------------------------
cap = cv2.VideoCapture(0)

person_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = yolo(frame, verbose=False)

    current_ids = []

    # -----------------------------
    # DETECT PEOPLE
    # -----------------------------
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # person class
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                person_crop = frame[y1:y2, x1:x2]

                if person_crop.size == 0:
                    continue

                # assign ID (simple tracking)
                person_key = f"person_{person_id}"
                current_ids.append(person_key)

                if person_key not in feature_buffers:
                    feature_buffers[person_key] = []

                # extract CNN features
                feat = extract_features(person_crop, cnn_model)
                feature_buffers[person_key].append(feat)

                # keep last 30 frames
                if len(feature_buffers[person_key]) > SEQ_LEN:
                    feature_buffers[person_key].pop(0)

                # -----------------------------
                # PREDICT
                # -----------------------------
                if len(feature_buffers[person_key]) == SEQ_LEN:
                    seq = np.array(feature_buffers[person_key])
                    seq = np.expand_dims(seq, axis=0)

                    pred = model.predict(seq, verbose=0)
                    class_id = np.argmax(pred)
                    label = labels[class_id]

                    # draw result
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 2)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                person_id += 1

    # cleanup old people buffers (optional memory fix)
    feature_buffers = {k: v for k, v in feature_buffers.items() if k in current_ids}

    cv2.imshow("HAR - CNN + LSTM + YOLO", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()