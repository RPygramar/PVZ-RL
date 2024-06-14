import pygame

from spritesheet import SpriteSheet

################################# LOAD UP A BASIC WINDOW #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
###########################################################################################

my_spritesheet = SpriteSheet('assets\suns\suns_sheet.png')
trainer = [pygame.transform.scale2x(my_spritesheet.parse_sprite(f'sprite{i}')) for i in range(1,3)]

index = 0

while running:
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############### UPDATE SPRITE IF SPACE IS PRESSED #################################
            if event.key == pygame.K_SPACE:
                index = (index + 1) % len(trainer)


    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((255,255,255))
    canvas.blit(trainer[index], (0, DISPLAY_H - 128))
    window.blit(canvas, (0,0))
    pygame.display.update()








