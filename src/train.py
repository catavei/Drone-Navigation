import numpy as np

from src.config import *
from src.utils import plot_data_over_episodes, pick_action, plot_q_table


def train(env):
    q_table = np.zeros(AREA_SIZE + (ACTION_SIZE,))
    epsilon = EPSILON

    rewards_per_episode = np.zeros(EPISODES)
    steps_per_episode = np.zeros(EPISODES)

    print("=== Training ===\n")

    for episode in range(EPISODES):
        state, _ = env.reset()
        done = False
        total_reward = 0
        steps = 0
        while not done:
            if np.random.rand() <= epsilon:
                action = np.random.randint(ACTION_SIZE)
            else:
                action = pick_action(state, q_table, ACTION_SIZE, AREA_SIZE, RANDOM_PICK_CHANCE)

            next_state, reward, done, _, _ = env.step(action)
            total_reward += reward

            q_table[state + (action,)] += LEARNING_RATE * (
                    reward + DISCOUNT_FACTOR * np.max(q_table[next_state]) - q_table[state + (action,)]
            )

            state = next_state
            steps += 1

        epsilon = max(epsilon * EPSILON_DECAY, EPSILON_MIN)
        rewards_per_episode[episode] = total_reward
        steps_per_episode[episode] = steps

        if episode % 200 == 0:
            print(f'Episode: {episode}, Epsilon: {epsilon:.2f}, Reward: {total_reward}, Steps: {steps}')

    np.save('models/q_table.npy', q_table)

    plot_data_over_episodes(rewards_per_episode, 'Rewards-Over-Episodes', 'Average Reward')
    plot_data_over_episodes(steps_per_episode, 'Steps-Per-Episode', 'Average Steps per Episode')
    plot_q_table(q_table)
    return env
