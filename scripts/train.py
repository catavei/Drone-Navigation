import numpy as np

from envs.drone_navigation_env import DroneNavigationEnv
from scripts.utils import plot_data_over_episodes, evaluate, plot_q_table


def train():
    area_size = (20, 20)
    max_steps = 200
    action_size = 4
    epsilon = 1.0
    epsilon_min = 0.01
    epsilon_decay = 0.99
    learning_rate = 0.1
    discount_factor = 0.99
    env = DroneNavigationEnv(area_size, max_steps)

    episodes = 5000
    rewards_per_episode = np.zeros(episodes)
    steps_per_episode = np.zeros(episodes)

    q_table = np.zeros(area_size + (action_size,))

    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        steps = 0
        while not done:
            if np.random.rand() <= epsilon:
                action = np.random.randint(4)
            else:
                action = np.argmax(q_table[state])

            next_state, reward, done, _, _ = env.step(action)

            q_table[state + (action,)] = (q_table[state + (action,)] + learning_rate * (
                    reward + discount_factor * np.max(q_table[next_state]) - q_table[state + (action,)]))

            state = next_state
            steps += 1

            if episode % 100 == 0:
                env.render()

        epsilon = max(epsilon * epsilon_decay, epsilon_min)
        if epsilon == epsilon_min:
            learning_rate = 0.0001

        rewards_per_episode[episode] = reward
        steps_per_episode[episode] = steps
        if episode % 100 == 0:
            print(f'Episode: {episode}, Epsilon: {epsilon:.2f}')

    np.save('q_table.npy', q_table)

    evaluate(q_table, env)
    plot_data_over_episodes(rewards_per_episode, 'Smoothed Rewards Over Episodes', 'Average Reward')
    plot_data_over_episodes(steps_per_episode, 'Smoothed Steps Per Episode', 'Average Steps per Episode')
    plot_q_table(q_table)


if __name__ == "__main__":
    np.random.seed(42)
    train()
