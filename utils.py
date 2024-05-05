import numpy as np
import matplotlib.pyplot as plt


def plot_data_over_episodes(data, title, y_label, window_size=100):
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
    plt.show()


def pick_action(state, q_table, action_size, area_size, random_pick_chance=0.1):
    y, x = state
    potential_actions = list(range(action_size))

    # Remove out-of-bound actions
    if y == 0:  # Can't move up if at the top edge
        potential_actions.remove(0)
    if y == area_size[0] - 1:  # Can't move down if at the bottom edge
        potential_actions.remove(1)
    if x == 0:  # Can't move left if at the left edge
        potential_actions.remove(2)
    if x == area_size[1] - 1:  # Can't move right if at the right edge
        potential_actions.remove(3)

    best_action = max(potential_actions, key=lambda a: q_table[state][a])

    # Introduce randomness to avoid deterministic loops
    if np.random.rand() < random_pick_chance:
        return np.random.choice(potential_actions)
    else:
        return best_action
