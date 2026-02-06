import pygame

from Classes.others import Enemy, Platform, Lava, Coin, Exit, Spike


class World:
    def __init__(
        self,
        data,
        tile_size,
        spike_sheet,
        spike_width,
        spike_height,
        blob_group,
        platform_group,
        lava_group,
        coin_group,
        exit_group,
        spike_group,
    ):
        self.tile_list = []
        dirt_img = pygame.image.load("img/dirt.png")
        grass_img = pygame.image.load("img/grass.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_data = (img, img_rect)
                    self.tile_list.append(tile_data)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile_data = (img, img_rect)
                    self.tile_list.append(tile_data)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 8, tile_size)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(
                        col_count * tile_size,
                        row_count * tile_size,
                        1,
                        0,
                        tile_size,
                    )
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(
                        col_count * tile_size,
                        row_count * tile_size,
                        0,
                        1,
                        tile_size,
                    )
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(
                        col_count * tile_size,
                        row_count * tile_size + (tile_size // 2),
                        tile_size,
                    )
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(
                        col_count * tile_size + (tile_size // 2),
                        row_count * tile_size + (tile_size // 2),
                        tile_size,
                    )
                    coin_group.add(coin)
                if tile == 8:
                    exit_obj = Exit(
                        col_count * tile_size,
                        row_count * tile_size - 19,
                        tile_size,
                    )
                    exit_group.add(exit_obj)

                if tile == 9:
                    spike = Spike(
                        col_count * tile_size,
                        row_count * tile_size,
                        0,
                        tile_size,
                        spike_sheet,
                        spike_width,
                        spike_height,
                    )
                    spike_group.add(spike)
                if tile == 10:
                    spike = Spike(
                        col_count * tile_size,
                        row_count * tile_size,
                        1,
                        tile_size,
                        spike_sheet,
                        spike_width,
                        spike_height,
                    )
                    spike_group.add(spike)
                if tile == 11:
                    spike = Spike(
                        col_count * tile_size,
                        row_count * tile_size,
                        2,
                        tile_size,
                        spike_sheet,
                        spike_width,
                        spike_height,
                    )
                    spike_group.add(spike)
                if tile == 12:
                    spike = Spike(
                        col_count * tile_size,
                        row_count * tile_size,
                        3,
                        tile_size,
                        spike_sheet,
                        spike_width,
                        spike_height,
                    )
                    spike_group.add(spike)

                col_count += 1
            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

