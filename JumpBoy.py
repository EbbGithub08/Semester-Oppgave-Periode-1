import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import time

from Classes import Player, Button, HighscoreDatabase, World, Coin, Slider

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
score = 0
score_at_level_start = 0
death_counter = 0
selected_world = 0
world_select = False
SPIKE_WIDTH = 16
SPIKE_HEIGHT = 16

font_score = pygame.font.SysFont('Bauhaus 93', 30)
font = pygame.font.SysFont('Bauhaus 93', 90)
font_leaderboard_entry = pygame.font.SysFont('Bauhaus 93', 24)
white = (255, 255, 255)
gray = (128, 128, 128)
black = (0, 0, 0)
green = (0, 100, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
light_blue = (100, 149, 237)
orange = (255, 128, 0)
gold = (255, 215, 0)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
red_sky_img = pygame.image.load('img/red_sky.png')
restart_img = pygame.image.load('img/restart_btn.png')
back_img = pygame.transform.scale(pygame.image.load('img/back.png'), (50, 50))
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
resume_img = pygame.transform.scale(pygame.image.load('img/back.png'), (100, 100))
exit_to_menu_img = pygame.transform.scale(pygame.image.load('img/exit_btn.png'), (150, 60))
world1_img = pygame.transform.scale(pygame.image.load('img/world1.png'), (200, 300))
world2_img = pygame.transform.scale(pygame.image.load('img/world2.png'), (200, 300))
world3_img = pygame.transform.scale(pygame.image.load('img/world3.png'), (200, 300))
world5_img = pygame.transform.scale(pygame.image.load('img/World3_Demon.png'), (200, 300))
demon_btn_img = pygame.transform.scale(pygame.image.load('img/Demon_Button.png'), (200, 100))
tutorial_img = pygame.transform.scale(pygame.image.load('img/tutorial.png'), (300, 200))
spike_sheet = pygame.image.load("img/spike.png").convert_alpha()
death_skull = pygame.image.load('img/skull.png')
leaderboard_img = pygame.transform.scale(pygame.image.load('img/leaderboard.png'), (400, 235))
settings_img = pygame.transform.scale(pygame.image.load('img/settings.png'), (150, 100))
trym_img = pygame.transform.scale(pygame.image.load('img/trym.png'), (230, 200))
speech_img = pygame.transform.scale(pygame.image.load('img/speech.png'), (250, 180))
logo_img = pygame.transform.scale(pygame.image.load('img/logo.png'), (500, 500))

red_overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
red_overlay.fill((255, 0, 0, 70))

pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0,0)

coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.2) 
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.2) 
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.2) 
win_fx = pygame.mixer.Sound('img/win.wav')
win_fx.set_volume(0.2)
plop_fx = pygame.mixer.Sound('img/plop.wav')
plop_fx.set_volume(0.2)


db = HighscoreDatabase("Database/platformer_scores.db")
db.init_db()
db.debug_print_scores()
leaderboard_data = db.get_top_scores()

def draw_text(text, font, text_col, x, y, outline_col=None, outline_thickness=1):
    base_text = str(text)

    if outline_col is None:
        outline_col = black

    text_surface = font.render(base_text, True, text_col)

    if outline_thickness > 0:
        outline_surface = font.render(base_text, True, outline_col)
        for ox in range(-outline_thickness, outline_thickness + 1):
            for oy in range(-outline_thickness, outline_thickness + 1):
                if ox == 0 and oy == 0:
                    continue
                if ox * ox + oy * oy <= outline_thickness * outline_thickness:
                    screen.blit(outline_surface, (x + ox, y + oy))

    screen.blit(text_surface, (x, y))

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
            y = 700
        if level == 3:
            x = 100
            y = 100
    elif selected_world == 5:
        if level == 2:
            x = screen_width // 2
            y = 700
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

    world = World(
        world_data,
        tile_size,
        spike_sheet,
        SPIKE_WIDTH,
        SPIKE_HEIGHT,
        blob_group,
        platform_group,
        lava_group,
        coin_group,
        exit_group,
        spike_group,
    )
    return world

def get_total_coins(world_num):
    total = 0
    lvl = 1
    while True:
        file_path = f'World_Data/World{world_num}/level{lvl}_data'
        if not path.exists(file_path):
            break
        
        pickle_in = open(file_path, 'rb')
        world_data = pickle.load(pickle_in)
        pickle_in.close()
        
        for row in world_data:
            for tile in row:
                if tile == 7:
                    total += 1
        lvl += 1
    return total


player = Player(80, screen_height - 110)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()

