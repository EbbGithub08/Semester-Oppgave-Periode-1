import pygame


class Button:

    last_click_time = 0

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.mask = pygame.mask.from_surface(self.image)

        hover_width = int(self.rect.width * 1.05)
        hover_height = int(self.rect.height * 1.05)
        self.hover_image = pygame.transform.scale(
            self.image, (hover_width, hover_height)
        )

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and self.mask.get_at(
            (pos[0] - self.rect.x, pos[1] - self.rect.y)
        ):
            hover_rect = self.hover_image.get_rect()
            hover_rect.center = self.rect.center
            screen.blit(self.hover_image, hover_rect)

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                if pygame.time.get_ticks() - Button.last_click_time > 500:
                    action = True
                    self.clicked = True
                    Button.last_click_time = pygame.time.get_ticks()
        else:
            screen.blit(self.image, self.rect)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
