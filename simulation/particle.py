import random
import math
import pygame
from utils import map_temperature_to_color, is_wall_vertical


class Particle:
    def __init__(self, x, y, temperature, humidity, velocity, radius=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.temperature = temperature
        self.humidity = humidity
        self.vx = random.uniform(-velocity, velocity)
        self.vy = random.uniform(-velocity, velocity)
        self.color = map_temperature_to_color(self.temperature)
        self.start_time = pygame.time.get_ticks()

    def move(self):
        self.x += self.vx
        self.y += self.vy
        
    def create_circle_rect(self):
        rect_width = self.radius * 2
        rect_height = self.radius * 2
        rect_x = self.x - self.radius
        rect_y = self.y - self.radius
        return pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    def check_single_wall_collision(self, wall):
        if not wall.collidepoint(self.x, self.y):
            return
        if is_wall_vertical(wall):
            if self.vx > 0:
                self.x = wall.left - self.radius
            else:
                self.x = wall.right + self.radius
            self.vx = -self.vx
        else:
            if self.vy > 0:
                self.y = wall.top - self.radius
            else:
                self.y = wall.bottom + self.radius
            self.vy = -self.vy
            
    def check_wall_collision(self, house):
        for wall in house.tmp_walls:
            self.check_single_wall_collision(wall)
        for door in house.tmp_doors:
            self.check_single_wall_collision(door)
        for window in house.tmp_windows:
            self.check_single_wall_collision(window)
            

    def check_outside_collision(self, width, height, new_temp):
        if self.x - self.radius <= 0:
            self.vx = abs(self.vx)
            self.x = self.radius
        elif self.x + self.radius >= width:
            self.vx = -abs(self.vx)
            self.x = width - self.radius
        if self.y - self.radius <= 0:
            self.vy = abs(self.vy)
            self.y = self.radius
        elif self.y + self.radius >= height:
            self.vy = -abs(self.vy)
            self.y = height - self.radius
        else:
            return
        self.temperature = new_temp
        self.color = map_temperature_to_color(new_temp)


    def check_particle_collision(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            return
        if dist <= self.radius + other.radius:
            
            # Calculate velocities after
            v1x = other.vx
            v1y = other.vy
            v2x = self.vx
            v2y = self.vy
            
            self.vx = v1x
            self.vy = v1y
            other.vx = v2x
            other.vy = v2y
            
            # Calculate the unit normal
            nx = dx / dist
            ny = dy / dist
            
            # Separate the particles so they are no longer overlapping
            overlap = (self.radius + other.radius) - dist
            self.x -= overlap / 2.0 * nx
            self.y -= overlap / 2.0 * ny
            other.x += overlap / 2.0 * nx
            other.y += overlap / 2.0 * ny
                
            # Update the temperature, humidity and color of the particles
            delta_temp = ((self.temperature - other.temperature) / (1 + (self.humidity + other.humidity)/2)) / 2
            self.temperature -= delta_temp
            other.temperature += delta_temp
            delta_hum = (self.humidity - other.humidity) / 2
            self.humidity -= delta_hum
            other.humidity += delta_hum
            self.color = map_temperature_to_color(self.temperature)
            other.color = map_temperature_to_color(other.temperature)


    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
    def is_inside_house(self, house):
        bbox = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        return house.outside_walls.contains(bbox)