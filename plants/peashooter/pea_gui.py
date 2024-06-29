import pygame
import time

from spritesheet.spritesheet import SpriteSheet

class Pea_Gui(pygame.sprite.Sprite):
    def __init__(self, screen, grid, pos) -> None:
        self.__spritesheet = SpriteSheet('assets\plants\peashooter\peashooter_sheet.png')
        self.__sprite_list = [pygame.transform.scale2x(self.__spritesheet.parse_sprite(f'sprite{i}')) for i in range(13,15+1)]
        self.__index = 0

        self.rect = self.__sprite_list[0].get_rect()

        self.hit_target = False

        self._ready_to_die = False

        self.__grid = grid
        self.__screen = screen
        self.__pos_in_grid = pos
        self.__pos = ((grid.get_start_grid_pos()) + (pos[0] * grid.get_cell_size()),grid.get_cell_size() + grid.get_cell_size() * pos[1]+1)

        self.__last_update_time = time.time()

        self.rect = pygame.Rect(self.__pos[0],self.__pos[1],self.rect.width,self.rect.height)

    def draw(self):
        if self.hit_target:
            self._ready_to_die = True
        self.__screen.blit(self.__sprite_list[self.__index], (self.rect.x, self.rect.y))
    

