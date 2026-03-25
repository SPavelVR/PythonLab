from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import ast

def validateInt(text: str):
    if text == "" or text == "-": return True
    try:
        float(text)
        return True
    except:
        return False

def validatePosint(text: str):
    if text == "": return True
    try:
        return (float(text) >= 0)
    except:
        return False

def validateNegint(text: str):
    if text == "" or text == "-": return True
    try:
        return (float(text) <= 0)
    except:
        return False

def getFloat(text: str):
    if text == "" or text == "-": return None
    return float(text)


class SettingWindow:
    root: Tk = None
    window: Toplevel = None
    canvas: Canvas = None
    
    settings: dict 
    settingwidgets: dict
    

    color_settings: list        # настройки цвета
    number_settings: list       # числовые настройки
    str_settings: list          # строковые настройки
    array_settings: list        # настройки массивов (для range)
    args_settings: list         # аргументы для eval
    choice_settings: dict       # настройки с выбором (linestyle, marker и тд)
    
    def __init__(self, root):
        self.root = root
        self.settings           = dict()
        self.settingwidgets     = dict()
        
        self.color_settings     = list()
        self.number_settings    = list()
        self.array_settings     = list()
        self.args_settings      = list()
        self.choice_settings    = dict()

        
        self.__registor_int__ = (root.register(validateInt), '%P')
        self.__registor_posint__ = (root.register(validatePosint), '%P')
        self.__registor_negint__ = (root.register(validateNegint), '%P')
        pass
    
    def setCanvas(self, canvas: Canvas):
        self.canvas = canvas
    
    def setConfig(self, config: dict, 
                  color_settings: list = None,
                  number_settings: list = None,
                  array_settings: list = None,
                  args_settings: list = None,
                  str_settings: list = None,
                  choice_settings: dict = None
                  ):

        self.settings = config.copy()
        

        self.color_settings = color_settings if color_settings else list()
        self.number_settings = number_settings if number_settings else list()
        self.array_settings = array_settings if array_settings else list()
        self.args_settings = args_settings if args_settings else list()
        self.str_settings = str_settings if str_settings else list()
        self.choice_settings = choice_settings if choice_settings else dict()
        pass
    
    def getSettings(self) -> dict:
        return self.settings
    
    def createWindow(self, title: str = "Настройки"):
        self.window = Toplevel(self.root)
        self.window.title(title)
        

        self.window.transient(self.root)
        self.window.grab_set()
        
        self.__create_widget__()
        
        self.root.wait_window(self.window)
        pass
    
    def __create_widget__(self):
        # Создаем canvas с прокруткой для множества настроек
        canvas_frame = Frame(self.window)
        canvas_frame.pack(fill=BOTH, expand=1)
        
        canvas = Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.pack(side=RIGHT, fill=Y)
        

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        buttonFrame = Frame(self.window)
        buttonFrame.pack(fill=BOTH, expand=1, padx=10, pady=5)
        
        row = 0
        

        if self.color_settings:
            self.__create_section__(scrollable_frame, "Цвета", row)
            row = self.__create_color_widgets__(scrollable_frame, row + 1)
        
        if self.number_settings:
            self.__create_section__(scrollable_frame, "Числовые параметры", row)
            row = self.__create_number_widgets__(scrollable_frame, row + 1)

        if self.str_settings:
            self.__create_section__(scrollable_frame, "Строковые параметры", row)
            row = self.__create_str_widgets__(scrollable_frame, row + 1)
        
        if self.choice_settings:
            self.__create_section__(scrollable_frame, "Стили", row)
            row = self.__create_choice_widgets__(scrollable_frame, row + 1)
        
        if self.array_settings:
            self.__create_section__(scrollable_frame, "Массивы", row)
            row = self.__create_array_widgets__(scrollable_frame, row + 1)
        
        if self.args_settings:
            self.__create_section__(scrollable_frame, "Параметры функции", row)
            row = self.__create_args_widgets__(scrollable_frame, row + 1)
        
        
        btn_frame = Frame(buttonFrame)
        btn_frame.pack()
        
        Button(btn_frame, text="Применить значения",
               command=self.__return_from_window__,
               font=("Arial", 12, "bold"),
               bg="#A70347", fg="white",
               padx=20, pady=8).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Сбросить",
               command=self.__clear_settings__,
               font=("Arial", 12, "bold"),
               bg="#03A75A", fg="white",
               padx=20, pady=8).pack(side=LEFT, padx=5)
        
        pass
    
    def __create_section__(self, parent, title, row):
        section_frame = Frame(parent)
        section_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(10, 5))
        
        Label(section_frame, text=title, font=("Arial", 12, "bold"),
              bg="#E0E0E0", fg="#333").pack(fill=X, padx=5, pady=2)
        
        return row
    
    def __create_color_widgets__(self, parent, start_row):
        row = start_row
        
        for arg_name in self.color_settings:
            if arg_name not in self.settings:
                continue
                
            current_value = self.settings[arg_name]
            
            label = Label(parent, text=arg_name.capitalize(), 
                         font=("Arial", 10, "bold"))
            label.grid(row=row, column=0, pady=5, padx=5, sticky="w")
            

            color_frame = Frame(parent)
            color_frame.grid(row=row, column=1, pady=5, sticky="w")
            

            color_entry = Entry(color_frame, font=("Arial", 10), width=15)
            color_entry.insert(0, current_value)
            color_entry.pack(side=LEFT, padx=5)
            

            def choose_color(entry=color_entry):
                color = askcolor(title="Выберите цвет", 
                                initialcolor=entry.get())
                if color[1]:
                    entry.delete(0, END)
                    entry.insert(0, color[1])
            
            color_btn = Button(color_frame, text="Выбрать", 
                              command=choose_color,
                              bg="#4CAF50", fg="white",
                              font=("Arial", 9))
            color_btn.pack(side=LEFT, padx=5)
            
            self.settingwidgets[arg_name] = color_entry
            row += 1
        
        return row
    
    def __create_number_widgets__(self, parent, start_row):
        row = start_row
        
        for arg_name in self.number_settings:
            if arg_name not in self.settings:
                continue
                
            current_value = self.settings[arg_name]
            
            label = Label(parent, text=arg_name.capitalize(), 
                         font=("Arial", 10, "bold"))
            label.grid(row=row, column=0, pady=5, padx=5, sticky="w")
            
            widget = Entry(parent, font=("Arial", 10),
                          validate="key",
                          validatecommand=self.__registor_int__)
            widget.insert(0, str(current_value))
            widget.grid(row=row, column=1, pady=5, sticky="w")
            
            self.settingwidgets[arg_name] = widget
            row += 1
        
        return row
    
    def __create_str_widgets__(self, parent, start_row):

        row = start_row

        for arg_name in self.str_settings:
            if arg_name not in self.settings:
                continue
                
            current_value = self.settings[arg_name]
            
            label = Label(parent, text=arg_name.capitalize(), 
                         font=("Arial", 10, "bold"))
            label.grid(row=row, column=0, pady=5, padx=5, sticky="w")
            
            widget = Entry(parent, font=("Arial", 10))
            widget.insert(0, str(current_value))
            widget.grid(row=row, column=1, pady=5, sticky="w")
            
            self.settingwidgets[arg_name] = widget
            row += 1

        return row
    
    def __create_choice_widgets__(self, parent, start_row):
        row = start_row
        
        for arg_name, options in self.choice_settings.items():
            if arg_name not in self.settings:
                continue
                
            current_value = self.settings[arg_name]
            
            label = Label(parent, text=arg_name.capitalize(), 
                         font=("Arial", 10, "bold"))
            label.grid(row=row, column=0, pady=5, padx=5, sticky="w")
            

            combo = ttk.Combobox(parent, values=options, 
                                 font=("Arial", 10), 
                                 state="readonly",
                                 width=20)
            combo.set(current_value)
            combo.grid(row=row, column=1, pady=5, sticky="w")
            
            self.settingwidgets[arg_name] = combo
            row += 1
        
        return row
    
    def __create_array_widgets__(self, parent, start_row):
        row = start_row
        
        for arg_name in self.array_settings:
            if arg_name not in self.settings:
                continue
                
            current_value = self.settings[arg_name]
            
            label = Label(parent, text=arg_name.capitalize(), 
                         font=("Arial", 10, "bold"))
            label.grid(row=row, column=0, pady=5, padx=5, sticky="nw")
            

            array_frame = Frame(parent)
            array_frame.grid(row=row, column=1, pady=5, sticky="w")
            

            if isinstance(current_value, list):
                value_text = ", ".join(str(v) for v in current_value)
            else:
                value_text = str(current_value)
            

            array_entry = Entry(array_frame, font=("Arial", 10), width=30)
            array_entry.insert(0, value_text)
            array_entry.pack(side=LEFT, padx=5)
            
            self.settingwidgets[arg_name] = array_entry
            row += 1
        
        return row
    
    def __create_args_widgets__(self, parent, start_row):
        row = start_row
        
        for arg_name in self.args_settings:
            current_value = self.settings.get("args", {}).get(arg_name, 0)
            
            label = Label(parent, text=arg_name.capitalize(), 
                         font=("Arial", 10, "bold"))
            label.grid(row=row, column=0, pady=5, padx=5, sticky="w")
            
            widget = Entry(parent, font=("Arial", 10),
                          validate="key",
                          validatecommand=self.__registor_int__)
            widget.insert(0, str(current_value))
            widget.grid(row=row, column=1, pady=5, sticky="w")
            
            self.settingwidgets[arg_name] = widget
            row += 1
        
        return row
    
    def __parse_array_value__(self, value_str: str):
        value_str = value_str.replace(" ", "")
        

        if len(value_str) > 0 and value_str[0] == '[' and value_str[-1] == ']':
            try:
                return value_str[1:-1]
            except:
                pass
        

        try:
            parts = list()
            if len(value_str) > 0:
                parts = [getFloat(i) for i in value_str.split(',')]
            return parts
        except:
            pass
        

        return value_str

    
    def __set_settings_from_window__(self):

        for arg_name in self.color_settings:
            if arg_name in self.settingwidgets:
                self.settings[arg_name] = self.settingwidgets[arg_name].get()
        

        for arg_name in self.number_settings:
            if arg_name in self.settingwidgets:
                self.settings[arg_name] = getFloat(self.settingwidgets[arg_name].get())


        for arg_name in self.str_settings:
            if arg_name in self.settingwidgets:
                self.settings[arg_name] = self.settingwidgets[arg_name].get()
        

        for arg_name in self.choice_settings:
            if arg_name in self.settingwidgets:
                self.settings[arg_name] = self.settingwidgets[arg_name].get()
        

        for arg_name in self.array_settings:
            if arg_name in self.settingwidgets:
                value_str = self.settingwidgets[arg_name].get()
                self.settings[arg_name] = self.__parse_array_value__(value_str)
        

        if "args" not in self.settings:
            self.settings["args"] = {}
        
        for arg_name in self.args_settings:
            if arg_name in self.settingwidgets:
                self.settings["args"][arg_name] = getFloat(self.settingwidgets[arg_name].get())

        pass
    
    def __clear_settings__(self):

        for arg_name in self.color_settings:
            if arg_name in self.settingwidgets and arg_name in self.settings:
                widget = self.settingwidgets[arg_name]
                widget.delete(0, END)
                widget.insert(0, self.settings[arg_name])
        

        for arg_name in self.number_settings:
            if arg_name in self.settingwidgets and arg_name in self.settings:
                widget = self.settingwidgets[arg_name]
                widget.delete(0, END)
                widget.insert(0, str(self.settings[arg_name]))


        for arg_name in self.str_settings:
            if arg_name in self.settingwidgets and arg_name in self.settings:
                widget = self.settingwidgets[arg_name]
                widget.delete(0, END)
                widget.insert(0, str(self.settings[arg_name]))
        

        for arg_name in self.choice_settings:
            if arg_name in self.settingwidgets and arg_name in self.settings:
                widget = self.settingwidgets[arg_name]
                widget.set(self.settings[arg_name])
        

        for arg_name in self.array_settings:
            if arg_name in self.settingwidgets and arg_name in self.settings:
                widget = self.settingwidgets[arg_name]
                widget.delete(0, END)
                value = self.settings[arg_name]
                if type(value) == list:
                    widget.insert(0, ", ".join(str(v) for v in value))
                else:
                    widget.insert(0, str(value))
        

        for arg_name in self.args_settings:
            if arg_name in self.settingwidgets:
                widget = self.settingwidgets[arg_name]
                widget.delete(0, END)
                widget.insert(0, str(self.settings.get("args", {}).get(arg_name, 0)))

        pass
    
    def __return_from_window__(self):
        if self.window is None: return

        self.__set_settings_from_window__()
        self.window.destroy()
        self.window = None
        pass
    pass



if __name__ == "__main__":
    root = Tk()
    root.title("Главное окно")
    

    config = {
        "type": "explicit",
        "color": "black",
        "linestyle": "-",
        "linewidth": 2,
        "label": "x**2-a*x-b",
        "param": "x",
        "proj": "y",
        "range": [-14, 90],
        "dots": 2000,
        "args": {
            "a": 27,
            "b": 16
        },
        "points_x": [],
        "points_y": []
    }
    

    settings_win = SettingWindow(root)
    

    linestyle_options = ["-", "--", "-.", ":", "solid", "dashed", "dashdot", "dotted"]
    

    settings_win.setConfig(config,
                          color_settings=["color"],
                          number_settings=["linewidth", "dots"],
                          array_settings=["range"],
                          args_settings=["a", "b"],
                          choice_settings={"linestyle": linestyle_options})
    
    def show_settings():
        settings_win.createWindow("Настройки графика")

        updated_config = settings_win.getSettings()
        print("\nОбновленные настройки:")
        print(updated_config)
    
    Button(root, text="Открыть настройки", 
           command=show_settings,
           font=("Arial", 14),
           padx=20, pady=10).pack(pady=50)
    
    root.geometry("300x200")
    root.mainloop()