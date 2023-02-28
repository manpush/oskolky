import math
import random
import numpy as np
import scipy.interpolate

fractionOfExplosionEnergy = 0  # доля энергии взрыва

squere_count = [
    [0.120 * 0.120, 0.03*0.3],
    [0.080 * 0.080, 0.18*0.3],
    [0.040 * 0.040, 0.33*0.3],
    [0.030 * 0.030, 0.30*0.3],
    [0.070 * 0.010, 0.12*0.3],
    [0.050 * 0.010, 0.03*0.3],
    [0.005 * 0.005, 0.7],
]

class EventReaction:
    def __init__(self, mass_react, keff):
        self.mass_react, self.keff = mass_react * 100, keff


def get_count_parts(x, y):
    S = [1.5*1.2, 3*1.2]
    S.sort()
    C = [835, 1670]
    C.sort()
    y_interp = scipy.interpolate.interp1d(S, C)
    return y_interp(x*y)


class Glass:
    # m - масса вв, r - расстояние от места взрыва, ff - прочность на растяжение, a -коэффициент эквивалентности ВВ
    # ae - – доля энергии взрыва, ii - Импульс фазы сжатия, rr - приведенное расстояние
    # ee - поправочный коэффициент, p - плотность стекла,h – толщина стекла,eo – модуль Юнга
    # delp– давление во фронте,v0 - Скорость осколка,q– эффективная масса взрывчатого вещества
    # fad - f_d*ε_d
    def __init__(self, tensileStrength, moduleUng, correctionFactor, density, depth, distance_x, pos_dh, distance_z, air_resistance, event_destroy, size_x, size_y):
        """
        :param tensileStrength: прочность на растяжение
        :param moduleUng: модуль Юнга
        :param correctionFactor: поправочный коэффициент
        :param density: плотность стекла
        :param depth: толщина стекла
        :param distance_x: расстояние от места взрыва
        :param pos_dh: высота стекла над уровнем взрыва
        :param distance_z: смещение в сторону от взрыва
        :param air_resistance: Сопротивление воздуха
        :param event_destroy: event info
        :param size_x: ширина стекла
        :param size_y: высота стекла
        """
        self.tensileStrength, self.moduleUng, self.correctionFactor, self.p, self.depth, self.distance_x, self.pos_dh, self.distance_z, self.air_resistance \
            = tensileStrength, moduleUng, correctionFactor, density, depth, distance_x, pos_dh, distance_z, air_resistance
        self.event_destroy = event_destroy
        self.size_x = size_x
        self.size_y = size_y
        self.mass_react = event_destroy.mass_react

    def projectile(self, cor_dh: float = 0, correct_left: float = 0):
        q = (1 - fractionOfExplosionEnergy) * self.event_destroy.keff * self.event_destroy.mass_react  # q –
        # эффективная масса взрывчатого вещества
        rr = math.sqrt(self.distance_x ** 2 + self.distance_z ** 2) / q ** (1 / 3)  # rr - приведенное расстояние
        if rr < 17.8:
            delp = 100 * (0.92 + ((3.5 + 10.6 / rr) / rr)) / rr
        else:
            delp = 420 * rr ** (-1.45)
        ii = (350 * q ** (1 / 3)) / math.sqrt(self.distance_x ** 2 + self.distance_z ** 2)
        fad = 2.109 * self.tensileStrength ** 2 * rr ** (-0.03265) / self.moduleUng
        v = 1 / (self.p * self.depth) * (ii ** 2 + (2 * self.correctionFactor * delp - fad) * self.p * (self.depth ** 2)) ** (1 / 2)
        theta = math.atan(self.pos_dh + cor_dh / math.sqrt(self.distance_x ** 2 + self.distance_z ** 2))
        g = 9.81
        m = self.size_x * self.size_y * self.depth * self.p
        if m<0.01:
            return None, None, None, None
        square = self.size_x * self.size_y
        time = np.linspace(0, 100, 10000)
        tof = 0.0
        alpha = math.atan((self.distance_z + correct_left) / self.distance_x)
        dt = time[1] - time[0]
        gravity = -g * m
        v_x = v * math.fabs(np.cos(theta))
        v_y = v * np.sin(theta)
        r_x = 0
        r_y = self.pos_dh + cor_dh
        r_z = correct_left

        print(v, delp, m)
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
        parts_count = get_count_parts(self.size_x, self.size_y)+0
        print(parts_count)
        for i in squere_count:
            for j in range(int(i[1] * parts_count)):
                cor_dh = float(random.uniform(0.0, float(self.size_y)))
                corect_left = float(random.uniform(0.0, float(self.size_x)))
                r_xs, r_ys, r_zs, tof = Glass(self.tensileStrength, self.moduleUng, self.correctionFactor, self.p, self.depth, self.distance_x, self.pos_dh,
                                              self.distance_z,
                                              random.uniform(0.2, 1.2) / 10, self.event_destroy, math.sqrt(i[0]),
                                              math.sqrt(i[0])).projectile(cor_dh, corect_left)
                if r_zs is not None:
                    axes.plot(r_xs, r_zs, r_ys)
