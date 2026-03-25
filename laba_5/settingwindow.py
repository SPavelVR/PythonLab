from tkinter import *

"""

?label: str - имя окна
?relative: bool - значения координат изначальное относительные (по умл. False)
?enableCheckbutton: bool - вкл. флажок для управления режимом координат (по умл. True)
args: list - массив аргументов
    type: str - тип аргумента {"str", "int", "posint", "negint", "cords", "scale"}
    name: str - текст аргумента
    basearg: any - базовое значение
    ?minarg: int - минимальное значение для scale
    ?maxarg: int - максимальное значение для scale
    ?exis: str   - ось {"x", "y"}
    

"""

def validateInt(text: str):
    if text == "" or text == "-": return True

    try:
        float(text)
        return True
    except:
        return False
    pass   

def validatePosint(text: str):
    if text == "": return True

    try:
        return (float(text) >= 0)
    except:
        return False
    pass

def validateNegint(text: str):
    if text == "" or text == "-": return True

    try:
        return (float(text) <= 0)
    except:
        return False
    pass

def getFloat(text: str):
    if text == "" or text == "-": return 0.0
    return float(text)



class SettingWindow:

    root: Tk            = None 
    window: Toplevel    = None
    canvas: Canvas      = None

    settingmodels: list
    settings: list
    settingindex: int
    settingwidget: list

    relativeCord: IntVar


    def __init__(self, root):

        self.root = root
        
        self.settingmodels  = list()
        self.settings       = list()
        self.settingwidget  = list()
        self.settingindex   = 0

        self.relativeCord   = IntVar()
        self.relativeCord.set(0)

        self.__registor_int__       = (root.register(validateInt), '%P')
        self.__registor_posint__    = (root.register(validatePosint), '%P')
        self.__registor_negint__    = (root.register(validateNegint), '%P')

        pass

    def setCanvas(self, canvas: Canvas):
        self.canvas = canvas
        pass
    
    def __set_size_settings__(self, size: int):
        if len(self.settings) < size:
            self.settings       = [0] * size
            self.settingwidget  = [0] * size
            pass
        pass

    def appendModel(self, model: list | dict):

        if type(model) == list:
            for i in model:
                self.settingmodels.append(i.copy())
                self.__set_size_settings__(len(i.get("args", "")))
                pass
            return

        self.settingmodels.append(model.copy())
        self.__set_size_settings__(len(model.get("args", "")))

        pass
    
    def setIndexModel(self, index: int):
        if index == self.settingindex: return

        self.settingindex = max(0, min(len(self.settingmodels) - 1, index))
        self.setBaseArgs()
        pass

    def setBaseArgs(self):

        model: dict = self.settingmodels[self.settingindex]
        index: int  = 0
        temp: float
        for arg in model.get("args", ""):
            temp = arg["basearg"]
            if arg["type"] == "cord" and model.get("relative", False) and self.canvas:
                if arg.get("exis") == "x":
                    temp = temp * self.canvas.winfo_width()
                else:
                    temp = temp * self.canvas.winfo_height()
                pass 

            self.settings[index] = temp

            index += 1
            pass
        
        pass

    def getSettings(self):
        size: int = len(self.settingmodels[self.settingindex].get("args", ""))
        return self.settings[0:size]
    

    def createWindow(self):

        self.window = Toplevel(self.root)
        self.window.title(self.settingmodels[self.settingindex].get("label", "Настройки"))

        # Делет основное окно не активном
        self.window.transient(self.root)
        self.window.grab_set()

        self.__create_widget__()

        self.root.wait_window(self.window)

        pass


    
    def __create_widget__(self):

        model: dict = self.settingmodels[self.settingindex]
        args: list = model.get("args", [])

        settingFrame = Frame(self.window)
        buttonFrame  = Frame(self.window)

        settingFrame.pack(fill=BOTH, expand=1)
        buttonFrame.pack(fill=BOTH, expand=1)

        index = 0

        for arg in args:

            label = Label(settingFrame, text=arg["name"], font=("Arial", 10))
            widget = None

            if arg["type"] == "scale":
                widget = Scale(settingFrame, orient=HORIZONTAL, length=arg.get("length", 200), from_=arg.get("minarg", 0), to=arg.get("maxarg", 10), tickinterval=1, resolution=1, font=("Arial", 10))
                widget.set(self.settings[index])
            elif arg["type"] == "int" or arg["type"] == "cord":
                widget = Entry(settingFrame, font=("Arial", 10), validate="key", validatecommand=self.__registor_int__)
                widget.delete(0, END)
                if arg["type"] != "cord" or self.relativeCord == 0:
                    widget.insert(0, str(self.settings[index]))
                elif self.canvas:
                    if arg.get("exis", False) == "x": 
                        widget.insert(0, str(self.settings[index] / self.canvas.winfo_width()))
                    else:
                        widget.insert(0, str(self.settings[index] / self.canvas.winfo_height()))
                else:
                    widget.insert(0, str(0.0))
            elif arg["type"] == "posint":
                widget = Entry(settingFrame, font=("Arial", 10), validate="key", validatecommand=self.__registor_posint__)
                widget.delete(0, END)
                widget.insert(0, str(self.settings[index]))
            else:
                pass


            label.grid(row=index, column=0, pady=5, padx=5, sticky="w")
            if widget != None:
                widget.grid(row=index, column=1, pady=5, sticky="w")
                self.settingwidget[index] = widget
            
            index += 1
            pass


        Button(buttonFrame, text="Применить значения", 
                            command=self.__return_from_window__,
                            font=("Arial", 14, "bold"),
                            bg="#A70347", fg="white",
                            padx=20, pady=8).grid(row=0, column=0, pady=5, padx=5, sticky="w")
        Button(buttonFrame, text="Стереть значения", 
                            command=self.__clear_settings__,
                            font=("Arial", 14, "bold"),
                            bg="#03A75A", fg="white",
                            padx=20, pady=8).grid(row=0, column=1, pady=5, padx=5, sticky="w")
        if model.get("enableCheckbutton", 1):
            Checkbutton( buttonFrame, text="Относительные координаты",
                            variable=self.relativeCord,
                            onvalue=1,
                            offvalue=0,
                            selectcolor="black",

                            relief=RAISED,
                            bd=3,
                            bg="#6EA703", fg="white",
                            font=("Arial", 14, "bold"),
                            padx=20, pady=8).grid(row=0, column=2, pady=5, padx=5, sticky="w")
            
            if self.settingmodels[self.settingindex].get("relative", False):
                self.relativeCord.set(1)
            pass
        pass
    
    def __set_settings_from_window__(self):
        model = self.settingmodels[self.settingindex]
        args = model["args"]
        temp: int
        for i in range(0, len(args)):
            temp = getFloat(self.settingwidget[i].get())
            if args[i]["type"] == "cord" and self.relativeCord.get() and self.canvas:
                if args[i].get("exis") == "x":
                    temp = temp * self.canvas.winfo_width()
                else:
                    temp = temp * self.canvas.winfo_height()
                pass 

            self.settings[i] = temp
            pass
        pass

    def __clear_settings__(self):
        model = self.settingmodels[self.settingindex]
        args = model["args"]
        for i in range(0, len(args)):
            if args[i]["type"] == "scale":
                self.settingwidget[i].set(args[i].get("basearg", 0))
            else:
                self.settingwidget[i].delete(0, END)
                self.settingwidget[i].insert(0, str(args[i].get("basearg", 0)))
            pass
        pass
    
    def __return_from_window__(self):

        self.__set_settings_from_window__()
        self.window.destroy()

        self.window = None

        self.relativeCord.set(0)

        pass
    pass




