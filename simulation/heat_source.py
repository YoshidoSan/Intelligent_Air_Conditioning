import pygame
from particle import Particle
import math
import random
from utils import *
from smell_particle import Smell

class HeatSource:
    def __init__(self, x, y, radius, temperature, humidity, particle_speed, width, height):
        self.x = x
        self.y = y
        self.radius = radius
        self.temperature = temperature
        self.humidity = humidity
        self.particle_speed = particle_speed  # pixels per frame
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_heater_clicked = False

    def draw(self, surface):
        color = map_temperature_to_color(self.temperature)
        pygame.draw.rect(surface, color, self.rect)
        image = pygame.image.load(r'C:\Users\48604\Desktop\studia\sem6\PIAR\Projekt\z11\simulation\images\conditioner.png')
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * 0.54), int(image.get_height() * 0.53)))
        rotated_image = pygame.transform.rotate(scaled_image, 90)
        surface.blit(rotated_image, (self.rect.left-60, self.rect.top - 60))
    
    def toggle_heater(self):
        self.is_heater_clicked = not self.is_heater_clicked

    def suck_and_emit_particles(self, particles, suck_force, house, circle_radius, angle_range):
        for p in particles:
            if not p.is_inside_house(house):
                continue
            
            dx1 = p.x - (self.x + self.width//2)
            dy1 = p.y - self.y
            dx2 = p.x - (self.x + self.width//2)
            dy2 = p.y - (self.y + self.height)

            distance1 = math.sqrt(dx1**2 + dy1**2)
            distance2 = math.sqrt(dx2**2 + dy2**2)
            
            elapsed_time = pygame.time.get_ticks() - p.start_time
            
            if distance1 <= self.radius and dy1 <= 0 and elapsed_time > 1000:
                p.vx -= suck_force * dx1 /distance1**2
                p.vy -= suck_force * dy1 /distance1**2
                
            if distance2 <= self.radius and dy2 >= 0 and elapsed_time > 1000:
                p.vx -= suck_force * dx2 / distance2**2
                p.vy -= suck_force * dy2 / distance2**2
                
            circle_rect = pygame.Rect(p.x-circle_radius, p.y-circle_radius, circle_radius*2, circle_radius*2)
            is_inside = circle_rect.colliderect(self.rect)
            
            if distance1 <= circle_radius and dy1 <= 0 or distance2 <= circle_radius and dy2 >= 0 or is_inside and elapsed_time > 1000:
                particles.remove(p)
                self.emit_particle(particles, angle_range, self.temperature, self.humidity, self.particle_speed)
                


    def emit_particle(self, particles, angle_range, particles_temp, humidity, velocity):
        particle_x = self.x + self.width/2 + random.uniform(-2, 2)
        particle_y = self.y + self.height/2 + random.uniform(-2, 2)
        angle = random.randint(-angle_range, angle_range)
        angle = math.radians(angle)
        particle_vx = 2 * math.cos(angle)
        particle_vy = 2 * math.sin(angle)
        
        particle = Particle(particle_x, particle_y, particles_temp, humidity, velocity)
        particle.vx = particle_vx
        particle.vy = particle_vy
        particles.append(particle)
        
    def emit_smell(self, smell_particles, angle_range, velocity, duration, num):
        for _ in range(num):
            particle_x = self.x + self.width/2 + random.uniform(-2, 2)
            particle_y = self.y + self.height/2 + random.uniform(-2, 2)
            angle = random.randint(-angle_range, angle_range)
            angle = math.radians(angle)
            particle_vx = math.cos(angle)
            particle_vy = math.sin(angle)
            
            particle = Smell(particle_x, particle_y, velocity, duration)
            particle.vx = particle_vx
            particle.vy = particle_vy
            smell_particles.append(particle)
            



