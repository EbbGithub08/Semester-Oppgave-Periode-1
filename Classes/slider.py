import pygame
from pygame import mixer

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

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
plop_fx = pygame.mixer.Sound('img/plop.wav')
plop_fx.set_volume(0.2)

class Slider:
    def __init__(self, x, y, width, height, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.val = initial_val
        self.dragging = False
        self.last_step = int(initial_val * 10)

    def draw(self, surface):
        pygame.draw.rect(surface, gray, self.rect)
        pygame.draw.rect(surface, black, self.rect, 2)
        
        knob_x = self.rect.x + (self.val * self.rect.width)
        knob_rect = pygame.Rect(knob_x - 10, self.rect.y - 10, 20, self.rect.height + 20)
        pygame.draw.rect(surface, white, knob_rect)
        pygame.draw.rect(surface, black, knob_rect, 2)

    def update(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if click[0] == 0:
            self.dragging = False
        elif click[0] == 1 and self.rect.collidepoint(pos):
            self.dragging = True
            
        if self.dragging:
            rel_x = pos[0] - self.rect.x
            self.val = rel_x / self.rect.width
            self.val = max(0.0, min(1.0, self.val))
            
            current_step = int(self.val * 10)
            if current_step != self.last_step:
                plop_fx.play()
                self.last_step = current_step
        
        return self.val