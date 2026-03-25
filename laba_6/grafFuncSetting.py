from tkinter import filedialog, ttk, scrolledtext
import tkinter as tk

import settingwindow
import grafcreate


dictSettingPlt = {
    "xlim": "",
    "ylim": "",
    "grid": 1,
    "bgc": "white",
    "lnc": "grey"
}


class GrafBox:

    def __init__(self, root, ax=None, fig=None, canvasG=None):
        self.main_frame = ttk.Frame(root)

        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)

        self.stackFrame = ttk.Frame(self.canvas)
        self.stackFrame.pack(fill=tk.BOTH, expand=True)

        # Настройка прокрутки
        self.stackFrame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.stackFrame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.bind_all("<MouseWheel>", self.__on_mousewheel__)

        self.cells = list()
        self.ax = ax
        self.canvasG = canvasG
        self.fig = fig
        self.plot = dict()

        self.setting_graf = dictSettingPlt.copy()
        self.setting_graf_window = settingwindow.SettingWindow(self.main_frame)

        self.setting_graf_window.setConfig(self.setting_graf, 
                                           array_settings=["xlim", "ylim"],
                                           number_settings=["grid"],
                                           color_settings=["bgc", "lnc"])
        pass

    def __on_mousewheel__(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def append(self, funcs: list):
        for func in funcs:
            self.cells.append(GrafCell(self.stackFrame, func, self))

        self.stackFrame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        pass

    def appendPlot(self, func: dict):
        self.plot[func["label"]] = func
        self.__build__()
        pass

    def pack(self):
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        pass

    def unpack(self):
        self.main_frame.pack_forget()
        pass

    def __clear__(self):
        self.plot.clear()
        self.ax.clear()
        
        self.__set_setting_on_graf__()
        pass

    def __del_all__(self):
        for i in self.cells:
            i.destroy()
        
        self.cells.clear()

        self.stackFrame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        pass

    def __load__(self):
        file_path = filedialog.askopenfilename(
            title="Выберите текстовый файл",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ]
        )
    
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                content = eval(content)
                
                self.append(content)

            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
        pass
        pass

    def __save__(self):

        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ],
            initialfile="мой_файл.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    for i in self.cells:
                        i.__save__(file)
                    pass
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")
        pass

    def __save_no_points__(self):
        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ],
            initialfile="мой_файл.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("[")
                    for i in self.cells:
                        i.__save_no_points__(file)
                        if not i is self.cells[-1]: file.write(",")
                    file.write("]")
                    pass
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")
        pass


    def __save_picture__(self):
        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".png",
            filetypes=[
                ("Файл изображения PNG", "*.png"),
                ("Файл изображения JPG", "*.jpg"),
                ("Все файлы", "*.*")
            ],
            initialfile="грифик.png"
        )
        
        if file_path:
            try:
                self.fig.savefig(file_path, dpi=300)
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")
        pass
    
    def __build__(self):

        self.ax.clear()

        for v in self.plot.values():
            self.ax.plot(v["points_x"], v["points_y"], color=v["color"], linewidth=v["linewidth"], linestyle=v["linestyle"])

        self.__set_setting_on_graf__()

        pass

    def __build_all__(self):


        for c in self.cells:
            value = c.value
            self.plot[value["label"]] = value

        self.__build__()

        pass


    def __del_cell__(self, cell):

        for i in range(len(self.cells)):
            if self.cells[i] is cell:
                self.cells[i].destroy()
                del self.cells[i]
                break
            pass

        self.stackFrame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        pass


    def __setting_graf__(self):

        self.setting_graf_window.createWindow("Настройка графического поля")

        self.setting_graf = self.setting_graf_window.getSettings().copy()

        self.__set_setting_on_graf__()
        pass


    def __set_setting_on_graf__(self):

        self.ax.relim()
        self.ax.set_autoscale_on(True)
        self.ax.autoscale_view()

        if self.setting_graf["xlim"]:
            self.ax.set_xlim(*self.setting_graf["xlim"])


        
        if self.setting_graf["ylim"]:
            self.ax.set_ylim(*self.setting_graf["ylim"])


        self.ax.set_facecolor(self.setting_graf["bgc"])
        


        self.ax.grid(self.setting_graf["grid"], color=self.setting_graf["lnc"])
        self.canvasG.draw()

        pass

    pass


class GrafCell:


    def __init__(self, root, value: dict, stack: GrafBox):

        self.value = value
        self.stack = stack

        self.cellFrame = ttk.Frame(root, relief=tk.RIDGE, borderwidth=3)
        self.cellFrame.pack(fill=tk.BOTH, expand=True, pady=2, padx=5)

        ttk.Label(self.cellFrame, text=value.get("label", "None"), padding=10
                  ).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(self.cellFrame)
        button_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        self.setting = settingwindow.SettingWindow(root)

        linestyle_options = ["-", "--", "-.", ":", "solid", "dashed", "dashdot", "dotted"]
    

        self.setting.setConfig(copyNoPoints(value),
                                color_settings=["color"],
                                number_settings=["linewidth", "dots"],
                                array_settings=["range"],
                                args_settings=value.get("args", dict()).keys(),
                                choice_settings={"linestyle": linestyle_options})

        ttk.Button(
            button_frame, 
            text="Настройки", 
            width=10,
            command=self.__setting__
        ).pack(side=tk.LEFT, padx=2, expand=1, fill=tk.BOTH)
        ttk.Button(
            button_frame, 
            text="Построить", 
            width=10,
            command=self.__build__
        ).pack(side=tk.LEFT, padx=2, expand=1, fill=tk.BOTH)
        ttk.Button(
            button_frame, 
            text="Сохранить", 
            width=10,
            command=self.__save__
        ).pack(side=tk.LEFT, padx=2, expand=1, fill=tk.BOTH)
        ttk.Button(
            button_frame, 
            text="Сохранить БТ", 
            width=13,
            command=self.__save_no_points__
        ).pack(side=tk.LEFT, padx=2, expand=1, fill=tk.BOTH)
        ttk.Button(
            button_frame, 
            text="Удалить", 
            width=10,
            command=self.__del_func__
        ).pack(side=tk.LEFT, padx=2, expand=1, fill=tk.BOTH)

        if self.value.get(f"points_{self.value["param"]}", []) == []:
            self.remath()
        pass
    
    def __setting__(self):
        self.setting.createWindow()

        self.value = self.setting.getSettings().copy()

        self.remath()
        pass

    def remath(self):
        if self.value["param"] in "xyrp":
            grafcreate.create_points_explicit(self.value)
        else:
            grafcreate.create_points_parametrs(self.value)

    def __del_func__(self):
        self.stack.__del_cell__(self)
        pass

    def __save__(self, file=None):

        if not file is None:
            file.write(str(self.value))
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ],
            initialfile="мой_файл.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str([self.value]))
                    pass
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")
        pass

    def __save_no_points__(self, file=None):

        if not file is None:
            file.write(str(self.setting.getSettings()))
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ],
            initialfile="мой_файл.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str([self.setting.getSettings()]))
                    pass
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")
        pass

    def __build__(self):
        self.stack.appendPlot(self.value)
        pass

    def destroy(self):
        self.cellFrame.destroy()
        pass


    pass


def copyNoPoints(value: dict):

    res = {k: v for k,v in value.items() if not "points_" in k}
    return res