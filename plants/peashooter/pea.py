import pygame
import time

from plants.peashooter.pea_gui import Pea_Gui

class Pea(Pea_Gui):
    def __init__(self, screen, grid, pos):
        super().__init__(screen, grid, pos)
        self.__attack_damage = 20

        self.__screen = screen
        self.__grid = grid
        self.__pos = pos

        self.last_time = time.time()
    
    def get_attack_damage(self):
        return self.__attack_damage

    def get_pos(self):
        return self.__pos
    
    def check_death(self):
        if self.rect.x >= self.__screen.get_width():
            self._ready_to_die = True
    
    def hitted_target(self):
        self.hit_target = True

    def is_ready_to_die(self):
        self.check_death()
        return self._ready_to_die

    def __repr__(self) -> str:
        return f'Pea {self.rect}'