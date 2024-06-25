import pygame
import time
import random

from zombies.zombie_normal.zombie_normal import Zombie_Normal

class Horde:
    def __init__(self, screen, grid):
        self.__screen = screen
        self.__grid = grid

        self.__horde = []

        self.__n_zombies = None

    def update(self):
        self.fill_horde()

    def get_horde(self):
        return self.__horde
    
    def remove_zombie(self, zombie :object):
        self.__horde.remove(zombie)
    
    def fill_horde(self):
        if not self.__horde:
            if not self.__n_zombies:
                self.__n_zombies = random.randint(1,5)
                # self.__n_zombies = 1
            horde = [Zombie_Normal(self.__screen,self.__grid, pos=(10, random.randint(1,5))) for n in range(self.__n_zombies)]
            self.__n_zombies = None
            self.__horde = horde
