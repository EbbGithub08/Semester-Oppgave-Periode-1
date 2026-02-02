import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import sqlite3
import time

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
clock = pygame.time.Clock()
fps = 60


screen_width = 800
screen_height = 800

timer_running = False
start_time = 0
elapsed_time = 0
tile_size = 40
game_over = 0
main_menu = True
game_over_time = 0
level = 1
start_level = level
max_levels = 10
score = 0
death_counter = 0
selected_world = 0
world_select = False
SPIKE_WIDTH = 16
SPIKE_HEIGHT = 16

font_score = pygame.font.SysFont('Bauhaus 93', 30)
font = pygame.font.SysFont('Bauhaus 93', 90)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
restart_img = pygame.image.load('img/restart_btn.png')
back_img = pygame.transform.scale(pygame.image.load('img/back.png'), (50, 50))
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
world1_img = pygame.transform.scale(pygame.image.load('img/world1.png'), (200, 300))
world2_img = pygame.transform.scale(pygame.image.load('img/world2.png'), (200, 300))
world3_img = pygame.transform.scale(pygame.image.load('img/world3.png'), (200, 300))
tutorial_img = pygame.transform.scale(pygame.image.load('img/tutorial.png'), (300, 200))
spike_sheet = pygame.image.load("img/spike.png").convert_alpha()
death_skull = pygame.image.load('img/skull.png')

pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.2) 
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.2) 
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.2) 


