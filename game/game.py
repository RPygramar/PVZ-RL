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
        self.grid = Grid(screen=self.screen, cell_size=80)
        self.agent = Agent(screen=self.screen, grid=self.grid)
        
        self.horde = Horde(self.screen, self.grid)

        self.regen_time = time.time()

        self.suns = []

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
        self.agent.plants_behavior(self.horde.get_horde())
        self.agent.remove_dead_plants()
        if self.check_zombies_reached_limit():
            self.reset()
        

    def draw(self):
        self.grid.draw()
        for plant in self.agent.get_plants_owned():
            plant.draw()

        for zombie in self.horde.get_horde():
            if zombie.get_health() <= 0:
                self.horde.remove_zombie(zombie)
                self.agent.add_zombies_killed(zombie=zombie)
            if zombie.rect.collidelist(self.agent.get_plants_owned()) >= 0:
                zombie.eat_plant(self.agent.get_plants_owned()[zombie.rect.collidelist(self.agent.get_plants_owned())])
                # print(self.agent.get_plants_owned()[zombie.rect.collidelist(self.agent.get_plants_owned())].get_health())
            else:
                zombie.set_eating(boolean=False)
            zombie.draw()
            zombie.update()

        for sun in self.agent.existing_suns:
            if sun.time_to_die:
                self.agent.existing_suns.remove(sun)
            sun.update()
            sun.draw()

        for element in self.agent.get_all_elements():
            element.draw()
    
    def regen_suns(self):
        current_time = time.time()
        if current_time - self.regen_time >= 7.5:
            self.agent.existing_suns.append(Suns(self.screen,self.grid,(random.randint(1,9), -1),False))
            self.regen_time = current_time

    def check_zombies_reached_limit(self):
        for zombie in self.horde.get_horde():
            if zombie.rect.right <= 0:
                return True
        return False
            
