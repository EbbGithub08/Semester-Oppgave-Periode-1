import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Game window
tile_size = 40
cols = 20
margin = 50
screen_width = tile_size * cols
screen_height = (tile_size * cols) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

# Load images
sun_img = pygame.image.load('img/sun.png')
sun_img = pygame.transform.scale(sun_img, (tile_size, tile_size))
bg_img = pygame.image.load('img/sky.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
dirt_img = pygame.image.load('img/dirt.png')
grass_img = pygame.image.load('img/grass.png')
blob_img = pygame.image.load('img/blob.png')
platform_x_img = pygame.image.load('img/platform.png')
platform_y_img = pygame.image.load('img/platform.png')
lava_img = pygame.image.load('img/lava.png')
coin_img = pygame.image.load('img/coin.png')
exit_img = pygame.image.load('img/exit.png')
spike_img = pygame.image.load('img/spike.png')
spike_img1 = spike_img.subsurface(0, 0, 16, 16)
spike_img2 = spike_img.subsurface(16, 0, 16, 16)
spike_img3 = spike_img.subsurface(32, 0, 16, 16)
spike_img4 = spike_img.subsurface(48, 0, 16, 16)

# Define global variables
clicked = False
level = 1
world_num = 3

# Define colors
white = (255, 255, 255)
green = (144, 201, 120)
black = (0, 0, 0)

font = pygame.font.SysFont('Futura', 24)

def create_empty_level():
	# Create empty tile list (blank med bare nuller)
	data = []
	for row in range(20):
		r = [0] * 20
		data.append(r)

	# Create boundary
	for row in range(20):
		for col in range(20):
			if row == 0:
				data[row][col] = 1
			elif row == 19:
				if col == 0 or col == 19:
					data[row][col] = 1
				else:
					data[row][col] = 2
			elif col == 0 or col == 19:
				data[row][col] = 1
	return data

# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def load_level_data(world, level_num):
	file_path = f'World_Data/World{world}/level{level_num}_data'
	if path.exists(file_path):
		with open(file_path, 'rb') as pickle_in:
			return pickle.load(pickle_in)
	return create_empty_level()

world_data = load_level_data(world_num, level)

def draw_grid():
	for c in range(21):
		# Vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
		# Horizontal lines
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))

def draw_world():
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
				if world_data[row][col] == 4:
					img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5:
					img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 6:
					img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				if world_data[row][col] == 7:
					img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 8:
					img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
					screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))
				if world_data[row][col] == 9:
					img = pygame.transform.scale(spike_img1, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 10:
					img = pygame.transform.scale(spike_img2, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 11:
					img = pygame.transform.scale(spike_img3, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 12:
					img = pygame.transform.scale(spike_img4, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))

# Main game loop
run = True
while run:

	clock.tick(fps)

	# Draw background
	screen.fill(green)
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (tile_size * 2, tile_size * 2))

	# Show grid and world
	draw_grid()
	draw_world()

	# Text for instructions
	draw_text(f'World: {world_num}  Level: {level}', font, white, 10, screen_height - 40)
	draw_text('UP/DOWN: Change Level | LEFT/RIGHT: Change World', font, white, 250, screen_height - 40)
	draw_text('S: Save Level', font, white, 650, screen_height - 40)

	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		# Key presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
				world_data = load_level_data(world_num, level)
			if event.key == pygame.K_DOWN and level > 1:
				level -= 1
				world_data = load_level_data(world_num, level)
			if event.key == pygame.K_RIGHT:
				world_num += 1
				level = 1
				world_data = load_level_data(world_num, level)
			if event.key == pygame.K_LEFT and world_num > 1:
				world_num -= 1
				level = 1
				world_data = load_level_data(world_num, level)
			if event.key == pygame.K_s:
				# Save level data
				file_path = f'World_Data/World{world_num}/level{level}_data'
				with open(file_path, 'wb') as pickle_out:
					pickle.dump(world_data, pickle_out)
				print(f'Level {level} for world {world_num} saved to {file_path}')
			
			# Tile placement
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size

			# Check that the mouse is within the tile area
			if x >= 0 and x < 20 and y >= 0 and y < 20:
				if event.key == pygame.K_0:
					world_data[y][x] = 0
				if event.key == pygame.K_1:
					world_data[y][x] = 1
				if event.key == pygame.K_2:
					world_data[y][x] = 2
				if event.key == pygame.K_3:
					world_data[y][x] = 3
				if event.key == pygame.K_4:
					world_data[y][x] = 4
				if event.key == pygame.K_5:
					world_data[y][x] = 5
				if event.key == pygame.K_6:
					world_data[y][x] = 6
				if event.key == pygame.K_7:
					world_data[y][x] = 7
				if event.key == pygame.K_8:
					world_data[y][x] = 8
				if event.key == pygame.K_9:
					if world_data[y][x] == 9:
						world_data[y][x] = 10
					elif world_data[y][x] == 10:
						world_data[y][x] = 11
					elif world_data[y][x] == 11:
						world_data[y][x] = 12
					elif world_data[y][x] == 12:
						world_data[y][x] = 9
					else:
						world_data[y][x] = 9

	pygame.display.update()

pygame.quit()