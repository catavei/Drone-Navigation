import numpy as np
import matplotlib.pyplot as plt


def plot_data_over_episodes(data, title, y_label, window_size=100):
    """ Plots smoothed data over episodes with a configurable moving average window size. """
    smoothed_data = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    plt.figure(figsize=(12, 6))
    plt.plot(smoothed_data)
    plt.title(title)
    plt.xlabel('Episode')
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()


def plot_q_table(q_table):
    fig, ax = plt.subplots(figsize=(14, 14))
    max_q_values = np.max(q_table, axis=2)
    best_actions = np.argmax(q_table, axis=2)

    c = ax.matshow(max_q_values, cmap='coolwarm')
    fig.colorbar(c, ax=ax)

    # Define action vectors for arrow directions
    actions_dict = {0: (0, -1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)}  # Assuming 0: up, 1: down, 2: left, 3: right
    for i in range(q_table.shape[0]):
        for j in range(q_table.shape[1]):
            dx, dy = actions_dict[best_actions[i, j]]
            ax.arrow(j, i, dx, dy, head_width=0.5, head_length=0.5, fc='k', ec='k')

    ax.set_title('Policy Map with Directions')
    ax.set_xlabel('State X Coordinate')
    ax.set_ylabel('State Y Coordinate')
    plt.gca().invert_yaxis()  # Invert y-axis to match the array indexing
    plt.show()


def evaluate(q_table, env, episodes=10):
    total_rewards = 0
    max_steps_per_episode = 200  # Safeguard against infinite loops

    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        steps = 0

        while not done and steps < max_steps_per_episode:
            action = np.argmax(q_table[state])  # Choose best action based on learned Q-table
            state, reward, done, _, _ = env.step(action)
            total_rewards += reward
            steps += 1

        if steps >= max_steps_per_episode:
            print(f"Episode {episode + 1} reached max steps with no termination.")
        else:
            print(f'Episode {episode + 1}: reward = {reward}')

    avg_reward = total_rewards / episodes
    print(f'Average Reward: {avg_reward}')
    return avg_reward