def init_db():
    conn = sqlite3.connect('platformer_scores.db')
    c = conn.cursor()

    try:
        c.execute("SELECT time_seconds FROM highscores LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("DROP TABLE IF EXISTS highscores")
        print("Gammel database oppdaget. Oppdaterer tabell...")

    c.execute('''CREATE TABLE IF NOT EXISTS highscores
                 (username TEXT, world INTEGER, time_seconds REAL)''')
    c.execute("DELETE FROM highscores WHERE username = 'TEST'")
    conn.commit()
    conn.close()

def save_highscore(username, world, time_seconds):
    username = ''.join(char for char in username if char.isalpha()).upper()
    if not username:
        return
    conn = sqlite3.connect('platformer_scores.db')
    c = conn.cursor()
    
    c.execute("SELECT time_seconds FROM highscores WHERE username = ? AND world = ?", (username, world))
    row = c.fetchone()

    if row is None:
        c.execute("INSERT INTO highscores VALUES (?, ?, ?)", (username, world, time_seconds))
        print(f"Saved New Highscore -> Name: {username}, World: {world}, Time: {time_seconds:.2f} Sec")
    elif time_seconds < row[0]:
        c.execute("UPDATE highscores SET time_seconds = ? WHERE username = ? AND world = ?", (time_seconds, username, world))
        print(f"Updated Highscore -> Name: {username}, World: {world}, Time: {time_seconds:.2f} Sec")
    else:
        print(f"Time not fast enough -> Name: {username}, World: {world}, Time: {time_seconds:.2f} Sec (Best: {row[0]:.2f})")

    conn.commit()
    conn.close()

def debug_print_scores():
    conn = sqlite3.connect('platformer_scores.db')
    c = conn.cursor()
    
    print("\n====== LEADERBOARDS ======")
    for w in range(1, 5):
        c.execute("SELECT * FROM highscores WHERE world = ? ORDER BY time_seconds ASC", (w,))
        rows = c.fetchall()
        world_name = "TUTORIAL" if w == 4 else f"WORLD {w}"
        print(f"\n--- {world_name} ---")
        if not rows:
            print("No scores yet.")
        else:
            for rank, row in enumerate(rows, 1):
                print(f"{rank}. {row[0]} - {row[2]:.2f}s")
    print("\n==========================")
    conn.close()

def reset_scores():
    conn = sqlite3.connect('platformer_scores.db')
    c = conn.cursor()
    c.execute("DELETE FROM highscores")
    conn.commit()
    conn.close()
    print("Database cleared!")

def get_top_scores():
    conn = sqlite3.connect('platformer_scores.db')
    c = conn.cursor()
    scores = {}
    for w in range(1, 5):
        c.execute("SELECT * FROM highscores WHERE world = ? ORDER BY time_seconds ASC LIMIT 3", (w,))
        rows = c.fetchall()
        scores[w] = rows
    conn.close()
    return scores

init_db()
debug_print_scores()
leaderboard_data = get_top_scores()



def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

def draw_text(text, font, text_col, x, y):
    img = font.render(str(text), True, text_col)
    screen.blit(img, (x, y))

def format_time(seconds):
    return time.strftime("%M:%S", time.gmtime(seconds)) + f".{int((seconds % 1) * 100):02}"

def reset_level(level):
    x = 80
    y = screen_height - 110

    if selected_world == 2:
        if level == 1:
            x = screen_width // 2
            y = 700
        elif level == 2:
            x = screen_width - 560
            y = 700
        elif level == 3:
            x = 80
            y = 700
    elif selected_world == 3:
        if level == 2:
            x = screen_width // 2
        if level == 3:
            x = 100
            y = 100
            
    player.reset(x, y)

    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    platform_group.empty()
    coin_group.empty()
    spike_group.empty()
    coin_group.add(score_coin)

    file_path = f'World_Data/World{selected_world}/level{level}_data'

    if path.exists(file_path):
        pickle_in = open(file_path, 'rb')
        world_data = pickle.load(pickle_in)
    else:
        world_data = []
        for row in range(20):
            r = [0] * 20
            world_data.append(r)
        for row in range(20):
            for col in range(20):
                if row == 0 or row == 19 or col == 0 or col == 19:
                    world_data[row][col] = 1

    world = World(world_data)
    return world



class Button():
    last_click_time = 0
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                if pygame.time.get_ticks() - Button.last_click_time > 500:
                    action = True
                    self.clicked = True
                    Button.last_click_time = pygame.time.get_ticks()
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action



class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
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
                        self.rect.bottom = platform.rect.top -1
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
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

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

        

class World():
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

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
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect =img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile =(img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 8)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (19))
                    exit_group.add(exit)

                if tile == 9:
                    spike = Spike(col_count * tile_size, row_count * tile_size, 0)
                    spike_group.add(spike)
                if tile == 10:
                    spike = Spike(col_count * tile_size, row_count * tile_size, 1)
                    spike_group.add(spike)
                if tile == 11:
                    spike = Spike(col_count * tile_size, row_count * tile_size, 2)
                    spike_group.add(spike)
                if tile == 12:
                    spike = Spike(col_count * tile_size, row_count * tile_size, 3)
                    spike_group.add(spike)

                col_count += 1
            row_count += 1 

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen,(255, 0, 0), tile[1], 2)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
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
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_sprite(spike_sheet, type * SPIKE_WIDTH, 0, SPIKE_WIDTH, SPIKE_HEIGHT)
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.inflate_ip(-(tile_size // 2), -(tile_size // 2))



player = Player(80, screen_height - 110)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()

score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

world = reset_level(level)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2 + 100, start_img)
exit_button = Button(screen_width // 2 + 100, screen_height // 2 + 100, exit_img)
world1_button = Button(50, screen_height // 2 - 150, world1_img)
back_button_select = Button(10, -2, back_img)
back_button_game = Button(80, -2, back_img)
world2_button = Button(300, screen_height // 2 - 150, world2_img)
world3_button = Button(550, screen_height // 2 - 150, world3_img)
tutorial_button = Button(screen_width // 2 - 159, 550, tutorial_img)
death_img = pygame.transform.scale(death_skull, (tile_size, tile_size))
user_text = ''



run = True
while run == True:
    clock.tick(fps)

    screen.fill((0, 0, 0))
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu == True:
        if start_button.draw():
            main_menu = False
            world_select = True
            world1_button.clicked = True
            world2_button.clicked = True
            world3_button.clicked = True
        if exit_button.draw():
            run = False
        
        lb_x = screen_width - 250
        lb_y = 20
        draw_text('TOP SCORES', font_score, blue, lb_x, lb_y)
        lb_y += 30
        
        for w in range(1, 5):
            world_name = "TUTORIAL" if w == 4 else f"WORLD {w}"
            draw_text(world_name, font_score, blue, lb_x, lb_y)
            lb_y += 25
            if not leaderboard_data[w]:
                draw_text("No scores", font_score, blue, lb_x, lb_y)
                lb_y += 25
            else:
                for rank, row in enumerate(leaderboard_data[w], 1):
                    draw_text(f"{rank}. {row[0]} - {row[2]:.2f}s", font_score, blue, lb_x, lb_y)
                    lb_y += 25
            lb_y += 10

    elif world_select == True:
        draw_text('Select World', font, yellow, (screen_width // 2) - 200, screen_height // 2 - 250)
        if back_button_select.draw():
            world_select = False
            main_menu = True
            leaderboard_data = get_top_scores()
        if world1_button.draw():
            selected_world = 1
            world_select = False
            timer_running = True
            start_time = time.time()
            level = start_level
            game_over = 0
            score = 0
            death_counter = 0
            world = reset_level(level)
        if world2_button.draw():
            selected_world = 2
            world_select = False
            timer_running = True
            start_time = time.time()
            level = start_level
            game_over = 0
            score = 0
            death_counter = 0
            world = reset_level(level)
        if world3_button.draw():
            selected_world = 3
            world_select = False
            timer_running = True
            start_time = time.time()
            level = start_level
            game_over = 0
            score = 0
            death_counter = 0
            world = reset_level(level)
        if tutorial_button.draw():
            selected_world = 4
            world_select = False
            timer_running = True
            start_time = time.time()
            level = start_level
            game_over = 0
            score = 0
            death_counter = 0
            world = reset_level(level)

    else:
        world.draw()
        if game_over == 0:
            if timer_running:
                elapsed_time = time.time() - start_time
            blob_group.update()
            platform_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()

            if back_button_game.draw():
                world_select = True
                timer_running = False
                game_over = 0
                score = 0
                death_counter = 0

        draw_text('X ' + str(score), font_score, white, tile_size - 3, 12)
        time_text = format_time(elapsed_time)
        draw_text(time_text, font_score, white, screen_width - 220, 12)
        draw_text(death_counter, font_score, red, screen_width - 50, 12)
        screen.blit(death_img, (screen_width - 90, 0))

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        for spike in spike_group:
            screen.blit(spike.image, (spike.rect.x - 10, spike.rect.y - 10))
        coin_group.draw(screen)

        if game_over == 0:
            game_over = player.update(game_over)
            if game_over == -1:
                game_over_time = pygame.time.get_ticks()
        else:
            game_over = player.update(game_over)

        if game_over == -1: 
            key = pygame.key.get_pressed()
            if restart_button.draw() or (key[pygame.K_SPACE] and pygame.time.get_ticks() - game_over_time > 400):
                world = reset_level(level)
                if level == 1:
                    start_time = time.time()
                    timer_running = True
                death_counter += 1
                game_over = 0
                score = 0

        if game_over == 1:
            level += 1
            next_level_path = f'World_Data/World{selected_world}/level{level}_data'

            if path.exists(next_level_path):
                world = reset_level(level)
                game_over = 0
            else:
                game_over = 2
                game_over_time = pygame.time.get_ticks()
        
        if game_over == 2:
            timer_running = False
            draw_text('You win!', font, blue, (screen_width // 2) - 115, screen_height // 2 - 100)
            draw_text('Enter Name: ' + user_text, font_score, white, (screen_width // 2) - 150, screen_height // 2)
            draw_text('Press ENTER to save', font_score, white, (screen_width // 2) - 150, screen_height // 2 + 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if world_select:
                    world_select = False
                    main_menu = True
                    leaderboard_data = get_top_scores()
                elif main_menu:
                    run = False
                else:  # In-game (playing, dead, or won)
                    world_select = True
                    timer_running = False
                    game_over = 0
                    score = 0
                    death_counter = 0
                    user_text = ''
            if event.key == pygame.K_r:
                    level = 1
                    world = reset_level(level)
                    game_over = 0
                    score = 0
                    death_counter = 0
                    start_time = time.time()
                    timer_running = True
                    user_text = ''
                


        if game_over == 2 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                if len(user_text) > 0:
                    save_highscore(user_text, selected_world, elapsed_time)
                    level = 1
                    world = reset_level(level)
                    game_over = 0
                    score = 0
                    death_counter = 0
                    start_time = time.time()
                    timer_running = True
                    user_text = ''
            else:
                if len(user_text) < 15:
                    user_text += event.unicode

    pygame.display.update()


pygame.quit()
