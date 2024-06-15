import time

from zombies.zombie.zombie_gui import Zombie_Gui

class Zombie(Zombie_Gui):
    def __init__(self, screen, grid, pos):
        super().__init__(screen, grid, pos)
        self.__health = 181
        self.__attack_damage = 100
        self.__ticks_before_attack = 4.7

        self.__last_update_time = time.time()
        
        self.__pos = pos

    def get_health(self):
        return self.__health
    
    def get_attack_damage(self):
        return self.__attack_damage
    
    def get_ticks_before_attack(self):
        return self.__ticks_before_attack
    
    def update(self):
        self.__walk()

    def damage(self, value):
        self.__health -= value

    def __walk(self):
        current_time = time.time()
        if current_time - self.__last_update_time >= 0.2:
            self.rect.x -= 3
            self.__last_update_time = current_time
    
    def __repr__(self) -> str:
        return f'Zombie {self.rect}'