from tkinter import messagebox


messagebox.showinfo("Информация", "Это информационное сообщение")
messagebox.showwarning("Предупреждение", "Это предупреждение")
messagebox.showerror("Ошибка", "Это сообщение об ошибке")

result = messagebox.askquestion("Вопрос", "Это вопрос (Yes/No)")
print(f"askquestion: {result}")

result = messagebox.askokcancel("Подтверждение", "Нажмите OK для продолжения")
print(f"askokcancel: {result}")

result = messagebox.askretrycancel("Повтор", "Попробовать снова?")
print(f"askretrycancel: {result}")

result = messagebox.askyesno("Да/Нет", "Выберите Да или Нет")
print(f"askyesno: {result}")

result = messagebox.askyesnocancel("Да/Нет/Отмена", "Выберите вариант")
print(f"askyesnocancel: {result}")