if __name__ == "__main__":

    root = Tk()
    setting = SettingWindow(root)
    
    canvas = Canvas(root, width=400, height=400)
    canvas.create_rectangle(0,0, 400, 400, outline='#fff', fill = '#fff') 
    canvas.pack(fill=BOTH, expand=1)

    setting.setCanvas(canvas)

    setting.appendModel(
        {
            "label": "Test",
            "relative": 1,
            "args": [
                {
                    "type": "scale",
                    "name": "Скаляр",
                    "basearg": 0,
                    "minarg": 0,
                    "maxarg": 10
                },
                {
                    "type": "cord",
                    "name": "X1",
                    "axis": "x",
                    "basearg": 0
                },
                {
                    "type": "int",
                    "name": "Число",
                    "basearg": 0
                }
            ]
        }
    )
    setting.appendModel(
        {
            "label": "Test",
            "args": [
                {
                    "type": "scale",
                    "name": "Скаляр",
                    "basearg": 0,
                    "minarg": 0,
                    "maxarg": 10
                },
                {
                    "type": "cord",
                    "name": "X1",
                    "axis": "x",
                    "basearg": 0
                },
                {
                    "type": "int",
                    "name": "Число",
                    "basearg": 0
                },
                {
                    "type": "int",
                    "name": "Число",
                    "basearg": 0
                },
                {
                    "type": "int",
                    "name": "Число",
                    "basearg": 0
                },
                {
                    "type": "int",
                    "name": "Число",
                    "basearg": 0
                }
            ]
        }
    )

    setting.createWindow()

    def chsadasd():
        print(setting.getSettings())
        pass

    Button(root, text="Guga", 
                            command=chsadasd,
                            font=("Arial", 14, "bold"),
                            bg="#A70347", fg="white",
                            padx=20, pady=8).pack(fill=BOTH, expand=1)

    root.mainloop()


