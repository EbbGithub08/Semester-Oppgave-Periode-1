import pygame


def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/blob.png")

        self.draw_rect = self.image.get_rect()
        self.draw_rect.topleft = (x, y)

        self.rect = pygame.Rect(0, 0, self.draw_rect.width * 0.7, self.draw_rect.height * 0.6)
        self.rect.midbottom = self.draw_rect.midbottom

        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1
        
        self.draw_rect.midbottom = self.rect.midbottom

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/platform.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/lava.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/coin.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/exit.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, spike_type, tile_size, spike_sheet, spike_width, spike_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_sprite(
            spike_sheet,
            spike_type * spike_width,
            0,
            spike_width,
            spike_height,
        )
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.inflate_ip(-(tile_size // 2), -(tile_size // 2))