score_coin = Coin(tile_size // 2, tile_size // 2, tile_size)

world = reset_level(level)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2 + 100, start_img)
exit_button = Button(screen_width // 2 + 100, screen_height // 2 + 100, exit_img)
world1_button = Button(50, screen_height // 2 - 150, world1_img)
back_button_select = Button(10, -2, back_img)
back_button_game = Button(80, -2, back_img)
world2_button = Button(300, screen_height // 2 - 150, world2_img)
world3_button = Button(550, screen_height // 2 - 150, world3_img)
world5_button = Button(550, screen_height // 2 - 150, world5_img)
tutorial_button = Button(screen_width // 2 - 159, 550, tutorial_img)
demon_toggle_button = Button(screen_width // 2 - 110, screen_height - 125, demon_btn_img)
leaderboard_button = Button(screen_width // 2 - 187, screen_height // 2 + 170, leaderboard_img)
death_img = pygame.transform.scale(death_skull, (tile_size, tile_size))
settings_button = Button(screen_width // 2 - 63, screen_height // 2 + 120, settings_img)
resume_button = Button(250, 480, resume_img)
exit_to_menu_button = Button(400, 500, exit_to_menu_img)
user_text = ''

music_volume = 0.3
sfx_volume = 0.2
music_slider = Slider(300, 340, 200, 20, music_volume)
sfx_slider = Slider(300, 440, 200, 20, sfx_volume)

run = True
leaderboard_active = False
settings_active = False
full_leaderboard_data = {}
demon_mode = False
while run == True:
    clock.tick(fps)

    screen.fill((0, 0, 0))
    if (world_select and demon_mode) or (not main_menu and not world_select and selected_world == 5):
        screen.blit(red_sky_img, (0, 0))
    else:
        screen.blit(bg_img, (0, 0))
        screen.blit(sun_img, (100, 100))

    if leaderboard_active:
        screen.fill((0, 50, 100))
        draw_text('LEADERBOARD', font, light_blue, screen_width // 2 - 250, 50)
        if back_button_select.draw(screen):
            plop_fx.play()
            leaderboard_active = False
            main_menu = True
        
        leaderboard_worlds = {
            1: {"name": "World 1", "pos": (20, 150)},
            2: {"name": "World 2", "pos": (220, 150)},
            3: {"name": "World 3", "pos": (420, 150)},
            4: {"name": "Tutorial", "pos": (620, 150)},
        }

        for w, data in leaderboard_worlds.items():
            x, y_start = data["pos"]
            name = data["name"]
            
            draw_text(name, font_score, white, x, y_start)
            y = y_start + 40
            
            scores = full_leaderboard_data.get(w, [])
            if not scores:
                draw_text("No scores yet", font_leaderboard_entry, gray, x, y)
            else:
                for i, row in enumerate(scores[:15]):
                    is_perfect = len(row) > 4 and row[4] == 1
                    entry_color = gold if is_perfect else white
                    score_text = f"{i+1}. {row[0]} - {row[2]:.2f}s"
                    draw_text(score_text, font_leaderboard_entry, entry_color, x, y)
                    y += 30

    elif settings_active:
        if not main_menu and not world_select:
            world.draw(screen)
            for enemy in blob_group:
                screen.blit(enemy.image, enemy.draw_rect)
            platform_group.draw(screen)
            lava_group.draw(screen)
            exit_group.draw(screen)
            for spike in spike_group:
                screen.blit(spike.image, (spike.rect.x - 10, spike.rect.y - 10))
            coin_group.draw(screen)
            screen.blit(score_coin.image, score_coin.rect)
            
            draw_text('X ' + str(score), font_score, white, tile_size - 3, 12)
            time_text = format_time(elapsed_time)
            draw_text(time_text, font_score, white, screen_width - 220, 12)
            draw_text(death_counter, font_score, red, screen_width - 50, 12)
            screen.blit(death_img, (screen_width - 90, 0))
            screen.blit(player.image, player.rect)

            if selected_world == 4 and game_over != 2:
                screen.blit(trym_img, (screen_width - 200, 90))
                bubble_x = screen_width - 400
                bubble_y = 30
                screen.blit(speech_img, (bubble_x, bubble_y))
                
                lines = []
                if level == 1:
                    lines = ["Move: WASD / Arrows", "Jump: Space / Up", "R: Restart  ESC: Menu"]
                elif level == 2:
                    lines = ["Hold Space / Up to", "jump higher to reach", "higher platforms."]
                elif level == 3:
                    lines = ["Now its time to test", "your skill bitch!", "Huahuahuahuahuaa"]
                
                text_x = bubble_x + 15
                text_y = bubble_y + 32
                line_spacing = 26
                for line in lines:
                    draw_text(line, font_score, black, text_x, text_y, outline_thickness=0)
                    text_y += line_spacing

        pygame.draw.rect(screen, orange, (200, 200, 400, 400))
        pygame.draw.rect(screen, black, (200, 200, 400, 400), 5)

        draw_text('SETTINGS', font, white, 245, 220)
        
        draw_text('Music Volume', font_score, white, 300, 300)
        music_volume = music_slider.update()
        music_slider.draw(screen)
        pygame.mixer.music.set_volume(music_volume)
        
        draw_text('SFX Volume', font_score, white, 300, 400)
        sfx_volume = sfx_slider.update()
        sfx_slider.draw(screen)
        coin_fx.set_volume(sfx_volume)
        jump_fx.set_volume(sfx_volume)
        game_over_fx.set_volume(sfx_volume)
        win_fx.set_volume(sfx_volume)
        plop_fx.set_volume(sfx_volume)
        
        is_in_game = not main_menu and not world_select
        if is_in_game:
            if resume_button.draw(screen):
                plop_fx.play()
                settings_active = False
            if exit_to_menu_button.draw(screen):
                plop_fx.play()
                settings_active = False
                world_select = True
                timer_running = False
                game_over = 0
                score = 0
                death_counter = 0
                pygame.mixer.music.load('img/music.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
        else:
            if back_button_select.draw(screen):
                plop_fx.play()
                settings_active = False

    elif main_menu == True:
        screen.blit(logo_img, ((screen_width // 5), - 10))
        if start_button.draw(screen):
            plop_fx.play()
            main_menu = False
            world_select = True
            world1_button.clicked = True
            world2_button.clicked = True
            world3_button.clicked = True
        if exit_button.draw(screen):
            plop_fx.play()
            run = False
        if leaderboard_button.draw(screen):
            plop_fx.play()
            leaderboard_active = True
            main_menu = False
            full_leaderboard_data = db.get_all_scores()
        if settings_button.draw(screen):
            plop_fx.play()
            settings_active = True

    elif world_select == True:
        if demon_mode != True:
            draw_text('Select World', font, yellow, (screen_width // 2) - 200, screen_height // 2 - 250)
        if demon_toggle_button.draw(screen):
            plop_fx.play()
            demon_mode = not demon_mode

        if back_button_select.draw(screen):
            plop_fx.play()
            world_select = False
            main_menu = True
            demon_mode = False
            leaderboard_data = db.get_top_scores()
        
        if not demon_mode:
            if world1_button.draw(screen):
                plop_fx.play()
                selected_world = 1
                world_select = False
                timer_running = True
                start_time = time.time()
                level = start_level
                game_over = 0
                score = 0
                score_at_level_start = 0
                death_counter = 0
                world = reset_level(level)
                pygame.mixer.music.load('img/music.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if world2_button.draw(screen):
                plop_fx.play()
                selected_world = 2
                world_select = False
                timer_running = True
                start_time = time.time()
                level = start_level
                game_over = 0
                score = 0
                score_at_level_start = 0
                death_counter = 0
                world = reset_level(level)
                pygame.mixer.music.load('img/music.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if world3_button.draw(screen):
                plop_fx.play()
                selected_world = 3
                world_select = False
                timer_running = True
                start_time = time.time()
                level = start_level
                game_over = 0
                score = 0
                score_at_level_start = 0
                death_counter = 0
                world = reset_level(level)
                pygame.mixer.music.load('img/music.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if tutorial_button.draw(screen):
                plop_fx.play()
                selected_world = 4
                world_select = False
                timer_running = True
                start_time = time.time()
                level = start_level
                game_over = 0
                score = 0
                score_at_level_start = 0
                death_counter = 0
                world = reset_level(level)
                pygame.mixer.music.load('img/music.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
        else:
            lb_x = 275
            lb_y = 150
            draw_text("DEMON WORLD - TOP SCORES", font_score, blue, lb_x, lb_y)
            lb_y += 30
            if not leaderboard_data[5]:
                draw_text("No scores", font_score, white, lb_x, lb_y)
                lb_y += 30
            else:
                for rank, row in enumerate(leaderboard_data[5], 1):
                    is_perfect = len(row) > 4 and row[4] == 1
                    entry_color = gold if is_perfect else white
                    score_text = f"{rank}. {row[0]} - {row[2]:.2f}s"
                    draw_text(score_text, font_score, entry_color, lb_x, lb_y)
                    lb_y += 30
            lb_y += 10


            original_x = world5_button.rect.x
            world5_button.rect.x = (screen_width // 2) - (world5_button.image.get_width() // 2)
            if world5_button.draw(screen):
                plop_fx.play()
                selected_world = 5
                world_select = False
                timer_running = True
                start_time = time.time()
                level = start_level
                game_over = 0
                score = 0
                score_at_level_start = 0
                death_counter = 0
                world = reset_level(level)
                pygame.mixer.music.load('img/Demon_Theme.mp3')
                pygame.mixer.music.play(-1, 0.0, 5000)
            world5_button.rect.x = original_x

    else:
        world.draw(screen)
        if game_over == 0:
            if timer_running:
                elapsed_time = time.time() - start_time
            blob_group.update()
            platform_group.update()
            collided_coins = pygame.sprite.spritecollide(player, coin_group, True)
            for _ in collided_coins:
                score += 1
                coin_fx.play()

            if back_button_game.draw(screen):
                plop_fx.play()
                world_select = True
                timer_running = False
                game_over = 0
                score = 0
                death_counter = 0
                pygame.mixer.music.load('img/music.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)

        draw_text('X ' + str(score), font_score, white, tile_size - 3, 12)
        time_text = format_time(elapsed_time)
        draw_text(time_text, font_score, white, screen_width - 220, 12)
        draw_text(death_counter, font_score, red, screen_width - 50, 12)
        screen.blit(death_img, (screen_width - 90, 0))


        if selected_world == 4 and game_over != 2:
            screen.blit(trym_img, (screen_width - 200, 90))

            bubble_x = screen_width - 400
            bubble_y = 30
            screen.blit(speech_img, (bubble_x, bubble_y))

            tut_font = pygame.font.SysFont('Bauhaus 93', 30)
            lines = []

            if level == 1:
                lines = [
                    "Move: WASD / Arrows",
                    "Jump: Space / Up",
                    "R: Restart  ESC: Menu",
                ]
            elif level == 2:
                lines = [
                    "Hold Space / Up to",
                    "jump higher to reach",
                    "higher platforms.",
                ]
            elif level == 3:
                lines = [
                    "Now its time to test",
                    "your skill bitch!",
                    "Huahuahuahuahuaa"
                ]
            text_x = bubble_x + 15
            text_y = bubble_y + 32
            line_spacing = 26
            for line in lines:
                draw_text(line, tut_font, black, text_x, text_y, outline_thickness=0)
                text_y += line_spacing
        for enemy in blob_group:
            screen.blit(enemy.image, enemy.draw_rect)
        platform_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        for spike in spike_group:
            screen.blit(spike.image, (spike.rect.x - 10, spike.rect.y - 10))
        coin_group.draw(screen)
        screen.blit(score_coin.image, score_coin.rect)

        if game_over == 0:
            game_over = player.update(
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
            )
            if game_over == -1:
                game_over_time = pygame.time.get_ticks()
        else:
            game_over = player.update(
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
            )

        if game_over == -1: 
            key = pygame.key.get_pressed()
            reset_game = False
            if restart_button.draw(screen):
                plop_fx.play()
                reset_game = True
            elif (key[pygame.K_SPACE] and pygame.time.get_ticks() - game_over_time > 400) or (key[pygame.K_RETURN]):
                reset_game = True
            
            if reset_game:
                world = reset_level(level)
                if level == 1:
                    if not demon_mode:
                        start_time = time.time()
                    timer_running = True
                death_counter += 1
                game_over = 0
                score = score_at_level_start

        if game_over == 1:
            score_at_level_start = score
            level += 1
            next_level_path = f'World_Data/World{selected_world}/level{level}_data'

            if path.exists(next_level_path):
                world = reset_level(level)
                game_over = 0
            else:
                game_over = 2
                win_fx.play()
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
                if leaderboard_active:
                    leaderboard_active = False
                    main_menu = True
                elif settings_active:
                    settings_active = False
                elif world_select:
                    world_select = False
                    main_menu = True
                    demon_mode = False
                    leaderboard_data = db.get_top_scores()
                elif main_menu:
                    run = False
                else:
                    settings_active = True
            if game_over != 2:
                if event.key == pygame.K_r:
                        level = 1
                        world = reset_level(level)
                        game_over = 0
                        score = 0
                        score_at_level_start = 0
                        death_counter = 0
                        start_time = time.time()
                        timer_running = True
                        user_text = ''
                


        if game_over == 2 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                if len(user_text) > 0:
                    total_possible_coins = get_total_coins(selected_world)
                    print(f"DEBUG: Score: {score} / Total Possible: {total_possible_coins}")
                    is_perfect_run = (score >= total_possible_coins) and (total_possible_coins > 0) and (death_counter == 0)
                    
                    db.save_highscore(user_text, selected_world, elapsed_time, score, is_perfect_run)
                    level = 1
                    world = reset_level(level)
                    game_over = 0
                    score = 0
                    score_at_level_start = 0
                    death_counter = 0
                    start_time = time.time()
                    timer_running = True
                    user_text = ''
            else:
                if len(user_text) < 9:
                    user_text += event.unicode

    if (world_select and demon_mode) or (not main_menu and not world_select and selected_world == 5):
        screen.blit(red_overlay, (0, 0))


    pygame.display.update()


pygame.quit()
