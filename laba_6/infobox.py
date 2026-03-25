from tkinter import messagebox


class MessageError:


    label_sc: str
    label_err: str

    text_sc: str
    list_text_err: list


    def __init__(self, label_sc="Успешное выполнение", label_err="Ошибка"):
        self.label_sc = label_sc
        self.label_err = label_err

        self.text_sc = ""
        self.list_text_err = list()
        pass

    def appendErrorText(self, errMessage: str):
        self.list_text_err.append(errMessage)
        pass

    def clearErrorText(self):
        self.list_text_err.clear()
        pass

    def haveError(self):
        return len(self.list_text_err) > 0
    

    def __call__(self, *args, **kwds):

        count = len(self.list_text_err)

        if count:
            message = f"Обнаружена {count} ошибок(-ки):\n" + "\n".join(self.list_text_err)
            messagebox.showerror(self.label_err, message)
            self.clearErrorText()
        elif kwds.get("showSuccess", True):
            messagebox.showinfo(self.label_sc, self.text_sc)

        pass

    pass



if __name__ == "__main__":

    mess = MessageError(label_err="Плохая связь с сервером")

    mess()

    mess.appendErrorText("Не установлена связь с сервером")
    mess.appendErrorText("Не установлена связь с сервером")
    mess.appendErrorText("Не установлена связь с сервером")

    mess()

    mess(showSuccess=False)

    import numpy as np


    arr = np.linspace(-5, 20, 100)

    arrc = np.cos(arr) * arr
    print(arr)
    print("End")

    pass