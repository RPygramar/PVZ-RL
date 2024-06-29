import pygame

from zombies.zombie_normal.zombie_normal_gui import Zombie_Normal_Gui
from zombies.zombie import Zombie

class Zombie_Normal(Zombie,Zombie_Normal_Gui):
    def __init__(self, screen, grid, pos, framerate=60):
        super().__init__(screen, grid, pos)
        self.__health = 99
        self.__attack_damage = 100
        self.__ticks_before_attack = 2000

        #self.__last_update_time = pygame.time.get_ticks()

        self.__last_eat_time = 2000
        self.__accumulated_time = 0
        
        self.__pos = (9, pos[1])
        self.__grid = grid
        self.__screen = screen
        self.__framerate = framerate

        self.__eating = False

        self.__difficulty = 0 # 0 easy / 1 medium / 2 hard
    
    def get_screen(self):
        return self.__screen
    
    def get_grid(self):
        return self.__grid
    
    def get_pos(self):
        return self.__pos
    
    def get_difficulty(self):
        return self.__difficulty

    def get_health(self):
        return self.__health
    
    def walk(self, delta_time):
        if not self.__eating:
            move_distance = (delta_time / 50) * self.__framerate  # Move 60 pixels every 50 milliseconds
            self.rect.x -= move_distance

    def eat_plant(self, plant:object, delta_time):
        self.__eating = True
        self.__accumulated_time += delta_time* self.__framerate
        if self.__accumulated_time >= self.__last_eat_time / self.__framerate:
            plant.damage(self.__attack_damage)

    def set_eating(self, boolean : bool):
        self.__eating = boolean

    def damage(self, value):
        self.__health -= value

    def get_attack_damage(self):
        return self.__attack_damage
    
    def update(self, delta_time):
        self.walk(delta_time)
    
    def __repr__(self) -> str:
        return f'Zombie {self.rect}'