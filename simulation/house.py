import pygame

class House:
    def __init__(self, color=(0,0,0), color_door = (70, 90, 90), color_window = (0, 255, 255)):
        self.color = color
        self.color_door = color_door
        self.color_window = color_window
        
        self.outside_walls = pygame.Rect(150, 100, 860, 710)
        self.walls = self.spawns_walls()
        self.doors = self.spawn_doors()
        self.windows = self.spawn_windows()
        
        self.tmp_walls = self.walls.copy()
        self.tmp_doors = self.doors.copy()
        self.tmp_windows = self.windows.copy()

    def spawns_walls(self):
        walls = []
        
        w1 = pygame.Rect(150, 100, 325, 10)
        w2 = pygame.Rect(525, 100, 125, 10)
        w3 = pygame.Rect(150, 100, 10, 700)
        
        w4 = pygame.Rect(150, 800, 200, 10)
        w5 = pygame.Rect(450, 800, 200, 10)
        w6 = pygame.Rect(650, 100, 10, 185)
        w7 = pygame.Rect(650, 335, 10, 475)
        
        w8 = pygame.Rect(650, 100, 350, 10)
        w9 = pygame.Rect(1000, 100, 10, 25)
        w10 = pygame.Rect(1000, 175, 10, 625)
        
        w11 = pygame.Rect(660, 800, 125, 10)
        w12 = pygame.Rect(885, 800, 125, 10)
        w13 = pygame.Rect(650, 400, 20, 10)
        w14 = pygame.Rect(720, 400, 280, 10)
        
        w15 = pygame.Rect(650, 200, 20, 10)
        w16 = pygame.Rect(720, 200, 280, 10)
        w17 = pygame.Rect(800, 200, 10, 75)
        w18 = pygame.Rect(800, 325, 10, 75)
        
        walls.extend([w1,w2,w3,w4,w5,w6,w7,w8,w9])
        walls.extend([w10,w11,w12,w13,w14,w15,w16,w17,w18])
        return walls
    
    def spawn_doors(self):
        doors = []
        d2 = pygame.Rect(801, 275, 8, 50)
        d3 = pygame.Rect(670, 201, 50, 8)
        d4 = pygame.Rect(670, 401, 50, 8)
        d5 = pygame.Rect(651, 285, 8, 50)
        
        doors.extend([d2,d3,d4,d5])
        return doors
    
    def spawn_windows(self):
        windows  = []
        win0 = pygame.Rect(475, 101, 50, 8)
        win1 = pygame.Rect(785, 802, 100, 6)
        win2 = pygame.Rect(1002, 125, 6, 50)
        win3 = pygame.Rect(350, 802, 100, 6)
        
        windows.extend([win0,win1,win2,win3])
        return windows

    def draw_objects_with_color(self, surface, color, objects):
        for object in objects:
            pygame.draw.rect(surface, color, object)
            
    def draw_house(self, surface):
        self.draw_objects_with_color(surface, self.color, self.tmp_walls)
        self.draw_objects_with_color(surface, self.color_door, self.tmp_doors)
        self.draw_objects_with_color(surface, self.color_window, self.tmp_windows)
        
