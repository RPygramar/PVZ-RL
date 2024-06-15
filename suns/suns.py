import pygame
import time
import random

from suns.suns_gui import Suns_Gui

class Suns(Suns_Gui):
    def __init__(self, screen, grid, pos, is_sunflower=False):
        super().__init__(screen=screen,grid=grid, pos=pos)
        self.__screen = screen
        self.__grid = grid

        self.__is_sunflower = is_sunflower
        self.__pos = pos
        
        self.__last_update_time = time.time()

        self.time_to_die = False

        self.__value = 50

    def update(self):
        current_time = time.time()
        if current_time - self.__last_update_time <= 10:
            if not self.__is_sunflower: 
                self.rect.y += 1
        else:
            self.time_to_die = True

    def get_value(self):
        return self.__value
    
    def __repr__(self) -> str:
        return f'Sun'
        