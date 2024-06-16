import pygame
import time

from plants.sunflower.sunflower_gui import Sunflower_Gui
from suns.suns import Suns

class Sunflower(Sunflower_Gui):
    def __init__(self, screen, grid, pos):
        super().__init__(screen, grid, pos)
        self.__health = 300
        self.__ticks_before_attack = 24.25
        self.__sun_cost = 50
        self.name = 'sunflower'

        self.__screen = screen
        self.__grid = grid
        self.__pos = pos

        self.__last_sunproduced_time = time.time()

        self.__list_suns = []

    def get_health(self):
        return self.__health
    
    def get_attack_damage(self):
        return self.__attack_damage
    
    def get_ticks_before_attack(self):
        return self.__ticks_before_attack
    
    def get_sun_cost(self):
        return self.__sun_cost
    
    def produce_suns(self):
        current_time = time.time()
        if current_time - self.__last_sunproduced_time >= 24.25:
            self.__last_sunproduced_time = current_time
            self.__list_suns.append(Suns(self.__screen, self.__grid,(self.__pos[0]+1,self.__pos[1]),True))
    
    def get_list_suns(self):
        return self.__list_suns
    
    def remove_sun(self, sun:object):
        self.__list_suns.remove(sun)

    def damage(self, value):
        self.__health -= value

    def get_pos(self):
        return self.__pos

    def __repr__(self) -> str:
        return f'Sunflower {self.__pos}'