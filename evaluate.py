import numpy as np

from config import ACTION_SIZE, AREA_SIZE, RANDOM_PICK_CHANCE
from utils import pick_action


def evaluate(env, mode="render"):
    if mode == "render":
        episodes = 10
    elif mode == "eval":
        episodes = 1000
    else:
        return "Invalid mode"

    q_table = np.load('q_table.npy')
    total_rewards = 0
    max_steps_per_episode = 100
    successful_landings = 0
    total_steps = 0
    if mode == "render":
        print("\n=== Evaluation ===\n")
    else:
        print("\n=== Rendering ===\n")
    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        steps = 0

        while not done and steps < max_steps_per_episode:
            action = pick_action(state, q_table, ACTION_SIZE, AREA_SIZE, RANDOM_PICK_CHANCE)
            state, reward, done, _, _ = env.step(action)
            total_rewards += reward
            steps += 1

            if mode == 'render':
                env.render(mode='human')

        if steps >= max_steps_per_episode:
            print(f"Episode {episode + 1} reached max steps with no termination.")
        else:
            print(f'Episode {episode + 1}: Landed in {steps} steps.')
            successful_landings += 1
        total_steps += steps

    average_steps = total_steps / episodes
    landing_rate = successful_landings / episodes
    if mode == "eval":
        print(f'\nSuccessful landings: {landing_rate * 100:.2f}%')
        print(f'Average steps per episode: {average_steps:.0f}')
    return landing_rate
