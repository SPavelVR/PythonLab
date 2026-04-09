from tkinter import *
from tkinter import ttk, filedialog, messagebox
from ball import Ball
from ball_settings import BallSettings
from save_load import *
import random

runMotion = False
runAll = True
getData = False
grabbed_ball_index = -1     # Индекс захваченного шара (-1 значит ничего не захвачено)
balls = []                  # Массив для хранения шаров
cw = 800                    # Текущая ширина холста
ch = 640                    # Текущая высота холста


def StartStop():
    global runMotion
    runMotion = not runMotion
    if runMotion:
        startBtn['text'] = "Пауза"
    else:
        startBtn['text'] = "Старт"
    
def StopAll():
    global runAll
    runAll = False

# Ищет шар на который указывает мышь
def GrabBall(event):
    global runMotion, grabbed_ball_index, balls
    if not runMotion:

        for i, ball in enumerate(balls):
            if ball.is_point_inside(event.x, event.y):
                ball.grab_ball()
                grabbed_ball_index = i

                settings_panel.show(ball, i)
                break
        
def ReleaseBall(event):
    global grabbed_ball_index, balls
    if grabbed_ball_index != -1:
        balls[grabbed_ball_index].release_ball()
        grabbed_ball_index = -1
    
def DragBall(event):
    global grabbed_ball_index, balls
    if grabbed_ball_index != -1:
        balls[grabbed_ball_index].drag_ball(event.x, event.y)
        
def ReadData(*arg):
    global getData
    getData = True
    
def UpdateAllBalls():
    global balls, getData
    try:
        new_g = float(gEnt.get())
        new_wind = float(windEnt.get())
        
        for ball in balls:
            ball.update_acceleration(new_g)
            ball.update_wind(new_wind)
        
        gEnt.delete(0, 'end')
        gEnt.insert(0, '{:.3f}'.format(new_g))
        windEnt.delete(0, 'end')
        windEnt.insert(0, '{:.3f}'.format(new_wind))
    except ValueError:
        if balls:
            gEnt.delete(0, 'end')
            gEnt.insert(0, '{:.3f}'.format(balls[0].get_acceleration()))
            windEnt.delete(0, 'end')
            windEnt.insert(0, '{:.3f}'.format(balls[0].get_wind()))
    
    getData = False
    pass

def UpdateCanvasSize():
    global cw, ch, balls
    
    try:
        new_width = int(widthEnt.get())
        new_height = int(heightEnt.get())
        
        if new_width < 200:
            new_width = 200
        if new_height < 200:
            new_height = 200
            
        cw = new_width
        ch = new_height
        

        cnv.config(width=cw, height=ch)
        
        for ball in balls:
            ball_radius = ball.get_radius()
            x, y = ball.get_position()
            
            if x + ball_radius > cw:
                ball.x = cw - ball_radius
            elif x - ball_radius < 0:
                ball.x = ball_radius
                
            if y + ball_radius > ch:
                ball.y = ch - ball_radius
            elif y - ball_radius < 0:
                ball.y = ball_radius
        
        widthEnt.delete(0, 'end')
        widthEnt.insert(0, str(cw))
        heightEnt.delete(0, 'end')
        heightEnt.insert(0, str(ch))
        
        pass
        
    except ValueError:
        widthEnt.delete(0, 'end')
        widthEnt.insert(0, str(cw))
        heightEnt.delete(0, 'end')
        heightEnt.insert(0, str(ch))

    pass

# Добавляет новый шар со случайными параметрами через словарь конфигурации"
def AddBall():
    global cw, ch

    radius = random.randint(20, 50)
    
    config = {
        'x':            random.randint(radius + 10, cw - radius - 10),
        'y':            random.randint(radius + 10, ch - radius - 10),
        'radius':       radius,
        'color':        random.choice(['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'cyan']),
        'vx':           random.uniform(-8, 8),
        'vy':           random.uniform(-10, 5),
        'ay':           0.1,
        'wind':         random.uniform(0.01, 0.05),
        'mass':         radius / 10,
        'freezemode':   False
    }
    
    new_ball = Ball(cnv, config)
    balls.append(new_ball)
    
    ballCountLbl.config(text=f"Шаров: {len(balls)}")
    pass

# Удаляет последний добавленный шар
def RemoveBall():
    global balls, grabbed_ball_index

    if balls:
        removed_ball = balls.pop()
        ballCountLbl.config(text=f"Шаров: {len(balls)}")
        
        if grabbed_ball_index >= len(balls):
            grabbed_ball_index = -1

# Сбрасывает скорость всех шаров
def ResetBallsVelocity():
    global balls
    for ball in balls:
        ball.vx = 0
        ball.vy = 0
    pass

# Удаляет шар по индексу (вызывается из настроек)
def DeleteBallFromSettings(ball_index):
    global balls, grabbed_ball_index
    
    if 0 <= ball_index < len(balls):
        removed_ball = balls.pop(ball_index)
        print(f"Удален шар #{ball_index + 1}. Осталось шаров: {len(balls)}")
        
        ballCountLbl.config(text=f"Шаров: {len(balls)}")
        
        if grabbed_ball_index == ball_index:
            grabbed_ball_index = -1
        elif grabbed_ball_index > ball_index:
            grabbed_ball_index -= 1
        
        settings_panel.hide()
        pass
    pass
            

# Проверяет столкновения между всеми парами шаров
def CheckAllCollisions():
    global balls
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].check_collision(balls[j])
    pass

# ========== ФУНКЦИИ СОХРАНЕНИЯ И ЗАГРУЗКИ ==========

# Сохраняет текущее состояние игры
def SaveGame():
    global balls, cw, ch
    
    canvas_settings = {
        'width': cw,
        'height': ch
    }
    
    screen_settings = {
        'g': float(gEnt.get()) if gEnt.get() else 0.1,
        'wind': float(windEnt.get()) if windEnt.get() else 0.0
    }
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".bc",
        filetypes=[("Ball Config files", "*.bc"), ("All files", "*.*")],
        title="Сохранить состояние"
    )
    
    if filename:
        result = save_state(filename, balls, canvas_settings, screen_settings)
        if result['success']:
            messagebox.showinfo("Успех", result['message'])
        else:
            messagebox.showerror("Ошибка", result['message'])
    pass

