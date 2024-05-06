import numpy as np

from config import AREA_SIZE, MAX_STEPS
from drone_navigation_env import DroneNavigationEnv
from evaluate import evaluate
from train import train

if __name__ == "__main__":
    np.random.seed(42)
    drone_env = DroneNavigationEnv(AREA_SIZE, MAX_STEPS)
    train(drone_env)
    evaluate(drone_env, mode='render')
