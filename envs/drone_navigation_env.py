import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces


class DroneNavigationEnv(gym.Env):
    def __init__(self, area_size=(600, 600), max_steps=100):
        super(DroneNavigationEnv, self).__init__()
        self.area_size = area_size
        self.max_steps = max_steps
        self.action_space = gym.spaces.Discrete(4)  # up, down, left, right
        self.observation_space = gym.spaces.Box(low=0, high=np.array([area_size[0], area_size[1]]), dtype=np.int32)

        pygame.init()
        self.screen = pygame.display.set_mode(area_size)
        self.clock = pygame.time.Clock()

        self.bg_color = pygame.Color('white')
        self.drone_color = pygame.Color('blue')
        self.target_color = pygame.Color('red')

        self.drone_size = 10
        self.target_size = 10

        self.target = np.random.randint(low=0, high=self.area_size, size=2)

        self.reset()

    def reset(self):
        self.position = np.random.randint(low=0, high=self.area_size, size=2)
        self.current_step = 0
        return self._get_obs()

    def _get_obs(self):
        return np.array(self.position, dtype=np.float32)

    def step(self, action):
        assert self.action_space.contains(action), f"Invalid Action: {action}"

        if action == 0:  # Move up
            self.position[1] = max(0, self.position[1] - 10)
        elif action == 1:  # Move down
            self.position[1] = min(self.area_size[1], self.position[1] + 10)
        elif action == 2:  # Move left
            self.position[0] = max(0, self.position[0] - 10)
        elif action == 3:  # Move right
            self.position[0] = min(self.area_size[0], self.position[0] + 10)

        self.current_step += 1

        done = np.array_equal(self.position, self.target) or self.current_step >= self.max_steps
        reward = 1 if np.array_equal(self.position, self.target) else -0.1

        return self._get_obs(), reward, done, {}


    def render(self, mode='human', close=False):
        if close:
            pygame.quit()
            return

        self.screen.fill(self.bg_color)
        pygame.draw.circle(self.screen, self.drone_color, self.position, self.drone_size)
        pygame.draw.circle(self.screen, self.target_color, self.target, self.target_size)

        pygame.display.flip()
        self.clock.tick(60)  # Control the frame rate

    def close(self):
        pygame.quit()
