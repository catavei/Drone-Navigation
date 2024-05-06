"""
Defines the Drone Navigation environment based on Gymnasium API.
Handles the dynamics and rules of the drone's movement and interactions within the environment.
"""
import numpy as np
import gymnasium as gym
import pygame
from gymnasium import spaces


class DroneNavigationEnv(gym.Env):
    metadata = {'render.modes': ['human', 'console']}

    def __init__(self, area_size, max_steps):
        self.area_size = area_size
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Tuple((spaces.Discrete(area_size[0]), spaces.Discrete(area_size[1])))
        self.target = tuple(np.random.randint(low=0, high=self.area_size, size=2))
        self.state = None
        self.steps_beyond_done = None
        self.max_steps = max_steps
        self.current_step = 0
        self.reward = 0
        self.done = False

        self.screen_size = 600
        self.scale = self.screen_size // max(self.area_size)
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        self.clock = pygame.time.Clock()

    def reset(self):
        self.state = tuple(np.random.randint(low=0, high=self.area_size, size=2))
        self.action_space = spaces.Discrete(4)
        self.current_step = 0
        self.steps_beyond_done = None
        self.reward = 0
        return self.state, {}

    def step(self, action):
        if self.steps_beyond_done is not None:
            return self.state, -10, True, {}

        # Move mapping (action: (delta_y, delta_x))
        move_map = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}

        y, x = self.state

        if action in move_map:
            dy, dx = move_map[action]
            new_y, new_x = y + dy, x + dx
        else:
            # Invalid action, no movement
            new_y, new_x = y, x

        out_of_bounds = not (0 <= new_y < self.area_size[0] and 0 <= new_x < self.area_size[1])

        if not out_of_bounds:
            self.state = (new_y, new_x)

        self.current_step += 1
        self.done = self.state == self.target or out_of_bounds

        if self.state == self.target:
            reward = 10  # Reward for reaching the target
        elif out_of_bounds:
            reward = -10  # Penalty for going out of bounds
        else:
            reward = -0.1  # Step penalty

        return self.state, reward, self.done, False, {}

    def render(self, mode='human'):
        if mode == 'human':
            self.screen.fill((0, 0, 0))

            target_rect = pygame.Rect(self.target[1] * self.scale, self.target[0] * self.scale, self.scale, self.scale)
            pygame.draw.rect(self.screen, (255, 0, 0), target_rect)

            drone_rect = pygame.Rect(self.state[1] * self.scale, self.state[0] * self.scale, self.scale, self.scale)
            pygame.draw.rect(self.screen, (0, 255, 0), drone_rect)

            pygame.display.flip()  # Update the display
            self.clock.tick(30)

    def close(self):
        pygame.quit()
