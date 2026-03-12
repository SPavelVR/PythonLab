import tkinter as tk
from tkinter import ttk

class Form:

    __file_name__: str    = None
    __lkeys__: list       = ("name", "surname", "university", "position", "country", "letter")
    __lboundkeys__: list  = ("name", "surname", "university", "position", "country")
    __luniversity__: list = ("ССАУ", "МГУ", "СПбГУ", "МФТИ", "ВШЭ", "МГТУ", "Другой")
    __lcountry__: list    = ("Россия", "Казахстан", "Беларусь", "Китай", "США", "Другая")
    __lposition__: list   = ("Студент","Аспирант","Младший научный сотрудник","Старший научный сотрудник","Профессор","Доцент","Другое")

    __entries__: dict           = None
    __labels__: dict            = None
    __text1__: dict             = None
    __text2__: dict             = None
    __values__: dict            = None

    def __init__(self, root):

        if root == None:
            print("Root must be inilize")
            exit()
            pass

        self.root = root

        self.__entries__    = dict()
        self.__labels__     = dict()
        self.__text1__      = dict()
        self.__text2__      = dict()
        self.__values__     = dict()

        pass

    # Проверка обязательных условий 
    def __isCondition__(self)->bool:

        if len(self.__values__) == 0: return False

        for key in self.__lboundkeys__:
            if not isWord(self.__values__.get(key, "")): return False
        
        return True
        pass
    
    # Установка параметров условий через внешний словарь
    def setFromDict(self, args: dict):

        self.__values__["name"]         = args.get("name", "")
        self.__values__["surname"]      = args.get("surname", "")
        self.__values__["position"]     = args.get("position", self.__lposition__[0])
        self.__values__["country"]      = args.get("country", self.__lcountry__[0])
        self.__values__["university"]   = args.get("university", self.__luniversity__[0])
        self.__values__["letter"]       = args.get("letter", "")

        self.__set_data__()
        pass

    def setFileName(self, fname: str):

        self.__file_name__ = fname

        pass

    # Передача условий в виде словаря
    # Условие letter не запишется, если не заполнина
    def __get_dict__(self)->dict:

        res: dict = dict()

        for key, value in self.__values__.items():
            if len(value) == 0: continue

            res[key] = value
            pass

        return res
        pass

    # Передача условий в виде текста
    def __str__(self)->str:

        if self.__isCondition__():
            d = self.__get_dict__()
            return str(d).replace("\'", "\"")
        
        return str("no valid data")
        pass
    
    def __copy_data__(self)->bool:

        self.__clear_effects__()

        for key in self.__lkeys__:
            if key == "letter":
                self.__values__[key] = self.__entries__[key].get("1.0", "end-1c")
                continue

            if key in self.__lboundkeys__ and not isWord(self.__entries__[key].get()):
                self.__text1__[key].config(fg = "red")
                pass
    
            self.__values__[key] = self.__entries__[key].get()
            pass
        
        self.__set_data__()

        pass

    def __set_data__(self):

        if not self.__isCondition__():
            return False
        
        for key in self.__lkeys__:
            self.__labels__[key]["text"] = self.__values__[key]
            pass

        pass


    def __save_to_file__(self)->bool:

        if type(self.__file_name__) != str or len(self.__file_name__) == 0 or not self.__isCondition__(): return False

        with open(self.__file_name__, "w", encoding="utf-8") as file:
            file.write(str(self))
            pass
        pass

    def __clear_all__(self):

        for key in self.__lkeys__:
            self.__labels__[key]["text"] = ""
            self.__values__[key] = ""
            pass

        pass

    def __clear_effects__(self):

        if len(self.__entries__) == 0: return

        for key in self.__lboundkeys__:
            self.__text1__[key].config(fg = "black")
            pass
        pass

    # Супер функция по созданию формы
    def createForm(self):
        
        # Заголовок
        title_label = tk.Label(self.root, text="РЕГИСТРАЦИОННАЯ КАРТОЧКА КОНФЕРЕНЦИИ", font=("Arial", 16, "bold"), fg="blue")
        title_label.pack(pady=10)
        
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # ========== ПЕРВАЯ КАРТОЧКА ==========

        card1_frame = tk.LabelFrame(main_frame, text="Карточка 1 (заполнить)", font=("Arial", 12, "bold"), padx=10, pady=10)
        card1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Имя
        self.__text1__["name"] = tk.Label(card1_frame, text="Имя:", font=("Arial", 10))
        self.__text1__["name"].grid(row=0, column=0, sticky="w", pady=5)

        name_entry = tk.Entry(card1_frame, width=25, font=("Arial", 10))
        name_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.__entries__["name"] = name_entry
        

        # Фамилия
        self.__text1__["surname"] = tk.Label(card1_frame, text="Фамилия:", font=("Arial", 10))
        self.__text1__["surname"].grid(row=1, column=0, sticky="w", pady=5)

        surname_entry = tk.Entry(card1_frame, width=25, font=("Arial", 10))
        surname_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.__entries__["surname"] = surname_entry
        

        # Университет (выпадающий список)
        self.__text1__["university"] = tk.Label(card1_frame, text="Университет:", font=("Arial", 10))
        self.__text1__["university"].grid(row=2, column=0, sticky="w", pady=5)

        """
        listbox_frame = tk.Frame(card1_frame)
        listbox_frame.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        temp_listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            height=5,
            exportselection=False)

        temp_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=temp_listbox.yview)

        for item in self.__luniversity__:
            temp_listbox.insert(tk.END, item)
            pass

        temp_listbox.selection_set(0)
        temp_listbox.activate(0)

        self.__entries__["university"] = temp_listbox
        """

        temp_listbox = ttk.Combobox(card1_frame, values=self.__luniversity__, width=23, font=("Arial", 10))
        temp_listbox.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        temp_listbox.set(self.__luniversity__[0])
        self.__entries__["university"] = temp_listbox

        
        # Должность (выпадающий список)
        self.__text1__["position"] = tk.Label(card1_frame, text="Должность:", font=("Arial", 10))
        self.__text1__["position"].grid(row=3, column=0, sticky="w", pady=5)

        temp_listbox = ttk.Combobox(card1_frame, values=self.__lposition__, width=23, font=("Arial", 10))
        temp_listbox.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        temp_listbox.set(self.__lposition__[0])
        self.__entries__["position"] = temp_listbox
        
        # Страна (выпадающий список)
        self.__text1__["country"] = tk.Label(card1_frame, text="Страна:", font=("Arial", 10))
        self.__text1__["country"].grid(row=4, column=0, sticky="w", pady=5)

        temp_listbox = ttk.Combobox(card1_frame, values=self.__lcountry__, width=23, font=("Arial", 10))
        temp_listbox.grid(row=4, column=1, pady=5, padx=5, sticky="w")
        temp_listbox.set(self.__lcountry__[0])
        self.__entries__["country"] = temp_listbox

        # Письмо
        self.__text1__["letter"] = tk.Label(card1_frame, text="Письмо:", font=("Arial", 10))
        self.__text1__["letter"].grid(row=5, column=0, sticky="w", pady=5)

        letter_text = tk.Text(card1_frame, width=23, height=5, wrap="char")
        letter_text.grid(row=5, column=1, pady=5, padx=5, sticky="w")
        self.__entries__["letter"] = letter_text

        # ========== ВТОРАЯ КАРТОЧКА ==========
        card2_frame = tk.LabelFrame(main_frame, text="Карточка 2 (копия)", font=("Arial", 12, "bold"), padx=10, pady=10)
        card2_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Имя (копия)
        self.__text2__["name"] = tk.Label(card2_frame, text="Имя:", font=("Arial", 10))
        self.__text2__["name"].grid(row=0, column=0, sticky="w", pady=5)

        name_label2 = tk.Label(card2_frame, text="", font=("Arial", 10), width=23, anchor="w", relief=tk.SUNKEN)
        name_label2.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.__labels__["name"] = name_label2
        
        # Фамилия (копия)
        self.__text2__["surname"] = tk.Label(card2_frame, text="Фамилия:", font=("Arial", 10))
        self.__text2__["surname"].grid(row=1, column=0, sticky="w", pady=5)

        surname_label2 = tk.Label(card2_frame, text="", font=("Arial", 10), width=23, anchor="w", relief=tk.SUNKEN)
        surname_label2.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.__labels__["surname"] = surname_label2
        
        # Университет (копия)
        self.__text2__["university"] = tk.Label(card2_frame, text="Университет:", font=("Arial", 10))
        self.__text2__["university"].grid(row=2, column=0, sticky="w", pady=5)

        university_label2 = tk.Label(card2_frame, text="", font=("Arial", 10), width=23, anchor="w", relief=tk.SUNKEN)
        university_label2.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        self.__labels__["university"] = university_label2
        
        # Должность (копия)
        self.__text2__["position"] = tk.Label(card2_frame, text="Должность:", font=("Arial", 10))
        self.__text2__["position"].grid(row=3, column=0, sticky="w", pady=5)

        position_label2 = tk.Label(card2_frame, text="", font=("Arial", 10), width=23, anchor="w", relief=tk.SUNKEN)
        position_label2.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        self.__labels__["position"] = position_label2
        
        # Страна (копия)
        self.__text2__["country"] = tk.Label(card2_frame, text="Страна:", font=("Arial", 10))
        self.__text2__["country"].grid(row=4, column=0, sticky="w", pady=5)

        country_label2 = tk.Label(card2_frame, text="", font=("Arial", 10), width=23, anchor="w", relief=tk.SUNKEN)
        country_label2.grid(row=4, column=1, pady=5, padx=5, sticky="w")
        self.__labels__["country"] = country_label2

        # Имя (копия)
        self.__text2__["letter"] = tk.Label(card2_frame, text="Письмо:", font=("Arial", 10))
        self.__text2__["letter"].grid(row=5, column=0, sticky="w", pady=5)

        name_label2 = tk.Message(card2_frame, text="", font=("Arial", 10), width=250, anchor="w", relief=tk.SUNKEN)
        name_label2.grid(row=5, column=1, pady=5, padx=5, sticky="w")
        self.__labels__["letter"] = name_label2


        # ========== КНОПКИ УПРАВЛЕНИЯ ==========
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Кнопка копирования
        copy_btn = tk.Button(button_frame, text="Копировать данные во вторую карточку", 
                            command=self.__copy_data__,
                            font=("Arial", 11, "bold"),
                            bg="#4CAF50", fg="white",
                            padx=20, pady=8)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка сохранения в файл
        save_btn = tk.Button(button_frame, text="Сохранить в файл", 
                            command=self.__save_to_file__,
                            font=("Arial", 11, "bold"),
                            bg="#2196F3", fg="white",
                            padx=20, pady=8)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка очистки
        clear_btn = tk.Button(button_frame, text="Очистить все", 
                             command=self.__clear_all__,
                             font=("Arial", 11, "bold"),
                             bg="#FF5722", fg="white",
                             padx=20, pady=8)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Информационная строка
        info_label = tk.Label(self.root, 
                              text="Заполните первую карточку и нажмите кнопку копирования",
                              font=("Arial", 9, "italic"),
                              fg="gray")
        info_label.pack(pady=5)

        pass

    pass


def isWord(text: str)->bool:

    if type(text) != str or len(text) == 0 or not text[0].isalpha(): 
        return False

    return True
    pass

if __name__ == "__main__":

    root = tk.Tk()
    fr = Form(root)
    fr.setFileName("Resultat.json")

    fr.createForm()
    root.mainloop()
    pass