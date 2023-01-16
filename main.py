import math
import random

import numpy as np
import matplotlib.pyplot as plt

from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

massVV = 7000  # масса вв
lenToBomb = 50  # расстояние от места взрыва
tensileStrength = 30000000  # прочность на растяжение
equivalenceCoefficientVV = 1  # коэффициент эквивалентности ВВ
fractionOfExplosionEnergy = 0  # доля энергии взрыва
moduleUng = 700000000000  # модуль Юнга
correctionFactor = 2.3  # поправочный коэффициент
p = 2500  # плотность стекла
depth = 0.009  # толщина стекла
dh = 5  # высота от 0 до осколка

squereCount = [
    [120*120 , 1*0.33],
    [80*80, 6*0.33],
    [40*40, 11*0.33],
    [30*30, 10*0.33],
    [70*10, 4*0.33],
    [50*10, 1*0.33],
]

class event_reaction:
    def __init__(self, mass_react, keff, rho_vozd):
        self.mass_react, self.keff, self.rho_vozd = mass_react, keff, rho_vozd
class glass:
    def __init__(self, ff, eo, ee, p, h, pos_radius, pos_dh, pos_left, rho_st, parent, square):
        self.ff, self.eo, self.ee, self.p, self.h, self.pos_radius, self.pos_dh, self.pos_left, self.rho_st = ff, eo, ee, p, h, pos_radius, pos_dh, pos_left, rho_st
        self.parent = parent
        self.square = square
        self.mass_react = parent.mass_react
        self.rho_vozd = parent.rho_vozd

    def projectile(self, cor_dh = 0, cor_left = 0):
        d = self.pos_dh
        r = self.pos_radius
        q = (1 - fractionOfExplosionEnergy) * equivalenceCoefficientVV * self.parent.mass_react  # q – эффективная масса взрывчатого вещества
        rr = r / q ** (1 / 3)  # rr - приведенное расстояние
        if rr < 17.8:
            delp = 100 * (0.92 + ((3.5 + 10.6 / rr) / rr)) / rr
        else:
            delp = 420 * rr ** (-1.45)
        ii = (350 * q ** (1 / 3)) / r
        fad = 2.109 * tensileStrength ** 2 * rr ** (-0.03265) / moduleUng
        v = 1 / (p * depth) * (ii ** 2 + (2 * correctionFactor * delp - fad) * p * (depth ** 2)) ** (1 / 2)
        theta = math.atan(self.pos_dh / r)
        Cx = 0.2 #лоб сопр
        # delta_y = 0.05  # длинна ширина осколка
        # delta_z = 0.075 #
        g = 9.81
        m = self.square * d * self.rho_st
        S = self.square
        time = np.linspace(0, 100, 10000)
        tof = 0.0
        deviation = self.pos_left
        alpha = math.atan(deviation / r)
        dt = time[1] - time[0]
        gravity = -g * m
        if np.cos(theta) < 0:
            yy = - np.cos(theta)
        else:
            yy = np.cos(theta)
        V_ix = v * yy
        V_iy = v * np.sin(theta)
        print('V', v)
        v_x = V_ix
        v_y = V_iy
        r_x = 0 
        r_z = 0 
        r_y = dh

        r_xs = list()
        r_ys = list()
        r_zs = list()

        r_xs.append(r_x)
        r_ys.append(r_y)
        r_zs.append(r_z)

        for t in time:
            F_x = 0.0
            F_y = 0.0
            dd = 0.5 * Cx * self.parent.rho_vozd * S / m
            F_y = F_y - dd
            F_x = F_x - dd * np.sign(v_x)
            F_y = F_y + gravity

            r_x = (r_x + v_x * dt * np.cos(alpha) + (F_x / (2 * m)) * dt ** 2)
            r_y = (r_y + v_y * dt + (F_y / (2 * m)) * dt ** 2)
            r_z = np.sin(alpha) * r_x * dt
            v_x = v_x + (F_x / m) * dt
            v_y = v_y + (F_y / m) * dt

            if (r_y >= 0.0):
                r_xs.append(r_x)
                r_ys.append(r_y)
                r_zs.append(r_z)
            else:
                tof = t
                r_xs.append(r_x)
                r_ys.append(r_y)
                r_zs.append(r_z)
                break

        for i in range(len(r_zs)):
            r_zs[i]+=cor_dh
        for i in range(len(r_ys)):
            r_ys[i]+=cor_left
        return r_xs, r_ys, r_zs, tof

    def get_count_parts(self):
        return 10

    def print_destroy(self, ax):
        partsCount = self.get_count_parts()
        for i in squereCount:
            for j in range(int(i[1]*partsCount)):
                #parts.append(glass(self.ff, self.eo, self.ee, self.p, self.h, self.pos_radius, self.pos_dh, self.pos_left, self.rho_st, self, i[0]))
                cor_dh = random.uniform(0, int(math.sqrt(self.square)/100))
                cor_left = random.uniform(0, int(math.sqrt(self.square)/100))
                r_xs, r_ys, r_zs, tof = glass(self.ff, self.eo, self.ee, self.p, self.h, self.pos_radius, self.pos_dh+cor_dh, self.pos_left+cor_left,
                      self.rho_st, self, i[0]).projectile(cor_dh, cor_left)
                ax.plot(r_xs, r_zs, r_ys)






        # np.interp(V, [1, 1800000],
        #           [1, 33])

#m - масса вв, r - расстояние от места взрыва, ff - прочность на растяжение, a -коэффициент эквивалентности ВВ
#ae - – доля энергии взрыва, ii - Импульс фазы сжатия, rr - приведенное расстояние
#ee - поправочный коэффициент, p - плотность стекла,h – толщина стекла,eo – модуль Юнга
#delp– давление во фронте,v0 - Скорость осколка,q– эффективная масса взрывчатого вещества
#fad - f_d*ε_d
er = event_reaction(massVV, equivalenceCoefficientVV, 1.225)
gss = glass(tensileStrength, moduleUng, correctionFactor, p, depth, lenToBomb, dh, 50, 100, er, 1500 * 1200)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
gss.print_destroy(ax)
# r_xs, r_ys, r_zs, tof = gss.projectile()
# ax.plot(r_xs, r_zs, r_ys, label="Gravity and Drag")
# ax.grid(True)

# plt.legend()
plt.axis("square")
plt.colorbar
root = Tk()
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().grid(row=0, column=0)
root.mainloop()
