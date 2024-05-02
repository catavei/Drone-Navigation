import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from collections import deque
import random


class DQNAgent:
    def __init__(self, state_size, action_size, model_path=None):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount factor
        self.epsilon = 1.0   # exploration rate initially high
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("base_path:", base_path)
        self.checkpoint_directory = os.path.join(base_path, 'checkpoints/')

        os.makedirs(self.checkpoint_directory, exist_ok=True)  # Ensure directory exists
        if model_path:
            self.model.load_weights(os.path.join(self.checkpoint_directory, model_path))  # Load weights if path provided

    def _build_model(self):
        model = Sequential([
            tf.keras.layers.Input(shape=(self.state_size,)),  # Specify input shape here
            Dense(24, activation='relu'),
            Dense(24, activation='relu'),
            Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model


    def save_model(self, filename='dqn_model.keras'):
        full_path = os.path.join(self.checkpoint_directory, filename)
        self.model.save(full_path)  # Save the model to file
        print(f"Model saved to {full_path}")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size=32):
        minibatch = random.sample(self.memory, min(len(self.memory), batch_size))
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
