import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

def extract_features(img, cnn_model):
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    features = cnn_model.predict(img, verbose=0)
    return features.flatten()   # 1280-d vector