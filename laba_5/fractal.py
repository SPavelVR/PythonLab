from tkinter import *
import math

def Koch(order, x1, y1, x2, y2):
    if (order==0):
        canvas.create_line(x1,y1,x2,y2,fill=myColor, width=myPenWidth.get())
    else:
        alpha=math.atan2(y2-y1, x2-x1) 
        R=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

        # вычислим xA, yA, xB, yB, xC, yC 
        xA=x1+(R/3)*math.cos(alpha) 
        yA=y1+(R/3)*math.sin(alpha) 
        xC=xA+R*math.cos(alpha-math.pi/3)/3 
        yC=yA+R*math.sin(alpha-math.pi/3)/3 
        xB=x1+2*R*math.cos(alpha)/3 
        yB=y1+2*R*math.sin(alpha)/3

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

def Sierpinski(order, x, y, length):
    s3d2=math.sqrt(3)/2
    #строим цветной треугольник ABC #вычисляем координаты вершин треугольника
    points=[x, y, x+length/2, y-length*s3d2, x+length, y] 
    canvas.create_polygon(points, outline=myColor, fill=myColor,
    width=myPenWidth.get()) #теперь будем «выбрасывать» средние треугольники 
    if (order>0):
        #рисуем треугольник MNK цветом фона
        points=[x+length/4, y-length*s3d2/2, x+3*length/4, y-length*s3d2/2, x+length/2, y]
        canvas.create_polygon(points, outline='#fff', fill='#fff', width=myPenWidth.get())
        #рекурсивно вызываем фунцкию
        Sierpinski(order-1, x, y, length/2); # в т.A
        Sierpinski(order-1, x+length/2, y, length/2); # в т.K
        Sierpinski(order-1, x+length/4, y-length*s3d2/2, length/2); # в т.M
        pass
    pass


def getDragonPoints(order): 
    x=canvas.winfo_width()/5 
    y=canvas.winfo_height()/2 
    if (order==0):
        # ломаная нулевого порядка состоит из одного сегмента
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
    # начальная точка ломаной не изменяется 
    res.append(prevRes[0]) 
    res.append(prevRes[1])
    for i in range(0,len(prevRes)-3,2):
        # считаем очередной сегмент ломаной
        p1x=prevRes[i] 
        p1y=prevRes[i+1] 
        p2x=prevRes[i+2] 
        p2y=prevRes[i+3]
        alpha = math.atan2(p2y - p1y, p2x - p1x)-DirSign*math.pi/4 
        R = math.sqrt(((p1x - p2x) * (p1x - p2x) + (p1y - p2y) * (p1y - p2y))/2) 
        # найдем новую точку ломаной 
        pcx=p1x+R*math.cos(alpha) 
        pcy=p1y+R*math.sin(alpha)
        # добавляем ее и конечную точку в список точек ломаной
        res.append(pcx) 
        res.append(pcy) 
        res.append(p2x) 
        res.append(p2y)
        # меняем направление
        DirSign *= -1
    return res



root = Tk() # явно создать корневое окно

pict=Frame(root) # здесь будет канва и рисунок 
manage=Frame(root) # здесь будут управляющие элементы

pict.pack(side=LEFT) # разместим фреймы в окне 
manage.pack(side=RIGHT)

canvas=Canvas(pict, width=400, height=400) 
canvas.create_rectangle(0,0, 400, 400, outline='#fff', fill = '#fff') 
canvas.pack(fill=BOTH, expand=1)

rdVar=IntVar()  # ассоциированная переменная для радиокнопок 
rdVar.set(0)    # по умолчанию выбрана будет первая радиокнопка

# сами радиокнопки, родительский элемент — фрейм!!! 
rad0 = Radiobutton(manage,text="Кривая Коха", variable=rdVar,value=0)
rad1 = Radiobutton(manage,text="Салфетка Серпинского", variable=rdVar,value=1)
rad2 = Radiobutton(manage,text="Драконова ломаная", variable=rdVar,value=2)
rad3 = Radiobutton(manage,text="Звезда Коха", variable=rdVar,value=3)

rad0.pack(side=TOP, anchor=W) # экспериментируем с положением радиобаттонов 
rad1.pack(side=TOP, anchor=W)
rad2.pack(side=TOP, anchor=W)
rad3.pack(side=TOP, anchor=W)

# чтобы можно было управлять цветом кривой, заведем переменную и запишем туда # сначала черный цвет
myColor="#000"

#теперь, чтобы можно было вызывать диалоговое окно выбора цвета, сделам импорт
from tkinter.colorchooser import askcolor

#и заведем обработчик события, где будет вызываться диалоговое окно для цвета
def setColor(event):
    global myColor #тут уточняем, что работать будем с вышезаведенной переменной 
    (RGB, myColor)=askcolor() #запоминаем результат выбора цвета
    pass

    # а тут заводим кнопку, щелчок по которой вызовет диалог для выбора цвета # родительский элемент — фрейм
    # назначим обработчик и разместим кнопку 
butColor=Button(manage, text="Цвет") 
butColor.bind('<Button-1>', setColor) 
butColor.pack()

    #теперь введем 2 шкалы и определим ассоциированные переменные 
myPenWidth=IntVar() # для толщины линии фрактала 
myPenWidth.set(1) # установим ее равной 1 по умолчанию
penWidth = Scale(manage, label="Толщина линии", orient=HORIZONTAL, length=150, from_=1, to=10, tickinterval=1, resolution=1, variable=myPenWidth)

    # и ассоциированная переменная для второй шкалы — порядок фрактала 
myCurvePower=IntVar()
myCurvePower.set(0) # по умолчанию это 0
curvePower = Scale(manage, label="Порядок кривой", orient=HORIZONTAL, length=150, from_=0, to=20, tickinterval=5, resolution=1, variable=myCurvePower)

# разместим шкалы 
penWidth.pack() 
curvePower.pack()

def draw(event):

    curve = myCurvePower.get()
    pen = myPenWidth.get()

    if (rdVar.get()==0):
        x1=0
        y1=canvas.winfo_height() 
        x2=canvas.winfo_width() 
        y2=0
        Koch(curve,x1, y1, x2, y2)
        pass
    elif (rdVar.get()==1):
        Sierpinski(curve,0, canvas.winfo_height()-20, canvas.winfo_width()-10)
        pass
    elif (rdVar.get()==2):
        points = getDragonPoints(curve)
        canvas.create_line(points, fill=myColor, width=pen)
        pass
    elif rdVar.get()==3:
        Koch_zvezda(curve, canvas.winfo_width() // 2, canvas.winfo_height() // 2, 200)
        pass
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






