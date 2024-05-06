import numpy as np
import matplotlib.pyplot as plt


def plot_data_over_episodes(data: np.ndarray, title: str, y_label: str, window_size: int = 500) -> None:
    """
        Description:
            Plots smoothed data (rewards or steps) over episodes.

        Args:
            data (np.ndarray): The data array to plot, typically rewards or steps per episode.
            title (str): The title of the plot.
            y_label (str): The label for the y-axis.
            window_size (int): The size of the window to use for smoothing the data with a moving average.
    """

    smoothed_data = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    plt.figure(figsize=(12, 6))
    plt.plot(smoothed_data)
    plt.title(title)
    plt.xlabel('Episode')
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()


def plot_q_table(q_table: np.ndarray) -> None:
    """
    Description:
        Plots the Q-table as a heatmap with arrows indicating the best action per state.

    Args:
        q_table (np.ndarray): The Q-table to be plotted. It should be a 3D array where the first two
                              dimensions correspond to the state space and the third dimension to action values.

    """
    fig, ax = plt.subplots(figsize=(14, 14))
    max_q_values = np.max(q_table, axis=2)
    best_actions = np.argmax(q_table, axis=2)

    c = ax.matshow(max_q_values, cmap='coolwarm')
    fig.colorbar(c, ax=ax)

    actions_dict = {0: (0, -1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)}  # Assuming 0: up, 1: down, 2: left, 3: right
    for i in range(q_table.shape[0]):
        for j in range(q_table.shape[1]):
            dx, dy = actions_dict[best_actions[i, j]]
            ax.arrow(j, i, dx, dy, head_width=0.5, head_length=0.5, fc='k', ec='k')

    ax.set_title('Policy Map with Directions')
    ax.set_xlabel('State X Coordinate')
    ax.set_ylabel('State Y Coordinate')
    plt.show()


def pick_action(state: tuple, q_table: np.ndarray, action_size: int, area_size: tuple, random_pick_chance: float = 0.1) -> int:
    """
     Args:
        state (tuple): Current state of the agent, expressed as (y, x) coordinates.
        q_table (numpy.ndarray): The Q-table containing accumulated Q-values for state-action pairs.
        action_size (int): Total number of possible actions the agent can take.
        area_size (tuple): Dimensions of the environment (height, width).
        random_pick_chance (float): Probability of choosing a random action to facilitate exploration.

    Description:
        This function picks an action (up, down, left, right) for a given state from Q table.
        It introduces a chance of choosing another action with a `random_pick_chance` probability to avoid
        the case where two neighbouring states "point" to each other, introducing an infinite loop.

    Returns:
        int: The chosen action, which is either the best action according to the Q-table or a random valid action.
    """

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

    if np.random.rand() < random_pick_chance:
        return np.random.choice(potential_actions)
    else:
        return best_action
