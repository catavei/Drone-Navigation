# Configuration settings for the DroneNavigationEnv
AREA_SIZE = (30, 30)
MAX_STEPS = 200

# Action and learning parameters
ACTION_SIZE = 4
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99

# Exploration settings
EPSILON = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.99

# Training control
EPISODES = 2000
RANDOM_PICK_CHANCE = 0.1
