import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.layers as layers

model = tf.keras.Sequential([
    layers.Input(shape=(12, 8, 8)),
    layers.Conv2D(filters=32,kernel_size=3,padding="same" ,data_format='channels_last'),
    layers.Conv2D(filters=32,kernel_size=3,padding="same" ,data_format='channels_last'),
    layers.Conv2D(filters=32,kernel_size=3,padding="same" ,data_format='channels_last'),
    layers.Conv2D(filters=32,kernel_size=3,padding="same" ,data_format='channels_last'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),  
    layers.Dense(1)
])



model.compile(optimizer='adam', loss=keras.losses.mse,metrics=None)
model.summary()
model.save('Data/Data')