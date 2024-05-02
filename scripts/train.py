import numpy as np

from envs.drone_navigation_env import DroneNavigationEnv
from agents.dqn_agent import DQNAgent


def main():
    env = DroneNavigationEnv()
    agent = DQNAgent(state_size=2, action_size=4)  # Adjust based on your state and action space definitions
    episodes = 2

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, 2])

        for time in range(500):
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, 2])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"episode: {e + 1}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                break
        agent.replay(32)

        if e % 10 == 0:
            agent.save_model(f"dqn_model_{e}.keras")


if __name__ == "__main__":
    main()
