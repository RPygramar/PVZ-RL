import pygame

from zombies.zombie.zombie_gui import Zombie_Gui

class Zombie(Zombie_Gui):
    def __init__(self, screen, grid, pos):
        super().__init__(screen, grid, pos)
        self.__health = 181
        self.__attack_damage = 100
        self.__ticks_before_attack = 2000

        self.__last_update_time = pygame.time.get_ticks()

        self.__last_eat_time = pygame.time.get_ticks()
        
        self.__pos = (9, pos[1])
        self.__grid = grid
        self.__screen = screen

        self.__eating = False

    def get_health(self):
        return self.__health
    
    def get_attack_damage(self):
        return self.__attack_damage
    
    def get_ticks_before_attack(self):
        return self.__ticks_before_attack
    
    def get_pos(self):
        return self.__pos
    
    def update(self):
        self.__walk()

    def damage(self, value):
        self.__health -= value

    def __walk(self):
        if not self.__eating:
            current_time = pygame.time.get_ticks()
            # print(current_time)
            # print(current_time - self.__last_update_time)
            if current_time - self.__last_update_time >= 200:
                self.rect.x -= 4
                self.__last_update_time = current_time

    def eat_plant(self, plant:object):
        self.__eating = True
        current_time = pygame.time.get_ticks()
        if current_time - self.__last_eat_time >= 2000:
            plant.damage(self.__attack_damage)
            self.__last_eat_time = current_time
                
    
    def set_eating(self, boolean : bool):
        self.__eating = boolean
    
    def __repr__(self) -> str:
        return f'Zombie {self.rect}'