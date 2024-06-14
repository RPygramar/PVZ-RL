import pygame

class Grid_Gui(pygame.sprite.Sprite):
    def __init__(self, screen, cell_size) -> None:
        self.__image = 'assets/frontyard/frontyard.png'
        self.image = pygame.image.load(self.__image).convert_alpha()
        self.image_rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

        self.__cell_size = cell_size
        self.__screen = screen
        self.rect = pygame.Rect(self.__cell_size*2, self.__cell_size, self.__cell_size*9, self.__cell_size*5)
        self.__color = (255, 0, 0)

    def draw(self):
        pygame.draw.rect(self.__screen, self.__color, self.rect, self.rect.width)
