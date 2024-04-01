import pygame
from statistics import mean
from utils import map_temperature_to_color, add_unique_elements

class Sensor:
    def __init__(self, rectangle, parts_to_avg, color):
        self.rectangle = rectangle
        self.parts_to_avg = parts_to_avg
        self.color = color
        self.table = []
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rectangle)
        image = pygame.image.load(r'C:\Users\48604\Desktop\studia\sem6\PIAR\Projekt\z11\simulation\images\sensor.png')
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * 0.85), int(image.get_height() * 0.7)))
        rotated_image = pygame.transform.rotate(scaled_image, 90)
        surface.blit(rotated_image, (self.rectangle.left-12, self.rectangle.top))
        
    def check_temp(self, particles, init_temp, init_hum):
        part_rects = [part.create_circle_rect() for part in particles]
        particles_collided_indices = self.rectangle.collidelistall(part_rects)
        particles_collided = [particles[i] for i in particles_collided_indices]
        self.table = add_unique_elements(self.table, particles_collided)
        
        table_length = len(self.table)
        if table_length > self.parts_to_avg:
            self.table = self.table[table_length-self.parts_to_avg:]   
        if table_length != 0:
            temp, hum = self.measure_temp()
        else:
            temp = init_temp
            hum = init_hum
        self.color = map_temperature_to_color(temp)
        return temp, hum

            
    def measure_temp(self):
        temps = [part.temperature for part in self.table]
        hums = [part.humidity for part in self.table]
        return round(mean(temps), 2), round(mean(hums), 2)
        