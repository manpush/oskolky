import math
import random
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")

massVV = 4000  # масса вв
lenToBomb = 20  # расстояние от места взрыва
tensileStrength = 30000000  # прочность на растяжение
equivalenceCoefficientVV = 1  # коэффициент эквивалентности ВВ
fractionOfExplosionEnergy = 0  # доля энергии взрыва
moduleUng = 700000000000  # модуль Юнга
correctionFactor = 2.3  # поправочный коэффициент
p = 2500  # плотность стекла
depth = 0.009  # толщина стекла
dh = 0  # высота от 0
cor_left = 0 # сдвиг стекла относительно взрыва
x_size = 800 # ширина стекла
y_size = 1400 # высота стекла
squere_count = [
    [120 * 120, 1 * 0.33],
    [80 * 80, 6 * 0.33],
    [40 * 40, 11 * 0.33],
    [30 * 30, 10 * 0.33],
    [70 * 10, 4 * 0.33],
    [50 * 10, 1 * 0.33],
]


class EventReaction:
    def __init__(self, mass_react, keff):
        self.mass_react, self.keff = mass_react, keff


def get_count_parts(x, y):
    return math.sqrt(x * y) / 100


class Glass:
    # m - масса вв, r - расстояние от места взрыва, ff - прочность на растяжение, a -коэффициент эквивалентности ВВ
    # ae - – доля энергии взрыва, ii - Импульс фазы сжатия, rr - приведенное расстояние
    # ee - поправочный коэффициент, p - плотность стекла,h – толщина стекла,eo – модуль Юнга
    # delp– давление во фронте,v0 - Скорость осколка,q– эффективная масса взрывчатого вещества
    # fad - f_d*ε_d
    def __init__(self, ff, eo, ee, density, h, distance_x, pos_dh, distance_z, air_resistance, parent, size_x, size_y):
        """
        :param ff: прочность на растяжение
        :param eo: модуль Юнга
        :param ee: поправочный коэффициент
        :param density: плотность стекла
        :param h: толщина стекла
        :param distance_x: расстояние от места взрыва
        :param pos_dh: высота стекла над уровнем взрыва
        :param distance_z: смещение в сторону от взрыва
        :param air_resistance: ??Сопротивление??
        :param parent: event info
        :param size_x: ширина стекла
        :param size_y: высота стекла
        """
        self.ff, self.eo, self.ee, self.p, self.h, self.distance_x, self.pos_dh, self.distance_z, self.air_resistance \
            = ff, eo, ee, density, h, distance_x, pos_dh, distance_z, air_resistance
        self.parent = parent
        self.size_x = size_x
        self.size_y = size_y
        self.mass_react = parent.mass_react

    def projectile(self, cor_dh: float = 0, correct_left: float = 0):
        q = (1 - fractionOfExplosionEnergy) * equivalenceCoefficientVV * self.parent.mass_react  # q –
        # эффективная масса взрывчатого вещества
        rr = math.sqrt(self.distance_x ** 2 + self.distance_z ** 2) / q ** (1 / 3)  # rr - приведенное расстояние
        if rr < 17.8:
            delp = 100 * (0.92 + ((3.5 + 10.6 / rr) / rr)) / rr
        else:
            delp = 420 * rr ** (-1.45)
        ii = (350 * q ** (1 / 3)) / math.sqrt(self.distance_x ** 2 + self.distance_z ** 2)
        fad = 2.109 * tensileStrength ** 2 * rr ** (-0.03265) / moduleUng
        v = 1 / (p * depth) * (ii ** 2 + (2 * correctionFactor * delp - fad) * p * (depth ** 2)) ** (1 / 2)
        theta = math.atan(self.pos_dh + cor_dh / math.sqrt(self.distance_x ** 2 + self.distance_z ** 2))
        g = 9.81
        m = self.size_x * self.size_y * self.h / 100 * self.p
        square = self.size_x * self.size_y
        time = np.linspace(0, 100, 10000)
        tof = 0.0
        alpha = math.atan((self.distance_z + correct_left) / self.distance_x)
        dt = time[1] - time[0]
        gravity = -g * m
        v_x = v * math.fabs(np.cos(theta))
        v_y = v * np.sin(theta)
        r_x = 0
        r_y = dh + cor_dh
        r_z = correct_left

        r_xs = list()
        r_ys = list()
        r_zs = list()

        r_xs.append(r_x)
        r_ys.append(r_y)
        r_zs.append(r_z)

        for t in time:
            f_x = 0.0
            f_y = 0.0
            dd = 0.5 * self.air_resistance * square / m
            f_y = f_y - dd
            f_x = f_x - dd * np.sign(v_x)
            f_y = f_y + gravity

            r_x = (r_x + v_x * dt * np.cos(alpha) + (f_x / (2 * m)) * dt ** 2)
            r_y = (r_y + v_y * dt + (f_y / (2 * m)) * dt ** 2)
            r_z = correct_left + np.tan(alpha) * r_x
            v_x = v_x + (f_x / m) * dt
            v_y = v_y + (f_y / m) * dt

            r_xs.append(r_x)
            r_ys.append(r_y)
            r_zs.append(r_z)
            if not (r_y >= 0.0):
                tof = t
                break

        return r_xs, r_ys, r_zs, tof

    def print_destroy(self, axes):
        parts_count = get_count_parts(self.size_x, self.size_y)
        for i in squere_count:
            for j in range(int(i[1] * parts_count)):
                cor_dh = float(random.uniform(0.0, float(self.size_x / 100)))
                corect_left = float(random.uniform(0.0, float(self.size_y / 100)))
                r_xs, r_ys, r_zs, tof = Glass(self.ff, self.eo, self.ee, self.p, self.h, self.distance_x, self.pos_dh,
                                              self.distance_z,
                                              random.uniform(0.2, 1.2) / 10, self, math.sqrt(i[0]),
                                              math.sqrt(i[0])).projectile(cor_dh, corect_left)
                axes.plot(r_xs, r_zs, r_ys)


er = EventReaction(massVV, equivalenceCoefficientVV)
gss = Glass(tensileStrength, moduleUng, correctionFactor, p, depth, lenToBomb, dh, 10, 0.2, er, y_size, x_size)
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
gss.print_destroy(ax)
plt.axis("square")
plt.xlabel('X')
plt.ylabel('Z')
plt.show()
# root = Tk()
# canvas = FigureCanvasTkAgg(fig, root)
# canvas.get_tk_widget().grid(row=0, column=0)
# root.mainloop()