def LoadGame():
    global balls, cw, ch, gEnt, windEnt, widthEnt, heightEnt, ballCountLbl
    
    filename = filedialog.askopenfilename(
        defaultextension=".bc",
        filetypes=[("Ball Config files", "*.bc"), ("All files", "*.*")],
        title="Загрузить состояние"
    )
    
    if filename:
        def create_ball(config, canvas):
            return Ball(canvas, config)
        
        result = load_state(filename, create_ball, cnv, cw, ch)
        
        if result['success']:
            balls = result['balls']
            
            if result['canvas_settings']:
                new_cw = result['canvas_settings'].get('width', cw)
                new_ch = result['canvas_settings'].get('height', ch)
                
                if new_cw != cw or new_ch != ch:
                    cw = new_cw
                    ch = new_ch
                    cnv.config(width=cw, height=ch)
                    widthEnt.delete(0, 'end')
                    widthEnt.insert(0, str(cw))
                    heightEnt.delete(0, 'end')
                    heightEnt.insert(0, str(ch))
            
            if result['screen_settings']:
                g_value = result['screen_settings'].get('g', 0.1)
                wind_value = result['screen_settings'].get('wind', 0.0)
                
                gEnt.delete(0, 'end')
                gEnt.insert(0, '{:.3f}'.format(g_value))
                windEnt.delete(0, 'end')
                windEnt.insert(0, '{:.3f}'.format(wind_value))
                
                for ball in balls:
                    ball.update_acceleration(g_value)
                    ball.update_wind(wind_value)
            

            ballCountLbl.config(text=f"Шаров: {len(balls)}")
            
            messagebox.showinfo("Успех", result['message'])
        else:
            messagebox.showerror("Ошибка", result['message'])

# ========== СОЗДАНИЕ ГЛАВНОГО ОКНА ==========

root = Tk()
root.title("Шар с сохранением и загрузкой")
root.bind('<Return>', ReadData)

# ========== СОЗДАНИЕ MENU BAR ==========

menubar = Menu(root)
root.config(menu=menubar)

# Меню "Файл"
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Сохранить", command=SaveGame, accelerator="Ctrl+S")
file_menu.add_command(label="Загрузить", command=LoadGame, accelerator="Ctrl+O")
file_menu.add_separator()
file_menu.add_command(label="Выход", command=StopAll, accelerator="Ctrl+Q")

# Меню "Правка"
edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Правка", menu=edit_menu)
edit_menu.add_command(label="Добавить шар", command=AddBall, accelerator="Ctrl+A")
edit_menu.add_command(label="Удалить шар", command=RemoveBall, accelerator="Ctrl+D")
edit_menu.add_separator()
edit_menu.add_command(label="Сбросить скорость", command=ResetBallsVelocity, accelerator="Ctrl+R")

# Меню "Управление"
control_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Управление", menu=control_menu)
control_menu.add_command(label="Старт/Пауза", command=StartStop, accelerator="Space")

# ========== ОСНОВНОЙ КОНТЕЙНЕР ==========

main_container = Frame(root)
main_container.pack(expand=True, fill=BOTH)

# Создаем холст с начальными размерами
cnv = Canvas(main_container, width=cw, height=ch, background="white",  highlightbackground='black', highlightthickness=2)
cnv.pack(side=LEFT, expand=True, fill=BOTH)

cnv.bind('<Button-1>', GrabBall)
cnv.bind('<B1-Motion>', DragBall)
cnv.bind('<ButtonRelease-1>', ReleaseBall)

# Панель настроек (справа)
settings_panel = BallSettings(main_container, DeleteBallFromSettings)

# ========== ПАНЕЛЬ ИНСТРУМЕНТОВ ==========

