import random
import pygame
import time

class Smell:
    def __init__(self, x, y, velocity, duration):
        self.x = x
        self.y = y
        self.vx = random.uniform(-velocity, velocity)
        self.vy = random.uniform(-velocity, velocity)
        self.timer = time.time()
        self.duration = duration
        self.image =  self.scale_image(r'C:\Users\48604\Desktop\studia\sem6\PIAR\Projekt\z11\simulation\images\flower.png')
        self.alpha = 255
        
    def move(self, surface):
        self.x += self.vx
        self.y += self.vy
        self.update()
        self.draw(surface)

    def draw(self, surface):
        if self.alpha > 0:
            self.image.set_alpha(self.alpha)
        surface.blit(self.image, (self.x, self.y))
        
    def update(self):
        time_elapsed = time.time() - self.timer
        if time_elapsed >= self.duration:
            self.alpha = 0
        else:
            self.alpha = int((1 - time_elapsed / self.duration) * 255)
            
    def scale_image(self, path):
        image =  pygame.image.load(path)
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * 0.05), int(image.get_height() * 0.05)))
        return scaled_image