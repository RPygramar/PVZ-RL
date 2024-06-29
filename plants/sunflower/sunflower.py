import pygame

from plants.sunflower.sunflower_gui import Sunflower_Gui
from suns.suns import Suns
from plants.plant import Plant

class Sunflower(Plant, Sunflower_Gui):
    def __init__(self, screen, grid, pos, framerate=60):
        super().__init__(screen, grid, pos)
        self.__health = 300
        self.__ticks_before_attack = 24250
        self.__sun_cost = 50
        self.name = 'sunflower'

        self.__screen = screen
        self.__grid = grid
        self.__pos = pos
        self.__framerate = framerate

        self.__ticks_before_production = 24250  # example value, set as needed
        self.__accumulated_time = 0

        self.__list_suns = []

    def get_screen(self):
        return self.__screen

    def get_grid(self):
        return self.__grid
    
    def get_pos(self):
        return self.__pos

    def get_health(self):
        return self.__health
    
    def get_sun_cost(self):
        return self.__sun_cost
    
    def action(self, delta_time):
        self.__accumulated_time += delta_time * self.__framerate  # Scale delta time to make actions 60 times faster
        if self.__accumulated_time >= self.__ticks_before_production / self.__framerate:
            self.__accumulated_time -= self.__ticks_before_production
            self.__list_suns.append(Suns(self.__screen, self.__grid, (self.__pos[0] + 1, self.__pos[1]), True))

    def damage(self, value):
        self.__health -= value
    
    def get_list_suns(self):
        return self.__list_suns
    
    def remove_sun(self, sun:object):
        self.__list_suns.remove(sun)

    def get_pos(self):
        return self.__pos

    def __repr__(self) -> str:
        return f'Sunflower {self.__pos}'