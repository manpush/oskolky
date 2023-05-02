import tkinter

import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from glassDestroy import EventReaction, Glass

matplotlib.use("TkAgg")

# plt.show()

root = Tk()

massVV = 10  # масса вв (кг)
lenToBomb = 12.3  # расстояние от места взрыва (м)
tensileStrength = 120000000  # прочность на растяжение
equivalenceCoefficientVV = 1  # коэффициент эквивалентности ВВ

moduleUng = 70000000000  # модуль Юнга
correctionFactor = 2.3  # поправочный коэффициент
p = 2500  # плотность стекла
depth = 0.006  # толщина стекла (м)
dh = 0  # высота от 0 (м)
cor_left = 0  # сдвиг стекла относительно взрыва (м)
size_x = 1.2  # ширина стекла (м)
size_y = 1.5  # высота стекла (м)
budget = 2000  # максимальная стоимость замены квадратного метра стекла

import csv

with open('glassParam.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, dialect='excel', delimiter='\t')
    glasses = [tuple(row) for row in reader]

root.rowconfigure(index=18, weight=40)

Label(root, text="Параметры события").grid(row=0, column=2, columnspan=2)

Label(root, text="Масса взрывчатого вещества (кг)").grid(row=1, column=2, sticky=E)
ent_MassVV = Entry(root, width=30)
ent_MassVV.grid(row=1, column=3)

Label(root, text="Коэффицент эквивалентности взрывчатого вещества").grid(row=2, column=2, sticky=E)
# ent_equivalenceCoefficientVV = Entry(root, width=30)
a = [1.19, 1.26, 1.28, 1, 0.99, 1.14, 0.59, 1.55, 1.5]
a.sort()
ent_equivalenceCoefficientVV = Combobox(root, values=a,
                                        state="readonly")
ent_equivalenceCoefficientVV.current(2)
ent_equivalenceCoefficientVV.grid(row=2, column=3)

Label(root, text="Параметры стекла").grid(row=3, column=2, columnspan=2)

Label(root, text="Прочность на растяжение").grid(row=4, column=2, sticky=E)
# ent_TensileStrength = Entry(root, width=30)
ent_TensileStrength = Combobox(root, values=[120000000, 30000000], state="readonly")

ent_TensileStrength.grid(row=4, column=3)

# Label(root, text="Модуль Юнга").grid(row=5, column=2, sticky=E)
# ent_ModuleUng = Entry(root, width=30)
# ent_ModuleUng.grid(row=5, column=3)
#
# Label(root, text="Поправочный коэффициент").grid(row=6, column=2, sticky=E)
# ent_CorrectionFactor = Entry(root, width=30)
# ent_CorrectionFactor.grid(row=6, column=3)

Label(root, text="Плотность стекла").grid(row=5, column=2, sticky=E)
ent_Density = Entry(root, width=30)
ent_Density.grid(row=5, column=3)

Label(root, text="Толщина стекла (м)").grid(row=6, column=2, sticky=E)
ent_Depth = Entry(root, width=30)
ent_Depth.grid(row=6, column=3)

Label(root, text="Расстояние от места взрыва по нормали к поверхности стекла (м)").grid(row=7, column=2, sticky=E)
ent_lenToBomb = Entry(root, width=30)
ent_lenToBomb.grid(row=7, column=3)

Label(root, text="Высота относительно точки взрыва (м)").grid(row=8, column=2, sticky=E)
ent_Pos_dh = Entry(root, width=30)
ent_Pos_dh.grid(row=8, column=3)

Label(root, text="Расстояние от места взрыва перпендикулярно нормали к поверхности стекла (м)").grid(row=9, column=2,
                                                                                                     sticky=E)
ent_cor_left = Entry(root, width=30)
ent_cor_left.grid(row=9, column=3)

Label(root, text="Сопротивление воздуха").grid(row=10, column=2, sticky=E)
ent_air_resistance = Entry(root, width=30)
ent_air_resistance.grid(row=10, column=3)

Label(root, text="Высота стекла (м)").grid(row=11, column=2, sticky=E)
ent_size_y = Entry(root, width=30)
ent_size_y.grid(row=11, column=3)

Label(root, text="Ширина стекла (м)").grid(row=12, column=2, sticky=E)
ent_size_x = Entry(root, width=30)
ent_size_x.grid(row=12, column=3)

Label(root, text="Максимальная вероятность поражения \nчеловека осколком / коэффицент защищённости: ").grid(row=13,
                                                                                                            column=2,
                                                                                                            sticky=E)
P_max_lbl = Label(root, text="")
P_max_lbl.grid(row=13, column=3, sticky=W)

Label(root, text="Начальная скорость осколков (м/с): ").grid(row=14, column=2, sticky=E)
V_max_lbl = Label(root, text="")
V_max_lbl.grid(row=14, column=3, sticky=W)

Label(root, text="Бюджет на замену кв. метра стекла").grid(row=15, column=2, sticky=E)
ent_budget = Entry(root, width=30)
ent_budget.grid(row=15, column=3)

Label(root, text="Оптимальное стекло для установки: ").grid(row=16, column=2, sticky=E)
tv = Treeview(show="headings", height=1)
tv['columns'] = ('h', 'p', 'price', 'speed', 'k')
tv.heading('h', text='Толщина')
tv.column('h', anchor='w', width=60)
tv.heading('p', text='Прочность на растяжение')
tv.column('p', anchor='w', width=160)
tv.heading('price', text='Цена')
tv.column('price', anchor='w', width=50)
tv.heading('speed', text='V осколка')
tv.column('speed', anchor='w', width=50)
tv.heading('k', text='K защ.')
tv.column('k', anchor='w', width=50)
tv.grid(row=16, column=3, sticky=E)


def set_default_values():
    ent_MassVV.delete(0, END)
    ent_equivalenceCoefficientVV.delete(0, END)
    # ent_TensileStrength.delete(0, END)
    # ent_ModuleUng.delete(0, END)
    # ent_CorrectionFactor.delete(0, END)
    ent_Density.delete(0, END)
    ent_Depth.delete(0, END)
    ent_lenToBomb.delete(0, END)
    ent_Pos_dh.delete(0, END)
    ent_cor_left.delete(0, END)
    ent_air_resistance.delete(0, END)
    ent_size_y.delete(0, END)
    ent_size_x.delete(0, END)
    ent_budget.delete(0, END)

    ent_MassVV.insert(0, str(massVV))
    ent_equivalenceCoefficientVV.insert(0, str(equivalenceCoefficientVV))
    ent_TensileStrength.current(1)
    # ent_ModuleUng.insert(0, str(moduleUng))
    # ent_CorrectionFactor.insert(0, str(correctionFactor))
    ent_Density.insert(0, str(p))
    ent_Depth.insert(0, str(depth))
    ent_lenToBomb.insert(0, str(lenToBomb))
    ent_Pos_dh.insert(0, str(dh))
    ent_cor_left.insert(0, str(cor_left))
    ent_air_resistance.insert(0, str(0.2))
    ent_size_y.insert(0, str(size_y))
    ent_size_x.insert(0, str(size_x))
    P_max_lbl["text"] = '0'
    V_max_lbl["text"] = '0'
    ent_budget.insert(0, str(budget))


def drop_excess_vlues():
    tv.delete(*tv.get_children())


def start_calculation():
    drop_excess_vlues()
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection='3d')
    er = EventReaction(float(ent_MassVV.get()), float(ent_equivalenceCoefficientVV.get()))
    gss = Glass(float(ent_TensileStrength.get()), moduleUng, correctionFactor, float(ent_Density.get()),
                float(ent_Depth.get()), float(ent_lenToBomb.get()), float(ent_Pos_dh.get()), float(ent_cor_left.get()),
                float(ent_air_resistance.get()), er, float(ent_size_x.get()), float(ent_size_y.get()))
    gss.print_destroy(ax)
    plt.axis("square")
    plt.xlabel('X')
    plt.ylabel('Z')
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().grid(row=0, column=0, rowspan=19)
    P_max_lbl["text"] = str(round(gss.p_max, 3)) + ' / ' + str(1 - round(gss.p_max, 3))
    V_max_lbl["text"] = str(round(gss.v_glass, 3)) + ' ' + gss.err_msg
    resVals = []
    for glass in glasses:
        resVals.append((glass, gss.get_speed(float(glass[1]), float(glass[0])),gss.max_damage_prob(glass)))
    try:
        res = max(sorted(list(filter(lambda x: float(x[0][2]) < float(ent_budget.get()), resVals)),
                         key=lambda x: float(x[0][2])), key=lambda x: float(x[2]))
        if res[2] < gss.max_damage_prob(None):
            raise Exception()
    except:
        res = (("Недостаток бюджета. ", 0, 0), 0, 0)
    tv.insert("", tkinter.END, text='Listbox', values=(
                str(res[0][0]) + " " + str(res[0][1]) + ' ' + str(res[0][2]) + ' ' + str(res[1]) + ' ' + str(res[2])))


Button(root, text="Рассчитать", command=start_calculation).grid(row=18, column=2, sticky=N)

set_default_values()
root.mainloop()
