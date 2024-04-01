import pygame
import random
from utils import check_wall_click, map_temperature_to_color
from particle import Particle
from heat_source import HeatSource
from house import House
from sensor import Sensor
from params import *
import math
from regulator.pid import PID
from aplication.connection import Connection
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution, minimize
import csv
from smell_particle import Smell
import time


class Simulation:
    def __init__(self, window_width=1200, window_height=900):
        self.window_width = window_width
        self.window_height = window_height
        self.hours = 8
        self.minutes = 0
        self.seconds = 0
        self.measured_temp = measured_temp
        self.flag1 = 0
        self.values = []
        self.T1 = 0
        self.T2 = 0
        self.K = 0
        self.Td = 0
        self.e_prev2 = 0
        self.e_prev = 0
        self.u_prev = 0
        self.K_pid = 0
        self.Ti = 0
        self.Td_pid = 0
        self.Tp = 0
        self.smell_particles = []
        self.time_emited = time.time()

    def increment_time(self, hour, min, sec):
        self.seconds += sec
        if self.seconds >= 60:
            add_minutes = self.seconds // 60
            self.minutes += add_minutes
            self.seconds -= add_minutes * 60
        self.minutes += min
        if self.minutes >= 60:
            add_hours = self.minutes // 60
            self.hours += add_hours
            self.minutes -= add_hours * 60
        self.hours += hour
        if self.hours > 24:
            self.hours -= 24
        

    def create_particles(self, num_particles, velocity, house, temperature_inside, temperature_outside):
        particles = []
        for _ in range(num_particles):
            x = random.uniform(0, self.window_width)
            y = random.uniform(0, self.window_height) 
            temperature = 0
            humidity = random.randint(0, 4)
            particle = Particle(x, y, temperature, humidity, velocity)
            if particle.is_inside_house(house):
                particle.temperature = temperature_inside
            else:
                particle.temperature = temperature_outside
                
            particle.color = map_temperature_to_color(particle.temperature)    
            particles.append(particle)
        self.particles = particles

    def initialize_simulation(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Air Conditioner++")
        self.background_color = (255, 255, 255)
        rect = pygame.Rect(610,590,40,70)
        self.initialize_sensor(rect, 10, (0,0,0))
        
    def turn_on_heater(self, heater_radius, heater_temperature, heater_humidity, particle_speed, width, height):
        pos_x = 160
        pos_y = 450 - height//2
        self.heat_source = HeatSource(pos_x, pos_y, heater_radius, heater_temperature, heater_humidity, particle_speed, width, height)

    def draw_heater(self):
        self.heat_source.draw(self.window)
    
    def check_all_collisions(self, grid_size):
        particle_grid = {}

        for p in self.particles:
            cell_x = int(p.x / grid_size)
            cell_y = int(p.y / grid_size)
            cell_key = (cell_x, cell_y)
            if cell_key not in particle_grid:
                particle_grid[cell_key] = []
            particle_grid[cell_key].append(p)

        for cell_key in particle_grid:
            cell_particles = particle_grid[cell_key]
            for i in range(len(cell_particles)):
                for j in range(i+1, len(cell_particles)):
                    cell_particles[i].check_particle_collision(cell_particles[j])
                
            
    def move_and_draw(self, house, new_temp):
        for particle in self.particles:
            particle.move()
            particle.check_wall_collision(house)
            particle.check_outside_collision(self.window_width, self.window_height, new_temp)
            particle.draw(self.window)

    def move_smell(self, screen):
        for smell_part in self.smell_particles:
            smell_part.move(screen)

    def is_check_heater_clicked(self, pos):
        return self.heat_source.rect.collidepoint(pos)
        
    def change_heater_state(self):
        mouse_pos = pygame.mouse.get_pos()
        if not self.is_check_heater_clicked(mouse_pos): 
            return
        self.heat_source.toggle_heater()
        if sim.heat_source.is_heater_clicked:
            self.heat_source.temperature = 25
        else:
            self.heat_source.temperature = 18

    def approximate(self, x, step_resp):
        T1 = x[0]
        T2 = x[1]
        K = x[2]
        self.T1 = T1
        self.T2 = T2
        self.K = K
        Td = round(x[3])
        self.Td = Td
        alfa1 = np.exp(-1/T1)
        alfa2 = np.exp(-1/T2)
        a1 = -alfa1 - alfa2
        a2 = alfa1 * alfa2
        if T1 == T2:
            T1 += 0.1
        b1 = (K / (T1 - T2)) * (T1 * (1 - alfa1) - T2 * (1 - alfa2))
        b2 = (K / (T1 - T2)) * (alfa1 * T2 * (1 - alfa2) - alfa2 * T1 * (1 - alfa1))
        length = len(step_resp)
        y = np.zeros(length)
        u = np.ones(length)
        for k in range(Td + 2 + 1, length):
            y[k] = b1 * u[k - Td - 1] + b2 * u[k - Td - 2] - a1 * y[k - 1] - a2 * y[k - 2]
        E = 0
        for j in range(length):
            E += (y[j] - step_resp[j]) ** 2
        return E
    
    def approx(self, x, step_resp):
        T1 = x[0]
        T2 = x[1]
        K = x[2]
        Td = round(x[3])
        alfa1 = np.exp(-1/T1)
        alfa2 = np.exp(-1/T2)
        a1 = -alfa1 - alfa2
        a2 = alfa1 * alfa2
        if T1 == T2:
            T1 = T2 + 0.01
        b1 = (K / (T1 - T2)) * (T1 * (1 - alfa1) - T2 * (1 - alfa2))
        b2 = (K / (T1 - T2)) * (alfa1 * T2 * (1 - alfa2) - alfa2 * T1 * (1 - alfa1))
        length = len(step_resp)
        y = np.zeros(length)
        u = np.ones(length)
        for k in range(Td + 2 + 1, length):
            y[k] = b1 * u[k - Td - 1] + b2 * u[k - Td - 2] - a1 * y[k - 1] - a2 * y[k - 2]
        return y

    def approximate_pid(self, x, step_resp):
        K_pid = x[0]
        Ti = x[1]
        Td_pid = x[2]
        Tp = 0.5
        r2 = K_pid * Td_pid / Tp
        r1 = K_pid * ((Tp / (2 * Ti)) - 2 * (Td_pid / Tp) - 1)
        r0 = K_pid * (1 + (Tp / (2 * Ti)) + (Td_pid / Tp))

        T1 = self.T1
        T2 = self.T2
        K = self.K
        Td = self.Td
        alfa1 = np.exp(-1 / T1)
        alfa2 = np.exp(-1 / T2)
        a1 = -alfa1 - alfa2
        a2 = alfa1 * alfa2
        b1 = (K / (T1 - T2)) * (T1 * (1 - alfa1) - T2 * (1 - alfa2))
        b2 = (K / (T1 - T2)) * (alfa1 * T2 * (1 - alfa2) - alfa2 * T1 * (1 - alfa1))
        length = len(step_resp * 10)
        y = np.ones(length * 10) * 18
        e = np.zeros(length * 10)
        u = np.zeros(length * 10)
        y_zad = np.ones(length * 10) * 20

        for k in range(Td + 2 + 1, length * 10):
            e[k] = y_zad[k - 1] - y[k - 1]
            e_prev2 = self.e_prev2
            e_prev = self.e_prev
            u_prev = self.u_prev
            u[k] = r2 * e_prev2 + r1 * e_prev + r0 * e[k] + u_prev
            if u[k] > 100:
                u[k] = 100
            elif u[k] < 0:
                u[k] = 0
            y[k] = b1 * u[k - Td - 1] + b2 * u[k - Td - 2] - a1 * y[k - 1] - a2 * y[k - 2]
            self.e_prev2 = e_prev
            self.e_prev = e[k]
            self.u_prev = u[k]

        E = 0
        for j in range(Td + 2 + 1, length * 10):
            E += (e[j]) ** 2
        self.K_pid = K_pid
        self.Ti = Ti
        self.Td_pid = Td_pid
        self.Tp = Tp
        return E

    def autotune(self, temp, hum):
        # startowe wartości
        starting_temp = 18
        starting_hum = 40/25
        starting_value = 80
        step_temp = 22
        step_hum = 60/25
        step_value = 100
        s_temp, s_hum = self.measured_temp
        if temp == 1:
            bias = starting_temp
            if self.flag1 == 0:
                self.heat_source.temperature = starting_temp
                self.heat_source.humidity = starting_hum
                self.heat_source.particle_speed = starting_value
                # gdy startowe osiągnie to zbieramy odpowiedź, cyk flagi
                if starting_temp - 0.5 <= s_temp <= starting_temp + 0.5 and self.flag1 == 0:
                    self.heat_source.particle_speed = step_value
                    self.heat_source.temperature = step_temp
                    self.flag1 = 1
                    self.values.append(s_temp)
            # gdy cyk flagi to czekamy az koniec zbierania
            if self.flag1 == 1:
                self.heat_source.particle_speed = step_value
                self.heat_source.temperature = step_temp
                self.values.append(s_temp)
            # gdy osiągniemy to koniec zbierania
                if step_temp - 0.5 <= s_temp <= step_temp + 0.5 and self.flag1 == 1:
                    self.flag1 = -1
        elif hum == 1:
            bias = starting_hum
            if self.flag1 == 0:
                self.heat_source.temperature = starting_temp
                self.heat_source.humidity = starting_hum
                self.heat_source.particle_speed = starting_value
            # gdy startowe osiągnie to zbieramy odpowiedź
                if (starting_hum*25 - 5) <= s_hum <= (starting_hum*25 + 0.5) and self.flag1 == 0:
                    self.heat_source.particle_speed = step_value
                    self.heat_source.humidity = step_hum
                    self.flag1 = 1
                    self.values.append(s_hum)
            if self.flag1 == 1:
                self.heat_source.particle_speed = step_value
                self.heat_source.humidity = step_hum
                self.values.append(s_hum)
                # gdy osiągniemy to zwracamy dane
                if (step_hum*25 - 5) <= s_hum <= (step_hum*25 + 5) and self.flag1 == 1:
                    self.flag1 = -1
        # pora na matme
        if self.flag1 == -1:
            # przeskalowanie danych na skok jednostkowy
            for i in range(0, len(self.values)):
                self.values[i] = (self.values[i] - bias)/(step_value - starting_value)
            #filename = "step_resp.csv"
            #with open(filename, 'w', newline='') as file:
            #    writer = csv.writer(file)
            #    writer.writerows(zip(self.values))
            self.flag1 = -2
        # values to skok jednostkowy -> do aproksymacji
        if self.flag1 == -2:
            step_resp = np.array(self.values)
            bounds = [(0.01, 1000), (0.01, 1000), (0.01, 1000), (0.01, 1000)]
            start_point = [1, 2, 1, 1]
            result = minimize(self.approximate, start_point, args=(step_resp,), bounds=bounds)
            optimal_params = result.x
            approx_values = self.approx(optimal_params, step_resp)
            self.flag1 = -3
        if self.flag1 == -3:
            step_resp = np.array(self.values)
            bounds2 = [(0.5, 100), (0.1, 100), (0.1, 100)]
            start_point2 = [1, 1, 1]
            result = minimize(self.approximate_pid, start_point2, args=(step_resp,), bounds=bounds2)
            # reset flagi
            self.flag1 = 0
            return 1
        return 0

    def regulate_both(self, pidt, set_temp, cur_temp, pidh,  set_hum, cur_hum):
        self.heat_source.temperature = set_temp
        self.heat_source.humidity = set_hum
        ut = pidt.calculate_response(set_temp, cur_temp)
        uh = pidh.calculate_response(set_hum, cur_hum)
        self.heat_source.particle_speed = (ut + uh)/2
        print("T_zad: ", self.heat_source.temperature, " H_zad: ", self.heat_source.humidity*25)

    def update(self, house, grid_size, suck_force, radius, angle_range, new_temp, init_temp, init_hum, screen):
        self.move_and_draw(house, new_temp)
        self.check_all_collisions(grid_size)
        self.heat_source.suck_and_emit_particles(self.particles, suck_force, house, radius, angle_range)
        self.draw_heater()
        house.draw_house(self.window)
        self.measured_temp = self.update_sensor(self.window, init_temp, init_hum)
        if time.time() - self.time_emited > 8:
            self.heat_source.emit_smell(self.smell_particles, angle_range, 0.5, 6, 6)
            self.time_emited = time.time()
            if len(self.smell_particles) == 2*6:
                self.smell_particles = self.smell_particles[6:]
        if len(self.smell_particles) > 0:
            self.move_smell(screen)
        
    def click_event(self, event, doors, tmp_doors, windows, tmp_windows):
        check_wall_click(event, doors, tmp_doors)
        check_wall_click(event, windows, tmp_windows)
        sim.change_heater_state()
        
    def initialize_sensor(self, rect, parts_to_avg, color):
        self.sensor = Sensor(rect, parts_to_avg, color)
        
    def update_sensor(self, surface, init_temp, init_hum):
        self.sensor.draw(surface)
        measured_temp, measured_hum = self.sensor.check_temp(self.particles, init_temp, init_hum)
        self.sensor.color = map_temperature_to_color(measured_temp)
        return measured_temp, measured_hum * 25

if __name__ == '__main__':
    sim = Simulation()
    house = House()
    pid_temp = PID(Kp_t, Ti_t, Td_t)
    pid_hum = PID(Kp_h, Ti_h, Td_h)
    connection = Connection(r'C:\Users\48604\Desktop\studia\sem6\PIAR\Projekt\z11\aplication\database.db')

    sim.initialize_simulation()    
    sim.create_particles(num_particles, velocity, house, temperature_inside, temperature_outside)
    sim.turn_on_heater(heater_radius, heater_temperature, heater_humidity, particle_speed, heater_width, heater_height)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sim.click_event(event, house.doors, house.tmp_doors, house.windows, house.tmp_windows)
                
        sim.update(house, grid_size, suck_force, radius, angle_range, temperature_outside, temperature_inside, humidity_inside, sim.window)
        sens_temp, sens_hum = sim.measured_temp
        
        font = pygame.font.Font(None, 26)
        degree_sign = u'\N{DEGREE SIGN}'
        text_temp = font.render(f'{sens_temp}{degree_sign}', True, (255, 255, 255))
        sim.window.blit(text_temp, (605, 612))
        text_humi = font.render(f'{round(sens_hum, 2)}%', True, (255, 255, 255))
        sim.window.blit(text_humi, (605, 637))
        
        print("Czujnik T: ", sens_temp," H: ", sens_hum)
        pygame.display.update()

        # pobieranie i sprawdzanie zmiennych z bazy danych

        # sprawdzenie tuningu
        tuning = connection.select_tuning()
        if tuning[1] == 1:
        #   włączenie tuningu temperatury, następnie info że nastrojone
            print("tuning temperatury...")
            is_done = sim.autotune(1, 0)
            if is_done == 1:
                connection.change_tuning_state_temperature()
                pid_temp.K = sim.K_pid
                pid_temp.Ti = sim.Ti
                pid_temp.Td = sim.Td_pid
                pid_temp.Tp = sim.Tp
                is_done = 0
        if tuning[3] == 1:
        #   włączenie tuningu wilgotności, następnie info że nastrojone
            print("tuning wilgotności...")
            is_done = sim.autotune(0, 1)
            if is_done == 1:
                connection.change_tuning_state_humidity()
                pid_hum.K = sim.K_pid
                pid_hum.Ti = sim.Ti
                pid_hum.Td = sim.Td_pid
                pid_hum.Tp = sim.Tp
                is_done = 0
        # sprawdzenie trybu regulatora
        # harmonogram
        schedule_on = connection.select_is_schedule_on()
        if schedule_on[0] == 1:
        #   uruchomienie haromogramu
            print('Tryb harmonogramu')
            harmonogram = connection.select_all_records()
            for record in harmonogram:
                time_start = record[0]
                time_end = record[1]
                split_start = time_start.split(':')
                split_end = time_end.split(':')
                hour_start = int(split_start[0])
                minute_start = int(split_start[1])
                hour_end = int(split_end[0])
                minute_end = int(split_end[1])
                # sprawdzamy czy godzina, jeśli tak to ogień
                if (sim.hours >= hour_start and sim.minutes >= minute_start) and ((sim.hours == hour_end and sim.minutes < minute_end) or (sim.hours < hour_end)):
                    t_zad = float(record[2])
                    h_zad = float(record[3]) / 25
                    # odpalamy regulatory
                    sim.regulate_both(pid_temp, t_zad, sens_temp, pid_hum, h_zad, sens_hum)

        # ciągły
        continous = connection.select_continous()
        if continous[2] == 1:
        #   uruchomienie ciągłego trybu
            print('Tryb ciągły')
            t_zad = float(continous[0])
            h_zad = float(continous[1]) / 25
            # odpalamy regulatory
            sim.regulate_both(pid_temp, t_zad, sens_temp, pid_hum, h_zad, sens_hum)

        if continous[2] == 0 and schedule_on[0] == 0:
            sim.heat_source.particle_speed = 0
            sim.heat_source.radius = 0

        sim.increment_time(0, 0, 1)
        print("Godzina: ", sim.hours, ":", sim.minutes, ":", sim.seconds)
        print("====================================")
        clock.tick(60)
