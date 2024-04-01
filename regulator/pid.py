from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt


class PID():
    def __init__(self, k, ti, td):
        self.K = k
        self.Ti = ti
        self.Td = td
        self.Tp = 0.5
        self.e_prev2 = 0
        self.e_prev = 0
        self.u_prev = 0

    def calculate_response(self, y_zad, y):
        K = self.K
        Ti = self.Ti
        Td = self.Td
        Tp = self.Tp
        e_prev2 = self.e_prev2
        e_prev = self.e_prev
        u_prev = self.u_prev
        e = y_zad - y
        r2 = K * Td / Tp
        r1 = K * ((Tp / (2 * Ti)) - 2 * (Td / Tp) - 1)
        r0 = K * (1 + (Tp / (2 * Ti)) + (Td / Tp))

        u = r2 * e_prev2 + r1 * e_prev + r0 * e + u_prev
        if u > 100:
            u = 100
        elif u < 0:
            u = 0

        self.e_prev2 = e_prev
        self.e_prev = e
        self.u_prev = u

        return u
