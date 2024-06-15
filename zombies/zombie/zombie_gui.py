import pygame
import time

from spritesheet.spritesheet import SpriteSheet

class Zombie_Gui(pygame.sprite.Sprite):
    def __init__(self, screen, grid, pos) -> None:
        self.__spritesheet = SpriteSheet('assets\zombies\zombie\zombie_sheet.png')
        self.__sprite_list = [pygame.transform.scale(sprite, (int(sprite.get_width() * 1.8), int(sprite.get_height() * 1.8))) for sprite in (self.__spritesheet.parse_sprite(f'sprite{i}') for i in range(13, 20))]
        self.__index = 0
        self.__pos = ((grid.get_start_grid_pos()) + (pos[0] * grid.get_cell_size()),-15 + grid.get_cell_size() * pos[1]+1)
        self.rect = pygame.Rect(self.__pos[0],self.__pos[1],40*1.8,60*1.8)

        self.__grid = grid
        self.__screen = screen
        self.__last_update_time = time.time()

    def draw(self):
        current_time = time.time()
        if current_time - self.__last_update_time >= 0.2:
            self.__index = (self.__index + 1) % len(self.__sprite_list)
            self.__last_update_time = current_time
        self.__screen.blit(self.__sprite_list[self.__index], (self.rect.x, self.rect.y))
        #pygame.draw.rect(self.__screen, (255,255,255), self.rect)
