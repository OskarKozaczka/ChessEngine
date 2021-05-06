from tensorflow import keras
import tensorflow.keras.layers as layers
from tensorflow.keras.models import Sequential

model = Sequential([
    layers.Input(shape=(12, 8, 8)),
    layers.Conv2D(filters=64,kernel_size=3,padding="same" , activation='tanh'),
    layers.Conv2D(filters=64,kernel_size=3,padding="same", activation='tanh'),
    layers.Conv2D(filters=64,kernel_size=3,padding="same", activation='tanh'),
    layers.Conv2D(filters=64,kernel_size=3,padding="same", activation='tanh'),
    layers.Flatten(),
    layers.Dense(64),  
    layers.Dense(1)
])



model.compile(optimizer='adam', loss=keras.losses.mse)
model.summary()
#model.save('Data/Data')