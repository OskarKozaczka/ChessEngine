import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.layers as layers
from tensorflow.keras.models import Sequential
from tensorflow.python.keras.backend import flatten

model = Sequential([
    layers.Input(shape=(12, 8, 8)),
    layers.Conv2D(filters=64,kernel_size=3,padding="same" , activation='relu'),
    layers.BatchNormalization(),
    layers.Conv2D(filters=64,kernel_size=3,padding="same", activation='relu'),
    layers.BatchNormalization(),
    layers.Conv2D(filters=64,kernel_size=3,padding="same", activation='relu'),
    layers.BatchNormalization(),
    layers.Conv2D(filters=64,kernel_size=3,padding="same", activation='relu'),
    layers.BatchNormalization(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),  
    layers.Dense(1)
])



model.compile(optimizer='adam', loss=keras.losses.mse)
model.summary()
model.save('Data/Data')