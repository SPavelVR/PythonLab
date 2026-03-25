import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import textFuncSetting
import grafFuncSetting

class Program:
    def __init__(self, root):
        self.root = root
        self.root.title("Создание графика")
        

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)


        self.graf = grafFuncSetting.GrafBox(main_frame)
        self.text = textFuncSetting.ConsoleGraf(main_frame, self.graf)


        

        menubar = tk.Menu(root)
        root.config(menu=menubar)
        

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Текстовый файл", command=self.f1)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=root.quit)
        file_menu.add_command(label="Загрузить", command=self.text.__load__)
        file_menu.add_command(label="Сохранить", command=self.text.__save__)
        file_menu.add_command(label="Скомпилировать", command=self.text.__compile__)
        
        graphs_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Графики", menu=graphs_menu)
        graphs_menu.add_command(label="Графики",                command=self.f2)
        graphs_menu.add_separator()
        graphs_menu.add_command(label="Построить",              command=self.graf.__build__)
        graphs_menu.add_command(label="Построить все",          command=self.graf.__build_all__)
        graphs_menu.add_command(label="Стереть",                command=self.graf.__clear__)
        graphs_menu.add_command(label="Загрузить",              command=self.graf.__load__)
        graphs_menu.add_command(label="Сохранить",              command=self.graf.__save__)
        graphs_menu.add_command(label="Сохранить без точек",    command=self.graf.__save_no_points__)
        graphs_menu.add_command(label="Сохранить изображение",  command=self.graf.__save_picture__)
        graphs_menu.add_command(label="Удалить все",            command=self.graf.__del_all__)
        graphs_menu.add_command(label="Настроить",              command=self.graf.__setting_graf__)


        center_frame = ttk.Frame(main_frame)
        center_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.grid(True, color="grey")
        
        self.canvas = FigureCanvasTkAgg(fig, master=center_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.graf.ax = ax
        self.graf.canvasG = self.canvas
        self.graf.fig = fig

        self.graf.__set_setting_on_graf__()

        self.f1()
        pass

    def f1(self):
        self.text.pack()
        self.graf.unpack()

    def f2(self):
        self.text.unpack()
        self.graf.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Program(root)
    root.mainloop()