from envs.drone_navigation_env import DroneNavigationEnv
from agents.dqn_agent import DQNAgent
import numpy as np

def main():
    env = DroneNavigationEnv()
    agent = DQNAgent(state_size=2, action_size=4, model_path='dqn_model.h5')
    agent.model.load_weights('path_to_your_model.h5')  # Load the model

    for e in range(100):  # Number of evaluation episodes
        state = env.reset()
        state = np.reshape(state, [1, 2])
        total_reward = 0

        while True:
            action = agent.act(state)
            state, reward, done, _ = env.step(action)
            state = np.reshape(state, [1, 2])
            total_reward += reward
            if done:
                print(f"Episode: {e+1}, Total reward: {total_reward}")
                break

if __name__ == "__main__":
    main()
