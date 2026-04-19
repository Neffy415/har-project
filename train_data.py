import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# ---------------------------
# LOAD DATA
# ---------------------------
X = np.load("X.npy")
y = np.load("y.npy")

if len(X) == 0:
    raise RuntimeError("X.npy is empty. Run build_dataset.py after downloading videos.")

# one-hot encode labels
y = to_categorical(y)

# ---------------------------
# MODEL
# ---------------------------
model = Sequential()

seq_len = X.shape[1]
feature_dim = X.shape[2]

model.add(LSTM(128, return_sequences=True, input_shape=(seq_len, feature_dim)))
model.add(Dropout(0.3))

model.add(LSTM(64))
model.add(Dropout(0.3))

model.add(Dense(64, activation='relu'))
model.add(Dense(y.shape[1], activation='softmax'))

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ---------------------------
# TRAIN
# ---------------------------
model.fit(X, y, epochs=10, batch_size=8, validation_split=0.2)

# ---------------------------
# SAVE MODEL
# ---------------------------
model.save("model.h5")

print("Model trained and saved!")