import numpy as np
from drone_navigation_env import DroneNavigationEnv
from config import *
from evaluate import evaluate
from utils import plot_data_over_episodes, pick_action, plot_q_table


def train():
    env = DroneNavigationEnv(AREA_SIZE, MAX_STEPS)
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

        if episode % 500 == 0:
            print(f'Episode: {episode}, Epsilon: {epsilon:.2f}, Reward: {total_reward}, Steps: {steps}')

    np.save('q_table.npy', q_table)

    plot_data_over_episodes(rewards_per_episode, 'Smoothed Rewards Over Episodes', 'Average Reward')
    plot_data_over_episodes(steps_per_episode, 'Smoothed Steps Per Episode', 'Average Steps per Episode')
    plot_q_table(q_table)

    evaluate(env, mode='render')


if __name__ == "__main__":
    np.random.seed(42)
    train()
