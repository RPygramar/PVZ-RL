from abc import ABC, abstractmethod

class Zombie(ABC):

    @abstractmethod
    def get_screen(self):
        pass
    
    @abstractmethod
    def get_grid(self):
        pass
    
    @abstractmethod
    def get_pos(self):
        pass
    
    @abstractmethod
    def get_health(self):
        pass

    @abstractmethod
    def walk(self):
        pass

    @abstractmethod
    def eat_plant(self):
        pass

    def set_eating(self):
        pass

    @abstractmethod
    def damage(self):
        pass
        