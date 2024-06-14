from enum import Enum

from plants.peashooter.peashooter import Peashooter
from plants.sunflower.sunflower import Sunflower

class AgentAction(Enum):
    UP=0
    DOWN=1
    LEFT=2
    RIGHT=3
    PLACE_PEASHOOTER= 4
    PLACE_SUNFLOWER= 5
    
class Agent:
    def __init__(self, screen, grid):
        self.__grid = grid
        self.__screen = screen
        self.__suns = 10000
        self.__pos = (0,0)
        self.__plants_owned = []
        self.__plants = {0 : Peashooter(screen=screen, grid=grid, pos=self.get_pos()), 1 : Sunflower(screen=screen, grid=grid, pos=self.get_pos())}
        
    def perform_action(self, action:AgentAction) -> bool:

        self.last_action = action
        
        if action == AgentAction.UP:
            self.move_up()
        elif action == AgentAction.DOWN:
            self.move_down()
        elif action == AgentAction.LEFT:
            self.move_left()
        elif action == AgentAction.RIGHT:
            self.move_right()
        elif action == AgentAction.PLACE_PEASHOOTER:
            self.place_plant(0)
        elif action == AgentAction.PLACE_SUNFLOWER:
            self.place_plant(1)

    def get_suns(self):
        return self.__suns
    
    def get_plants_owned(self):
        return self.__plants_owned
    
    def get_pos(self):
        return self.__pos
    
    def place_plant(self, key):
        if self.__suns >= self.__plants[key].get_sun_cost() and not self.__grid.is_planted((self.__pos[0],self.__pos[1])):
            plant = self.__create_plant(key)
            self.__grid.set_on_grid(self.__pos, plant)
            self.__plants_owned.append(plant)
            self.__suns -= plant.get_sun_cost()

    def move_left(self):
        if self.__pos[0] > 0:
            self.__pos = list(self.__pos)
            self.__pos[0] -= 1
            self.__pos = tuple(self.__pos)

    def move_right(self):
        if self.__pos[0] < 8:
            self.__pos = list(self.__pos)
            self.__pos[0] += 1
            self.__pos = tuple(self.__pos)

    def move_up(self):   
        if self.__pos[1] > 0:     
            self.__pos = list(self.__pos)
            self.__pos[1] -= 1
            self.__pos = tuple(self.__pos)

    def move_down(self):
        if self.__pos[1] < 4:
            self.__pos = list(self.__pos)
            self.__pos[1] += 1
            self.__pos = tuple(self.__pos)

    def __create_plant(self, key):
        if key == 0:
            return Peashooter(screen=self.__screen, grid=self.__grid, pos=self.get_pos())
        elif key == 1:
            return Sunflower(screen=self.__screen, grid=self.__grid, pos=self.get_pos())
            
