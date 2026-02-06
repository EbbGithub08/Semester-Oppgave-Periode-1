import pygame


class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    def update(
        self,
        game_over,
        world,
        blob_group,
        lava_group,
        exit_group,
        platform_group,
        spike_group,
        game_over_fx,
        jump_fx,
        draw_text,
        font,
        red,
        screen,
        screen_width,
        screen_height,
    ):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            key = pygame.key.get_pressed()
            if (key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]) and self.on_ground:
                jump_fx.play()
                self.vel_y = -18
                self.on_ground = False
            if not (key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]) and self.vel_y < -6:
                self.vel_y = -6
            if key[pygame.K_a] or key[pygame.K_LEFT]:
                self.vel_x -= 1
                self.counter += 1
                self.direction = -1
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                self.vel_x += 1
                self.counter += 1
                self.direction = 1
            if not (key[pygame.K_a] or key[pygame.K_LEFT]) and not (key[pygame.K_d] or key[pygame.K_RIGHT]):
                if self.vel_x > 0:
                    self.vel_x -= 2
                    if self.vel_x < 0:
                        self.vel_x = 0
                elif self.vel_x < 0:
                    self.vel_x += 2
                    if self.vel_x > 0:
                        self.vel_x = 0

            if self.vel_x > 5:
                self.vel_x = 5
            if self.vel_x < -5:
                self.vel_x = -5

            dx += int(self.vel_x)

            self.on_ground = False

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.vel_y += 1
            if self.vel_y > 11:
                self.vel_y = 11
            dy += self.vel_y

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y > 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.on_ground = True

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top

                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        dy = 0
                        self.on_ground = True
                        if platform.move_x != 0:
                            self.rect.x += platform.move_direction

            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('You Died!!!', font, red, (screen_width // 2) - 140, screen_height // 2)
            self.rect.y -= 10

        self.draw_rect.center = self.rect.center
        screen.blit(self.image, self.draw_rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (32, 64))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.draw_rect = self.image.get_rect()
        self.draw_rect.topleft = (x, y)
        self.width = self.image.get_width() // 2
        self.height = self.image.get_height()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.draw_rect.center
        self.vel_y = 0
        self.vel_x = 0
        self.direction = 0
        self.on_ground = False

