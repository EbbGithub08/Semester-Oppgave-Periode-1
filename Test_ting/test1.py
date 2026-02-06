import pygame, sys

pygame.init()

screen_width = 1600
screen_height = 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My First Pygame")

fotballmann = pygame.image.load("img/fotbalman.png").convert_alpha()
fotballmann = pygame.transform.scale(fotballmann,
                                     (fotballmann.get_width() // 2,
                                      fotballmann.get_height() // 2))
                                      

clock = pygame.time.Clock()

x = screen_width
y = (screen_height - fotballmann.get_height()) // 2

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(fotballmann, (x, y))
    x -= 80
    if x < -fotballmann.get_width():
        x = screen_width

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
