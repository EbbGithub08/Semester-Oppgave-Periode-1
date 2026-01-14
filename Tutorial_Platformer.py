import pygame
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_height = 1000

tile_size = 200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

sun_img = pygame.image.load('platformer_assets/img/sun.png')
bg_img = pygame.image.load('platformer_assets/img/sky.png')



class World():
    def __init__(self, data):
        self.tile_list = []
        
        dirt_img = pygame.image.load('platformer_assets/img/dirt.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect =img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile =(img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1




world_data = [
[1,1,1,1,1],
[1,0,0,0,1],
[1,0,0,0,1],
[1,0,0,0,1],
[1,1,1,1,1],        
]

run = True
while run == True:

    screen.fill((0, 0, 0))
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()

