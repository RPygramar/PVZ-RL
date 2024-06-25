import pygame

from plants.peashooter.peashooter_gui import Peashooter_Gui
from plants.peashooter.pea import Pea


class Peashooter(Peashooter_Gui):
    def __init__(self, screen, grid, pos):
        super().__init__(screen, grid, pos)
        self.__health = 300
        self.__attack_damage = 20
        self.__ticks_before_attack = 1400
        self.__sun_cost = 100
        self.name = 'peashooter'

        self.__screen = screen
        self.__grid = grid
        self.__pos = pos

        self.__last_shot_time = pygame.time.get_ticks()

        self.__list_peas = []

    def get_health(self):
        return self.__health
    
    def get_attack_damage(self):
        return self.__attack_damage
    
    def get_ticks_before_attack(self):
        return self.__ticks_before_attack
    
    def get_sun_cost(self):
        return self.__sun_cost
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.__last_shot_time >= self.__ticks_before_attack:
            self.__last_shot_time = current_time
            self.__list_peas.append(Pea(self.__screen, self.__grid,self.__pos))

    def get_pos(self):
        return self.__pos
    
    def damage(self, value):
        self.__health -= value
    
    def get_peas_shoot(self):
        for pea in self.__list_peas:
            if pea.hit_target or pea.is_ready_to_die():
                self.__list_peas.remove(pea)
        return self.__list_peas

    def __repr__(self) -> str:
        return f'Peashooter {self.__pos}'