import pygame
import sys

from grid.grid import Grid
from agent.agent import Agent

from game.horde import Horde

class Game:
    def __init__(self, width=80*13, height=80*7, fps=60):
        pygame.init()
        pygame.display.set_caption("PVZ-RL")

        self.clock = pygame.time.Clock()

        screen_size = (width, height)
        self.screen = pygame.display.set_mode(screen_size)
        self.background = (60, 60, 60)
        self.fps = fps

        self.grid = Grid(screen=self.screen, cell_size=80)
        self.agent = Agent(screen=self.screen, grid=self.grid)
        
        self.horde = Horde(self.screen, self.grid)
    
    def reset(self, seed=None):
        pass

    def start_game(self):
        self.screen.fill(self.background)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.horde.update()

        self.draw()

        pygame.display.flip()

        self.clock.tick(self.fps)

    def draw(self):
        self.grid.draw()
        for plant in self.agent.get_plants_owned():
            plant.draw()
        for zombie in self.horde.get_horde():
            zombie.draw()
            zombie.update()