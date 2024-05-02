import tensorflow as tf
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.python.keras.models import Sequential


def create_dqn_model(input_shape, num_actions):
    model = Sequential([
        InputLayer(input_shape=input_shape),
        Dense(24, activation='relu'),
        Dense(24, activation='relu'),
        Dense(num_actions, activation='linear')  # No activation on the output layer
    ])
    model.compile(optimizer='adam', loss='mse')
    return model
