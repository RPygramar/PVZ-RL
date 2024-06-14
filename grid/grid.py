import pygame
from grid.grid_gui import Grid_Gui

class Grid(Grid_Gui):
    def __init__(self, screen, cell_size = 80):
        super().__init__(screen= screen, cell_size=cell_size)
        self.__cell_size = cell_size
        self.__start_grid_pos = self.__cell_size*2
        self.__grid = [[None for _ in range(5)] for _ in range(9)]

    def get_cell_size(self):
        return self.__cell_size
    
    def get_start_grid_pos(self):
        return self.__start_grid_pos
    
    def get_grid(self):
        return self.__grid
    
    def set_on_grid(self, position, objeto):
        if not self.__grid[position[0]][position[1]]:
            self.__grid[position[0]][position[1]] = objeto

    def is_planted(self, position):
        return self.__grid[position[0]][position[1]]

    def __str__(self):
        grid = self.get_grid()
        return '\n'.join([' '.join(map(str, row)) for row in grid])
    
if __name__ == '__main__':
    grid_instance = Grid()
    print(grid_instance._Grid__grid)