toolbar = Frame(root, bg='lightgray', height=100, relief=RAISED, bd=2)
toolbar.pack(side=TOP, fill=X)
toolbar.pack_propagate(False)


inner_frame = Frame(toolbar, bg='lightgray')
inner_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)


addBallBtn = Button(inner_frame, text="+ Добавить шар", command=AddBall, bg="lightgreen", font=("Arial", 10))
addBallBtn.pack(side=LEFT, padx=5)


removeBallBtn = Button(inner_frame, text="- Удалить шар", command=RemoveBall, bg="lightcoral", font=("Arial", 10))
removeBallBtn.pack(side=LEFT, padx=5)


resetSpeedBtn = Button(inner_frame, text="Сброс скорости", command=ResetBallsVelocity, bg="#FF9800", fg="white", font=("Arial", 10))
resetSpeedBtn.pack(side=LEFT, padx=5)


separator1 = Frame(inner_frame, width=2, bg='gray')
separator1.pack(side=LEFT, padx=10, fill=Y)


startBtn = Button(inner_frame, text="Старт", command=StartStop, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
startBtn.pack(side=LEFT, padx=5)


separator2 = Frame(inner_frame, width=2, bg='gray')
separator2.pack(side=LEFT, padx=10, fill=Y)


ballCountLbl = Label(inner_frame, text="Шаров: 0", font=("Arial", 11, "bold"), bg='lightgray')
ballCountLbl.pack(side=LEFT, padx=10)


separator3 = Frame(inner_frame, width=2, bg='gray')
separator3.pack(side=LEFT, padx=10, fill=Y)


gLbl = Label(inner_frame, text="g:", font=("Arial", 10), bg='lightgray')
gLbl.pack(side=LEFT, padx=(5,2))
gEnt = Entry(inner_frame, bd=2, width=8, font=("Arial", 10))
gEnt.pack(side=LEFT, padx=(0,10))

windLbl = Label(inner_frame, text="Сопротивление:", font=("Arial", 10), bg='lightgray')
windLbl.pack(side=LEFT, padx=(5,2))
windEnt = Entry(inner_frame, bd=2, width=8, font=("Arial", 10))
windEnt.pack(side=LEFT, padx=(0,10))


separator4 = Frame(inner_frame, width=2, bg='gray')
separator4.pack(side=LEFT, padx=10, fill=Y)


canvasSizeFrame = Frame(inner_frame, bg='lightgray')
canvasSizeFrame.pack(side=LEFT, padx=5)

widthFrame = Frame(canvasSizeFrame, bg='lightgray')
widthFrame.pack(anchor=W, pady=2)
widthLbl = Label(widthFrame, text="Ширина:", font=("Arial", 9), bg='lightgray')
widthLbl.pack(side=LEFT)
widthEnt = Entry(widthFrame, bd=2, width=8, font=("Arial", 9))
widthEnt.pack(side=LEFT, padx=(5,0))

heightFrame = Frame(canvasSizeFrame, bg='lightgray')
heightFrame.pack(anchor=W, pady=2)
heightLbl = Label(heightFrame, text="Высота:", font=("Arial", 9), bg='lightgray')
heightLbl.pack(side=LEFT)
heightEnt = Entry(heightFrame, bd=2, width=8, font=("Arial", 9))
heightEnt.pack(side=LEFT, padx=(5,0))

applySizeBtn = Button(canvasSizeFrame, text="Применить", command=UpdateCanvasSize, bg="#2196F3", fg="white", font=("Arial", 9))
applySizeBtn.pack(anchor=W, pady=2)

# ========== СОЗДАНИЕ НАЧАЛЬНЫХ ШАРОВ ==========

config1 = {
    'x': 150,
    'y': ch - 50,
    'radius': 35,
    'color': 'red',
    'vx': 4.0,
    'vy': -7.5,
    'ay': 0.1,
    'wind': 0.03,
    'mass': 3.5,
    'freezemode': False
}

config2 = {
    'x': cw - 150,
    'y': ch - 50,
    'radius': 30,
    'color': 'blue',
    'vx': -4.0,
    'vy': -7.5,
    'ay': 0.1,
    'wind': 0.03,
    'mass': 3.0,
    'freezemode': False
}

ball1 = Ball(cnv, config1)
ball2 = Ball(cnv, config2)

balls.append(ball1)
balls.append(ball2)

# Устанавливаем начальные значения
gEnt.insert(0, '0.100')
windEnt.insert(0, '0.030')
widthEnt.insert(0, str(cw))
heightEnt.insert(0, str(ch))
ballCountLbl.config(text=f"Шаров: {len(balls)}")

# ========== ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ==========

delay = 20

def game_loop():
    global runAll, runMotion, getData
    if not runAll:
        root.destroy()
        return
    
    cnv.delete(ALL)
    
    for ball in balls:
        ball.draw()
    
    cnv.update()
    
    if runMotion:
        for ball in balls:
            ball.update_position(cw, ch)
        CheckAllCollisions()
        
    elif getData:
        UpdateAllBalls()
    
    cnv.after(delay, game_loop)


game_loop()
root.mainloop()