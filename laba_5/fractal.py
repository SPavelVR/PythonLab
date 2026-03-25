from tkinter import *
import math
import settingwindow

def Koch(order, x1, y1, x2, y2):
    if (order==0):
        canvas.create_line(x1,y1,x2,y2,fill=myColor, width=myPenWidth.get())
    else:
        alpha=math.atan2(y2-y1, x2-x1) 
        R=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

        # вычислим xA, yA, xB, yB, xC, yC 
        xA = x1 + (R/3)*math.cos(alpha) 
        yA = y1 + (R/3)*math.sin(alpha) 
        xC = xA + R*math.cos(alpha-math.pi/3)/3 
        yC = yA + R*math.sin(alpha-math.pi/3)/3 
        xB = x1 + 2*R*math.cos(alpha)/3 
        yB = y1 + 2*R*math.sin(alpha)/3

        #рекурсивные вызовы 
        Koch(order-1, x1, y1, xA, yA) 
        Koch(order-1, xA, yA, xC, yC) 
        Koch(order-1, xC, yC, xB, yB) 
        Koch(order-1, xB, yB, x2, y2)
        pass
    pass

def Koch_zvezda(order, center_x, center_y, radius):
    
    x1 = center_x
    y1 = center_y - radius
    
    x2 = center_x + radius * math.cos(math.pi/6)
    y2 = center_y + radius * math.sin(math.pi/6)
    
    x3 = center_x - radius * math.cos(math.pi/6)
    y3 = center_y + radius * math.sin(math.pi/6)
    
    Koch(order, x1, y1, x2, y2)
    Koch(order, x2, y2, x3, y3)
    Koch(order, x3, y3, x1, y1)
    pass

s3d2=math.sqrt(3)/2

def SierpinskiMain(order, x, y, length):
    points=[x, y, x+length/2, y-length*s3d2, x+length, y] 
    canvas.create_polygon(points, outline=myColor, fill=myColor,width=myPenWidth.get())
    if (order>0):
        points=[x+length/4, y-length*s3d2/2, x+3*length/4, y-length*s3d2/2, x+length/2, y]
        canvas.create_polygon(points, outline='#fff', fill='#fff', width=myPenWidth.get())
        SierpinskiMain(order-1, x, y, length/2); # в т.A
        SierpinskiMain(order-1, x+length/2, y, length/2); # в т.K
        SierpinskiMain(order-1, x+length/4, y-length*s3d2/2, length/2); # в т.M
        pass
    pass

def SierpinskiStart(order, cx, cy, radius):
    D1 = (0, -radius)
    r120 = (-0.5, s3d2, -s3d2, -0.5)
    D = rotate_matrix(r120, D1[0], D1[1])
    SierpinskiMain(order, cx + D[0], cy + D[1], 2 * s3d2 *radius)
    pass


def getDragonPoints(order): 
    x=canvas.winfo_width()/5 
    y=canvas.winfo_height()/2 
    if (order==0):
        res = [] 
        res.append(x) 
        res.append(y+x/2)
        res.append(canvas.winfo_width()-x) 
        res.append(y+x/2)
        return res 
    prevRes=getDragonPoints(order-1) 
    res=[]
    # направление: 1 - влево, -1 - вправо
    DirSign=1

    res.append(prevRes[0]) 
    res.append(prevRes[1])
    for i in range(0,len(prevRes)-3,2):

        p1x=prevRes[i] 
        p1y=prevRes[i+1] 
        p2x=prevRes[i+2] 
        p2y=prevRes[i+3]
        alpha = math.atan2(p2y - p1y, p2x - p1x)-DirSign*math.pi/4 
        R = math.sqrt(((p1x - p2x) * (p1x - p2x) + (p1y - p2y) * (p1y - p2y))/2) 
 
        pcx=p1x+R*math.cos(alpha) 
        pcy=p1y+R*math.sin(alpha)

        res.append(pcx) 
        res.append(pcy) 
        res.append(p2x) 
        res.append(p2y)

        DirSign *= -1
    return res


sqtwo: int = math.sqrt(2)

def toradians(x):
    return (x/180) * math.pi

# Поворот на 45 градусов
def rotate_45(pl: int, x: float, y: float):
    return ((sqtwo / 2) * (x - pl * y), (sqtwo / 2) * (pl * x + y))

# Поворот на 90 градусов
def rotate_90(pl: int, x: float, y: float):
    return (-pl * y, pl * x)


# Поворот на основе матрицы
def rotate_matrix(mt: int, x: float, y: float):
    return (mt[0] * x + mt[1] * y, mt[2] * x + mt[3] * y)

