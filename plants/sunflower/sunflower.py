import pygame

from plants.sunflower.sunflower_gui import Sunflower_Gui

class Sunflower(Sunflower_Gui):
    def __init__(self, screen, grid, pos):
        super().__init__(screen, grid, pos)
        self.__health = 300
        self.__ticks_before_attack = 24.25
        self.__sun_cost = 50
        self.name = 'sunflower'

        self.__pos = pos

    def get_health(self):
        return self.__health
    
    def get_attack_damage(self):
        return self.__attack_damage
    
    def get_ticks_before_attack(self):
        return self.__ticks_before_attack
    
    def get_sun_cost(self):
        return self.__sun_cost
    
    def __repr__(self) -> str:
        return f'Sunflower {self.__pos}'