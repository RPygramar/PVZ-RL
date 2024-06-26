import pygame

from plants.peashooter.peashooter_gui import Peashooter_Gui
from plants.peashooter.pea import Pea
from plants.plant import Plant


class Peashooter(Plant, Peashooter_Gui):
    def __init__(self, screen, grid, pos, framerate = 60):
        super().__init__(screen, grid, pos)
        self.__health = 300
        self.__attack_damage = 20
        self.__ticks_before_attack = 1500
        self.__sun_cost = 100
        self.name = 'peashooter'

        self.__screen = screen
        self.__grid = grid
        self.__pos = pos
        self.__framerate = framerate

        self.__last_shot_time = 0
        self.__ticks_before_attack = 1000  # example value, set as needed
        self.__accumulated_time = 0

        self.__list_peas = []

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
        self.__accumulated_time += delta_time* self.__framerate
        if self.__accumulated_time >= self.__ticks_before_attack / self.__framerate:
            self.__last_shot_time = pygame.time.get_ticks()
            self.__accumulated_time -= self.__ticks_before_attack
            self.__list_peas.append(Pea(self.__screen, self.__grid, self.__pos))
        # current_time = pygame.time.get_ticks()
        # if current_time - self.__last_shot_time >= self.__ticks_before_attack:
        #     self.__last_shot_time = current_time
        #     self.__list_peas.append(Pea(self.__screen, self.__grid,self.__pos))

    def damage(self, value):
        self.__health -= value
    
    def get_attack_damage(self):
        return self.__attack_damage
    
    def get_peas_shoot(self):
        for pea in self.__list_peas:
            if pea.hit_target or pea.is_ready_to_die():
                self.__list_peas.remove(pea)
        return self.__list_peas

    def __repr__(self) -> str:
        return f'Peashooter {self.__pos}'