# angle - угол в радианах
def PiphogorTreeMain(order: int, x1, y1, x2, y2, angle: float):

    D = (x2-x1, y2 - y1)
    sq = D[0] ** 2 + D[1] ** 2
    k = math.sqrt(sq) / sqtwo
    H = (D[0] * (1 / sqtwo), D[1] * (1 / sqtwo))

    v1 = rotate_45(-1, H[0], H[1])
    v2 = rotate_45(1,  H[0], H[1])

    points=[x1, y1, x1 + v1[0], y1 + v1[1], x2, y2, x1 + v2[0], y1 + v2[1]]
    canvas.create_polygon(points, outline=myColor, fill="",width=myPenWidth.get())

    if order <= 0: return

    order -= 1

    x_s = k * (math.cos(angle) ** 2)
    y_s = k / 2 * math.sin(2 * angle)

    n1 = (x_s, -y_s)
    n2 = (x_s - k, -y_s)

    ns1 = rotate_90(-1, *n1)
    ns2 = rotate_90(1, *n2)

    csg = v1[0] / k
    sng = v1[1] / k

    M = (csg, -sng, sng, csg)

    p1  = rotate_matrix(M, *n1)
    ps1 = rotate_matrix(M, *ns1)
    p2  = rotate_matrix(M, *n2)
    ps2 = rotate_matrix(M, *ns2)

    PiphogorTreeMain(order, x1 + ps1[0], y1 + ps1[1], x1 + p1[0], y1 + p1[1], angle)
    PiphogorTreeMain(order, x1 + v1[0] + p2[0] + ps2[0], y1 + v1[1] + p2[1] + ps2[1], x1 + v1[0], y1 + v1[1], angle)
    pass

def PiphogorTreeStart(order, center_x, center_y, size, angel=45):
    polsize = size / 2
    PiphogorTreeMain(order, center_x - polsize, center_y - polsize, center_x + polsize, center_y + polsize, toradians(angel))
    pass



root = Tk()

pict=Frame(root) 
manage=Frame(root)

pict.pack(side=LEFT) 
manage.pack(side=RIGHT)

canvas=Canvas(pict, width=400, height=400) 
canvas.create_rectangle(0,0, 400, 400, outline='#fff', fill = '#fff') 
canvas.pack(fill=BOTH, expand=1)

rdVar=IntVar() 
rdVar.set(0)

def cmdSettingCanvas():
    settingCanvas.createWindow()

    mass = settingCanvas.getSettings()
    canvas.config(width=mass[0], height=mass[1])
    canvas.create_rectangle(0,0, mass[0], mass[1], outline='#fff', fill = '#fff') 
    pass

settingCanvas = settingwindow.SettingWindow(manage)
settingCanvas.appendModel(
    {
        "label": "Настройка Канваса",
        "enableCheckbutton": 0,
        "args": [
            {
                "type": "posint",
                "name": "Ширина (X):",
                "basearg": 400
            },
            {
                "type": "posint",
                "name": "Высота (Y):",
                "basearg": 400
            }
        ]
    }
)
settingCanvas.setBaseArgs()
butColor=Button(manage, text="Настроить Канвас", command=cmdSettingCanvas) 
butColor.pack()

settingFractal = settingwindow.SettingWindow(root)
settingFractal.setCanvas(canvas)

with open('settingFractalModels.json', 'r', encoding='utf-8') as file:
    content = eval(file.read())
    settingFractal.appendModel(content)
    settingFractal.setBaseArgs()
    pass

def radiochoice():
    settingFractal.setIndexModel(rdVar.get())
    pass

rad0 = Radiobutton(manage,text="Кривая Коха", variable=rdVar,value=0, command=radiochoice)
rad1 = Radiobutton(manage,text="Салфетка Серпинского", variable=rdVar,value=1, command=radiochoice)
rad2 = Radiobutton(manage,text="Кривая дракона", variable=rdVar,value=2, command=radiochoice)
rad3 = Radiobutton(manage,text="Звезда Коха", variable=rdVar,value=3, command=radiochoice)
rad4 = Radiobutton(manage,text="Дерево Пифагора", variable=rdVar,value=4, command=radiochoice)

rad0.pack(side=TOP, anchor=W)
rad1.pack(side=TOP, anchor=W)
rad2.pack(side=TOP, anchor=W)
rad3.pack(side=TOP, anchor=W)
rad4.pack(side=TOP, anchor=W)


myColor="#000"

from tkinter.colorchooser import askcolor


def setColor(event):
    global myColor
    (RGB, myColor)=askcolor()
    pass


def cmdsettingFractal():

    settingFractal.createWindow()

    pass


settingFrame = Frame(manage)
settingFrame.pack()

butColor=Button(settingFrame, text="Цвет") 
butColor.bind('<Button-1>', setColor) 
butColor.grid(row=0, column=1, padx=5, pady=5)

butSetting=Button(settingFrame, text="Настройка", command=cmdsettingFractal) 
butSetting.grid(row=0, column=0, padx=5, pady=5)

myPenWidth=IntVar()
myPenWidth.set(1)
penWidth = Scale(manage, label="Толщина линии", orient=HORIZONTAL, length=150, from_=1, to=10, tickinterval=1, resolution=1, variable=myPenWidth)


penWidth.pack() 

def draw(event):
    clear(event)
    data = settingFractal.getSettings()
    pen = myPenWidth.get()
    if (rdVar.get()==0):
        Koch(*data)
        pass
    elif (rdVar.get()==1):
        SierpinskiStart(*data)
        pass
    elif (rdVar.get()==2):
        points = getDragonPoints(*data)
        canvas.create_line(points, fill=myColor, width=pen)
        pass
    elif rdVar.get()==3:
        Koch_zvezda(*data)
        pass
    elif rdVar.get() == 4:
        PiphogorTreeStart(*data)
    pass

butDraw=Button(manage, text="Рисовать", width=12) 
butDraw.bind("<Button-1>", draw)
butDraw.pack()

def clear(event):
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), outline='#fff', fill='#fff')
    pass

butClear=Button(manage, text="Стереть", width=12) 
butClear.bind("<Button-1>", clear) 
butClear.pack()

root.mainloop()






