import matplotlib.pyplot as plt
from tkinter import *
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

moduleUng = 700000000000  # модуль Юнга
correctionFactor = 2.3  # поправочный коэффициент
p = 2500  # плотность стекла
depth = 0.006  # толщина стекла (м)
dh = 0  # высота от 0 (м)
cor_left = 0  # сдвиг стекла относительно взрыва (м)
size_x = 1.2  # ширина стекла (м)
size_y = 1.5  # высота стекла (м)

root.rowconfigure(index=15, weight=40)

Label(root, text="Параметры события").grid(row=0, column=2, columnspan=2)

Label(root, text="Масса взрывчатого вещества").grid(row=1, column=2, sticky=E)
ent_MassVV = Entry(root, width=30)
ent_MassVV.grid(row=1, column=3)

Label(root, text="Коэффицент эквивалентности взрывчатого вещества").grid(row=2, column=2, sticky=E)
ent_equivalenceCoefficientVV = Entry(root, width=30)
ent_equivalenceCoefficientVV.grid(row=2, column=3)

Label(root, text="Параметры стекла").grid(row=3, column=2, columnspan=2)

Label(root, text="Прочность на растяжение").grid(row=4, column=2, sticky=E)
ent_TensileStrength = Entry(root, width=30)
ent_TensileStrength.grid(row=4, column=3)

Label(root, text="Модуль Юнга").grid(row=5, column=2, sticky=E)
ent_ModuleUng = Entry(root, width=30)
ent_ModuleUng.grid(row=5, column=3)

Label(root, text="Поправочный коэффициент").grid(row=6, column=2, sticky=E)
ent_CorrectionFactor = Entry(root, width=30)
ent_CorrectionFactor.grid(row=6, column=3)

Label(root, text="Плотность стекла").grid(row=7, column=2, sticky=E)
ent_Density = Entry(root, width=30)
ent_Density.grid(row=7, column=3)

Label(root, text="Толщина стекла (м)").grid(row=8, column=2, sticky=E)
ent_Depth = Entry(root, width=30)
ent_Depth.grid(row=8, column=3)

Label(root, text="Расстояние от места взрыва по нормали к поверхности стекла(м)").grid(row=9, column=2, sticky=E)
ent_lenToBomb = Entry(root, width=30)
ent_lenToBomb.grid(row=9, column=3)

Label(root, text="Высота относительно точки взрыва (м)").grid(row=10, column=2, sticky=E)
ent_Pos_dh = Entry(root, width=30)
ent_Pos_dh.grid(row=10, column=3)

Label(root, text="Расстояние от места взрыва перпендикулярно нормали к поверхности стекла").grid(row=11, column=2, sticky=E)
ent_cor_left = Entry(root, width=30)
ent_cor_left.grid(row=11, column=3)

Label(root, text="Сопротивление воздуха").grid(row=12, column=2, sticky=E)
ent_air_resistance = Entry(root, width=30)
ent_air_resistance.grid(row=12, column=3)

Label(root, text="Высота стекла").grid(row=13, column=2, sticky=E)
ent_size_y = Entry(root, width=30)
ent_size_y.grid(row=13, column=3)

Label(root, text="Ширина стекла").grid(row=14, column=2, sticky=E)
ent_size_x = Entry(root, width=30)
ent_size_x.grid(row=14, column=3)

def set_default_values():
    ent_MassVV.delete(0, END)
    ent_equivalenceCoefficientVV.delete(0, END)
    ent_TensileStrength.delete(0, END)
    ent_ModuleUng.delete(0, END)
    ent_CorrectionFactor.delete(0, END)
    ent_Density.delete(0, END)
    ent_Depth.delete(0, END)
    ent_lenToBomb.delete(0, END)
    ent_Pos_dh.delete(0, END)
    ent_cor_left.delete(0, END)
    ent_air_resistance.delete(0, END)
    ent_size_y.delete(0, END)
    ent_size_x.delete(0, END)

    ent_MassVV.insert(0, str(massVV))
    ent_equivalenceCoefficientVV.insert(0, str(equivalenceCoefficientVV))
    ent_TensileStrength.insert(0, str(tensileStrength))
    ent_ModuleUng.insert(0, str(moduleUng))
    ent_CorrectionFactor.insert(0, str(correctionFactor))
    ent_Density.insert(0, str(p))
    ent_Depth.insert(0, str(depth))
    ent_lenToBomb.insert(0, str(lenToBomb))
    ent_Pos_dh.insert(0, str(dh))
    ent_cor_left.insert(0, str(cor_left))
    ent_air_resistance.insert(0, str(0.2))
    ent_size_y.insert(0, str(size_y))
    ent_size_x.insert(0, str(size_x))



def start_calculation():
    fig = plt.figure(figsize=(9, 9))

    ax = fig.add_subplot(111, projection='3d')
    er = EventReaction(float(ent_MassVV.get()), float(ent_equivalenceCoefficientVV.get()))
    gss = Glass(float(ent_TensileStrength.get()), float(ent_ModuleUng.get()), float(ent_CorrectionFactor.get()), float(ent_Density.get()), float(ent_Depth.get()), float(ent_lenToBomb.get()), float(ent_Pos_dh.get()), float(ent_cor_left.get()), float(ent_air_resistance.get()), er, float(ent_size_y.get()), float(ent_size_x.get()))
    gss.print_destroy(ax)
    plt.axis("square")
    plt.xlabel('X')
    plt.ylabel('Z')
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().grid(row=0, column=0, rowspan=16)


Button(root, text="Рассчитать", command=start_calculation).grid(row=15, column=2, sticky=N)

set_default_values()
root.mainloop()
