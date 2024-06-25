from abc import ABC, abstractmethod

class Plant(ABC):

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
    def get_sun_cost(self):
        pass

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def damage(self):
        pass
        