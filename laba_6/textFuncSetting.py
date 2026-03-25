from tkinter import filedialog, ttk, scrolledtext
import tkinter as tk

import CompileGraf
import grafFuncSetting


class ConsoleGraf:
    def __init__(self, root, graf: grafFuncSetting.GrafBox=None):

        self.mainFrame = ttk.Frame(root)
        self.graf = graf

        self.__create_widget__()
        pass

    def pack(self):
        self.mainFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        pass

    def unpack(self):
        self.mainFrame.pack_forget()
        pass


    def __create_widget__(self):

        self.textFrame  = ttk.Frame(self.mainFrame)
        self.text       = scrolledtext.ScrolledText(self.textFrame, wrap=tk.CHAR, font=("Courier", 10), height=30, width=30)

        self.textFrame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        pass

    def __clear__(self):
        self.text.delete("1.0", tk.END)
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
                
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", content)

            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
        pass



    def __save__(self):
        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            try:
                content = self.text.get("1.0", tk.END)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.current_file = file_path
                
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")
        pass

    def __compile__(self):
        content = self.text.get("1.0", tk.END)

        if len(content) == 0: return;

        res = CompileGraf.compilegraf(content)

        if not self.graf is None:
            self.graf.append(res)
        pass
    pass


