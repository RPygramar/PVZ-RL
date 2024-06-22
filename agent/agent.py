from enum import Enum

from plants.peashooter.peashooter import Peashooter
from plants.sunflower.sunflower import Sunflower

class AgentAction(Enum):
    UP=1
    DOWN=3
    LEFT=2
    RIGHT=0
    PLACE_PEASHOOTER= 4
    PLACE_SUNFLOWER= 5
    COLLECT_SUN = 6
    
class Agent:
    def __init__(self, screen, grid):
        self.__grid = grid
        self.__screen = screen
        self.__suns = 2000
        self.__pos = (0,0)
        self.__plants_owned = []
        self.__plants = {0 : Peashooter(screen=screen, grid=grid, pos=self.get_pos()), 1 : Sunflower(screen=screen, grid=grid, pos=self.get_pos())}

        self.existing_suns = []

        self.__zombies_killed = []
        
    def perform_action(self, action:AgentAction) -> bool:

        self.last_action = action
        
        if action == AgentAction.UP:
            self.move_up()
            return 0
        elif action == AgentAction.DOWN:
            self.move_down()
            return 1
        elif action == AgentAction.LEFT:
            self.move_left()
            return 2
        elif action == AgentAction.RIGHT:
            self.move_right()
            return 3
        elif action == AgentAction.PLACE_PEASHOOTER:
            self.place_plant(0)
            return 4
        elif action == AgentAction.PLACE_SUNFLOWER:
            self.place_plant(1)
            return 5
        elif action == AgentAction.COLLECT_SUN:
            self.__collect_suns(suns=self.existing_suns)
            return 6
            
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

    def plants_behavior(self, zombies : list):
        for plant in self.__plants_owned:
            if plant.name == 'peashooter':
                if plant.line_of_shoot.collidelist(zombies) >= 0:
                    plant.shoot()
                for pea in plant.get_peas_shoot():
                    if pea.rect.collidelist(zombies) >= 0:
                        zombies[pea.rect.collidelist(zombies)].damage(pea.get_attack_damage())
                        pea.hitted_target()
            if plant.name == 'sunflower':
                plant.produce_suns()
                    
    def get_all_elements(self):
        list_elements = []
        for plant in self.__plants_owned:
            if plant.name == 'peashooter':
                list_elements = list_elements + plant.get_peas_shoot()

            if plant.name == 'sunflower':
                existing_suns_set = set(self.existing_suns)
                new_suns = plant.get_list_suns()
                for sun in new_suns:
                    if sun not in existing_suns_set:
                        self.existing_suns.append(sun)
                        existing_suns_set.add(sun)
                        plant.remove_sun(sun)
        return list_elements

    def remove_owned_plant(self, plant : object):
        self.__plants_owned.remove(plant)

    def __create_plant(self, key):
        if key == 0:
            return Peashooter(screen=self.__screen, grid=self.__grid, pos=self.get_pos())
        elif key == 1:
            return Sunflower(screen=self.__screen, grid=self.__grid, pos=self.get_pos())
            
    def __collect_suns(self, suns : list):
        if suns:
            for sun in suns:
                if self.__suns < 2000:
                    self.__suns += sun.get_value()
                self.existing_suns.remove(sun)

    def remove_dead_plants(self):
        dead_plants = [plant for plant in self.__plants_owned if plant.get_health() <= 0]
        for dead_plant in dead_plants:
            self.__plants_owned.remove(dead_plant)
            self.__grid.remove_from_grid(dead_plant.get_pos())

    def get_zombies_killed(self) -> list:
        return self.__zombies_killed
    
    def add_zombies_killed(self, zombie: object):
        self.__zombies_killed.append(zombie)