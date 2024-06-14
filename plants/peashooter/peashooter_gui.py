import pygame
import time

from spritesheet.spritesheet import SpriteSheet

class Peashooter_Gui(pygame.sprite.Sprite):
    def __init__(self, screen, grid, pos) -> None:
        self.__spritesheet = SpriteSheet('assets\plants\peashooter\peashooter_sheet.png')
        self.__sprite_list = [pygame.transform.scale2x(self.__spritesheet.parse_sprite(f'sprite{i}')) for i in range(1,8+1)]
        self.__index = 0
        self.rect = self.__sprite_list[0].get_rect()

        self.__grid = grid
        self.__screen = screen
        self.__pixel_pos = ((grid.get_start_grid_pos()) + (pos[0] * grid.get_cell_size()),grid.get_cell_size() + grid.get_cell_size() * pos[1]+1)
        self.__pos = ((grid.get_start_grid_pos()) + (pos[0] * grid.get_cell_size()),grid.get_cell_size() + grid.get_cell_size() * pos[1]+1)
        self.__last_update_time = time.time()

    def draw(self):
        current_time = time.time()
        if current_time - self.__last_update_time >= 0.1:
            self.__index = (self.__index + 1) % len(self.__sprite_list)
            self.__last_update_time = current_time
        self.__screen.blit(self.__sprite_list[self.__index], (self.__pos[0], self.__pos[1]))
