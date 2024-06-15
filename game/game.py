import pygame
import sys
import time
import random

from grid.grid import Grid
from agent.agent import Agent
from suns.suns import Suns

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

        self.regen_time = time.time()

        self.suns = []
    
    def reset(self, seed=None):
        pass

    def start_game(self):
        self.screen.fill(self.background)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.horde.update()

        self.update()

        self.draw()

        pygame.display.flip()

        self.clock.tick(self.fps)

    def update(self):
        self.regen_suns()
        self.agent.check_shoot_peashooter(self.horde.get_horde())

    def draw(self):
        self.grid.draw()
        for plant in self.agent.get_plants_owned():
            plant.draw()
        for zombie in self.horde.get_horde():
            if zombie.get_health() <= 0:
                self.horde.remove_zombie(zombie)
                break
            zombie.draw()
            zombie.update()
        for sun in self.agent.existing_suns:
            if sun.time_to_die:
                self.agent.existing_suns.remove(sun)
            sun.update()
            sun.draw()
        for pea in self.agent.get_all_pea_shot():
            pea.draw()
    
    def regen_suns(self):
        current_time = time.time()
        if current_time - self.regen_time >= 7.5:
            self.agent.existing_suns.append(Suns(self.screen,self.grid,(random.randint(1,9), -26)))
            self.regen_time = current_time
            
