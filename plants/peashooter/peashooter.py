from plants.peashooter.peashooter_gui import Peashooter_Gui

class Peashooter(Peashooter_Gui):
    def __init__(self, screen, grid, pos):
        super().__init__(screen, grid, pos)
        self.__health = 300
        self.__attack_damage = 20
        self.__ticks_before_attack = 1.4
        self.__sun_cost = 100

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
        return f'Peashooter {self.__pos}'