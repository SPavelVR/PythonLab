from tkinter import *
from tkinter import ttk

class BallSettings:
    def __init__(self, parent, on_ball_deleted):

        self.parent = parent
        self.on_ball_deleted = on_ball_deleted
        self.current_ball = None
        self.current_ball_index = -1
        
        self.settings_frame = Frame(parent, bg='#f0f0f0', width=300, relief=RAISED, bd=2)
        self.settings_frame.pack_propagate(False)
        

        self.title_label = Label(self.settings_frame, text="Настройки шара", font=("Arial", 12, "bold"), bg='#f0f0f0')
        self.title_label.pack(pady=10)
        
        # ID шара
        id_frame = Frame(self.settings_frame, bg='#f0f0f0')
        id_frame.pack(fill=X, padx=10, pady=5)
        id_label = Label(id_frame, text="ID шара:", width=10, anchor=W, bg='#f0f0f0')
        id_label.pack(side=LEFT)
        self.id_var = StringVar()
        self.id_entry = Entry(id_frame, textvariable=self.id_var, state='readonly', width=15)
        self.id_entry.pack(side=LEFT, padx=5)
        
        # Разделитель
        separator1 = Frame(self.settings_frame, height=2, bg='gray')
        separator1.pack(fill=X, padx=10, pady=5)
        
        # Цвет шара
        color_frame = Frame(self.settings_frame, bg='#f0f0f0')
        color_frame.pack(fill=X, padx=10, pady=5)
        color_label = Label(color_frame, text="Цвет:", width=10, anchor=W, bg='#f0f0f0')
        color_label.pack(side=LEFT)
        
        self.color_var = StringVar()
        self.color_combobox = ttk.Combobox(color_frame, 
                                           textvariable=self.color_var, 
                                           values=['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'cyan'],
                                           width=13)
        self.color_combobox.pack(side=LEFT, padx=5)
        
        # Разделитель
        separator_radius = Frame(self.settings_frame, height=2, bg='gray')
        separator_radius.pack(fill=X, padx=10, pady=5)
        
        # Радиус шара
        radius_frame = Frame(self.settings_frame, bg='#f0f0f0')
        radius_frame.pack(fill=X, padx=10, pady=5)
        radius_label = Label(radius_frame, text="Радиус:", width=10, anchor=W, bg='#f0f0f0')
        radius_label.pack(side=LEFT)
        self.radius_var = StringVar()
        self.radius_entry = Entry(radius_frame, textvariable=self.radius_var, width=15)
        self.radius_entry.pack(side=LEFT, padx=5)
        
        # Разделитель
        separator_speed = Frame(self.settings_frame, height=2, bg='gray')
        separator_speed.pack(fill=X, padx=10, pady=5)
        
        # Настройка скорости
        speed_title = Label(self.settings_frame, text="Настройка скорости", 
                           font=("Arial", 10, "bold"), bg='#f0f0f0')
        speed_title.pack(anchor=W, padx=10, pady=(5,0))
        
        # Скорость по X
        vx_frame = Frame(self.settings_frame, bg='#f0f0f0')
        vx_frame.pack(fill=X, padx=10, pady=5)
        vx_label = Label(vx_frame, text="Скорость X:", width=10, anchor=W, bg='#f0f0f0')
        vx_label.pack(side=LEFT)
        self.vx_var = StringVar()
        self.vx_entry = Entry(vx_frame, textvariable=self.vx_var, width=15)
        self.vx_entry.pack(side=LEFT, padx=5)
        
        # Скорость по Y
        vy_frame = Frame(self.settings_frame, bg='#f0f0f0')
        vy_frame.pack(fill=X, padx=10, pady=5)
        vy_label = Label(vy_frame, text="Скорость Y:", width=10, anchor=W, bg='#f0f0f0')
        vy_label.pack(side=LEFT)
        self.vy_var = StringVar()
        self.vy_entry = Entry(vy_frame, textvariable=self.vy_var, width=15)
        self.vy_entry.pack(side=LEFT, padx=5)
        
        # Разделитель
        separator_freeze = Frame(self.settings_frame, height=2, bg='gray')
        separator_freeze.pack(fill=X, padx=10, pady=5)
        
        # Режим заморозки (Freezemode)
        freezemode_frame = Frame(self.settings_frame, bg='#f0f0f0')
        freezemode_frame.pack(fill=X, padx=10, pady=5)
        self.freezemode_var = BooleanVar()
        self.freezemode_checkbox = Checkbutton(
            freezemode_frame, 
            text="Режим заморозки (Freeze Mode)", 
            variable=self.freezemode_var,
            bg='#f0f0f0',
            command=self.on_freezemode_changed
        )
        self.freezemode_checkbox.pack(anchor=W)
        
        # Разделитель
        separator_buttons = Frame(self.settings_frame, height=2, bg='gray')
        separator_buttons.pack(fill=X, padx=10, pady=5)
        
        # ============== КНОПКИ ======================

        self.apply_btn = Button(self.settings_frame, text="Применить изменения", command=self.apply_settings, bg="#4CAF50", fg="white")
        self.apply_btn.pack(pady=5, padx=10, fill=X)
        

        self.delete_btn = Button(self.settings_frame, text="Удалить шар", command=self.delete_ball, bg="#f44336", fg="white")
        self.delete_btn.pack(pady=5, padx=10, fill=X)
        

        self.close_btn = Button(self.settings_frame, text="Закрыть", command=self.hide, bg="#9e9e9e", fg="white")
        self.close_btn.pack(pady=5, padx=10, fill=X)
        

        self.hide()
        pass
    
    # Показывает панель настроек для выбранного шара
    def show(self, ball, ball_index):

        self.current_ball = ball
        self.current_ball_index = ball_index
        
        self.id_var.set(f"Шар #{ball_index + 1}")
        self.color_var.set(ball.get_color() if hasattr(ball, 'get_color') else ball.color)
        self.radius_var.set(f"{ball.radius:.1f}")
        self.vx_var.set(f"{ball.vx:.2f}")
        self.vy_var.set(f"{ball.vy:.2f}")
        self.freezemode_var.set(ball.freezemode)
        
        self.settings_frame.pack(side=RIGHT, fill=Y, padx=(0, 0))
        pass

    # Скрывает панель настроек
    def hide(self):
        
        self.settings_frame.pack_forget()
        self.current_ball = None
        self.current_ball_index = -1

        pass
    
    # Обработчик изменения режима заморозки (немедленное применение)
    def on_freezemode_changed(self):

        if self.current_ball:
            self.current_ball.freezemode = self.freezemode_var.get()
            if self.current_ball.freezemode:
                self.current_ball.vx = 0
                self.current_ball.vy = 0
                pass
            pass
        pass
    

    def delete_ball(self):

        if self.current_ball and self.current_ball_index >= 0:

            self.on_ball_deleted(self.current_ball_index)
            self.hide()

            pass
        pass
                
    # Применяет настройки к текущему шару
    def apply_settings(self):

        if self.current_ball:
            changes = {}
            
            new_color = self.color_var.get()
            if new_color and hasattr(self.current_ball, 'set_color'):
                self.current_ball.set_color(new_color)
                changes['color'] = new_color
            elif new_color:
                self.current_ball.color = new_color
                changes['color'] = new_color
            

            try:
                new_radius = float(self.radius_var.get())
                if new_radius >= 10:
                    old_radius = self.current_ball.radius
                    self.current_ball.update_radius(new_radius)
                    changes['radius'] = new_radius
            except ValueError:
                print(f"Ошибка: некорректное значение радиуса: {self.radius_var.get()}")
            

            try:
                new_vx = float(self.vx_var.get())
                self.current_ball.vx = new_vx
                changes['vx'] = new_vx
            except ValueError:
                print(f"Ошибка: некорректное значение скорости X: {self.vx_var.get()}")
            

            try:
                new_vy = float(self.vy_var.get())
                self.current_ball.vy = new_vy
                changes['vy'] = new_vy
            except ValueError:
                print(f"Ошибка: некорректное значение скорости Y: {self.vy_var.get()}")
            

            changes['freezemode'] = self.current_ball.freezemode
            

            self.id_var.set(f"Шар #{self.current_ball_index + 1}")
            

            self.hide()
            pass
        pass
    pass
