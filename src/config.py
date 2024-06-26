"""
Configuration module for the Drone Navigation project.
Defines global constants and parameters used across various modules.
"""
AREA_SIZE = (30, 30)
MAX_STEPS = 200

ACTION_SIZE = 4
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99

EPSILON = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.99

EPISODES = 2000
RANDOM_PICK_CHANCE = 0.3
