import pygame
import time
import random

from suns.suns_gui import Suns_Gui

class Suns(Suns_Gui):
    def __init__(self, screen, grid, pos):
        super().__init__(screen=screen,grid=grid, pos=pos)
        self.__screen = screen
        self.__grid = grid

        self.__pos = pos
        
        self.__last_update_time = time.time()

        self.time_to_die = False

    def update(self):
        current_time = time.time()
        if current_time - self.__last_update_time <= 10:
            self.rect.y += 1
        else:
            self.time_to_die = True
        