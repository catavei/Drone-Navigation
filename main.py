import numpy as np

from config import AREA_SIZE, MAX_STEPS
from drone_navigation_env import DroneNavigationEnv
from evaluate import evaluate
from train import train

# if __name__ == "__main__":
#     np.random.seed(42)
#     drone_env = DroneNavigationEnv(AREA_SIZE, MAX_STEPS)
#     train(drone_env)
#     drone_env.reset()
#     evaluate(drone_env, mode='render')

import argparse
import numpy as np
from config import AREA_SIZE, MAX_STEPS
from drone_navigation_env import DroneNavigationEnv
from evaluate import evaluate
from train import train


def main(mode):
    drone_env = DroneNavigationEnv(AREA_SIZE, MAX_STEPS)

    if mode == 'train':
        train(drone_env)
    elif mode == 'eval':
        evaluate(drone_env, mode='eval')
    elif mode == 'render':
        evaluate(drone_env, mode='render')
    else:
        raise ValueError("Unsupported mode. Choose 'train', 'eval', or 'render'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Drone Navigation environment.")
    parser.add_argument('--mode', type=str, choices=['train', 'eval', 'render'], required=True,
                        help="Mode to run the environment: 'train', 'eval', or 'render'.")

    args = parser.parse_args()
    np.random.seed(42)

    main(args.mode)
