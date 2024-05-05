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
        self.target = tuple(np.random.randint(low=0, high=self.area_size, size=2))#tuple([area_size[0]//2, area_size[1]//2])
        self.state = None
        self.steps_beyond_done = None
        self.max_steps = max_steps  # Maximum steps per episode
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
            # Continue to punish the agent if called after the episode is done
            return self.state, -10, True, {}

        # Initialize move as no change
        y, x = self.state
        out_of_bounds = False

        if action == 0:  # up
            if y > 0:
                y -= 1
            else:
                out_of_bounds = True
        elif action == 1:  # down
            if y < self.area_size[0] - 1:
                y += 1
            else:
                out_of_bounds = True
        elif action == 2:  # left
            if x > 0:
                x -= 1
            else:
                out_of_bounds = True
        elif action == 3:  # right
            if x < self.area_size[1] - 1:
                x += 1
            else:
                out_of_bounds = True

        # Update the state only if not out of bounds
        if not out_of_bounds:
            self.state = (y, x)

        self.current_step += 1
        # self.done = self.state == self.target or self.current_step >= self.max_steps or out_of_bounds
        self.done = self.state == self.target or out_of_bounds

        if self.state == self.target:
            self.reward = 10  # Reward for reaching the target
        elif out_of_bounds:
            self.reward = -10  # Heavy penalty for going out of bounds
        else:
            self.reward = -0.1  # Small penalty for each step to encourage efficiency

        return self.state, self.reward, self.done, False, {}

    def render(self, mode='human'):
        if mode == 'human':
            self.screen.fill((0, 0, 0))  # Fill the screen with black

            # Draw target
            target_rect = pygame.Rect(self.target[1] * self.scale, self.target[0] * self.scale, self.scale, self.scale)
            pygame.draw.rect(self.screen, (255, 0, 0), target_rect)  # Red target

            # Draw drone
            drone_rect = pygame.Rect(self.state[1] * self.scale, self.state[0] * self.scale, self.scale, self.scale)
            pygame.draw.rect(self.screen, (0, 255, 0), drone_rect)  # Green drone

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Ensures a maximum of 60 frames per second

    def close(self):
        pygame.quit()
