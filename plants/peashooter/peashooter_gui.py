import pygame
import time

from spritesheet.spritesheet import SpriteSheet

class Peashooter_Gui(pygame.sprite.Sprite):
    def __init__(self, screen, grid, pos) -> None:
        self.__spritesheet = SpriteSheet('assets\plants\peashooter\peashooter_sheet.png')
        self.__sprite_list_idle = [pygame.transform.scale2x(self.__spritesheet.parse_sprite(f'sprite{i}')) for i in range(1,8+1)]
        self.__sprite_list_shoot = [pygame.transform.scale2x(self.__spritesheet.parse_sprite(f'sprite{i}')) for i in range(10,12+1)]
        self.__index_idle = 0

        self.rect = self.__sprite_list_idle[0].get_rect()

        self.__grid = grid
        self.__screen = screen
        self.__pos_in_grid = pos
        self.__pos = ((grid.get_start_grid_pos()) + (pos[0] * grid.get_cell_size()),grid.get_cell_size() + grid.get_cell_size() * pos[1]+1)
        self.__last_update_time = time.time()

        self.rect = pygame.Rect(self.__pos[0],self.__pos[1],self.rect.width,self.rect.height)

        self.line_of_shoot = pygame.Rect(self.__pos[0], self.rect.centery, grid.get_final_pos_grid(pos), 1)

    def draw(self):
        current_time = time.time()
        if current_time - self.__last_update_time >= 0.1:
            self.__index_idle = (self.__index_idle + 1) % len(self.__sprite_list_idle)
            self.__last_update_time = current_time
        self.__screen.blit(self.__sprite_list_idle[self.__index_idle], (self.__pos[0], self.__pos[1]))
        # pygame.draw.line(self.__screen, (255, 255, 255), (self.__pos[0],self.__pos[1]+25), (self.__grid.get_final_pos_grid(),self.__pos[1]+25), 1)
        pygame.draw.rect(self.__screen, (255,255,255), self.line_of_shoot)

