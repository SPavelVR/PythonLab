import math

"""
        Инициализация шара через словарь конфигурации
        
        Параметры конфигурации:
        - x: начальная позиция по X
        - y: начальная позиция по Y
        - radius: радиус шара
        - color: цвет шара (по умолчанию 'red')
        - vx: скорость по X (по умолчанию 4.0)
        - vy: скорость по Y (по умолчанию -7.5)
        - ay: ускорение по Y (по умолчанию 0.1)
        - wind: сила сопротивления воздуха (по умолчанию 0.0)
        - mass: масса шара (по умолчанию 1.0, пропорциональна 1/10 радиусу)
        - freezemode: режим заморозки (по умолчанию False)
        """

class Ball:
    def __init__(self, canvas, config):
        
        self.canvas = canvas
        
        # Загружаем параметры из словаря с значениями по умолчанию
        self.x = config.get('x', 0)
        self.y = config.get('y', 0)
        self.radius = config.get('radius', 35)
        self.color = config.get('color', 'red')
        self.vx = config.get('vx', 4.0)
        self.vy = config.get('vy', -7.5)
        self.ay = config.get('ay', 0.1)
        self.wind = config.get('wind', 0.0)  # Сила сопротивления воздуха
        self.mass = config.get('mass', self.radius / 10)  # Масса пропорциональна радиусу
        self.freezemode = config.get('freezemode', False)  # Режим заморозки
        self.grabbed = False
        self.grab_index = -1  # Индекс захваченного шара
        pass

    # Рисует шар на canvas
    def draw(self):

        outline = 'gray' if self.freezemode else ''
        width = 2 if self.freezemode else 0
        
        self.canvas.create_oval(
            self.x - self.radius, 
            self.y - self.radius,
            self.x + self.radius, 
            self.y + self.radius, 
            fill=self.color,
            outline=outline,
            width=width
        )
        
        # Если шар заморожен, рисуем белый крест
        if self.freezemode:
            self.canvas.create_line(
                self.x - self.radius//2, self.y - self.radius//2,
                self.x + self.radius//2, self.y + self.radius//2,
                fill='white', width=2
            )
            self.canvas.create_line(
                self.x + self.radius//2, self.y - self.radius//2,
                self.x - self.radius//2, self.y + self.radius//2,
                fill='white', width=2
            )
    # Обновляет позицию шара с учетом физики, границ и сопротивления воздуха
    def update_position(self, cw, ch):

        if self.freezemode:
            return
        
        if self.vx != 0 and self.wind:
            if self.vx > 0:
                self.vx -= self.wind
                if self.vx < 0:
                    self.vx = 0
            else:
                self.vx += self.wind
                if self.vx > 0:
                    self.vx = 0
        
        if self.vy < 0 and self.wind:
            self.vy += self.wind
            if self.vy > 0:
                self.vy = 0
        

        new_x = self.x + self.vx
        new_y = self.y + self.vy + 0.5 * self.ay
        
        # Проверка столкновений с границами по X
        if (new_x + self.radius) >= cw:
            self.vx = -abs(self.vx)
            new_x = cw - self.radius
        elif (new_x - self.radius) <= 0:
            self.vx = abs(self.vx)
            new_x = self.radius
        
        # Проверка столкновений с границами по Y
        if (new_y + self.radius) >= ch:
            self.vy = -abs(self.vy)
            new_y = ch - self.radius
        elif (new_y - self.radius) <= 0:
            self.vy = abs(self.vy)
            new_y = self.radius
        

        self.x = new_x
        self.y = new_y
        

        self.vy += self.ay * 0.5
        

        if abs(self.vx) < 0.05 and abs(self.vy) < 0.05:
            self.vx = 0
            self.vy = 0

        pass
    
    # Проверяет столкновение с другим шаром и обновляет скорости
    def check_collision(self, other_ball):

        if self.freezemode and other_ball.freezemode:
            return
            
        dx = self.x - other_ball.x
        dy = self.y - other_ball.y
        distance = math.sqrt(dx*dx + dy*dy)
        min_distance = (self.radius + other_ball.radius) * 1.01
        

        if distance < min_distance:
            overlap = min_distance - distance
            if distance > 0:
                angle = math.atan2(dy, dx)
                correction_x = math.cos(angle) * overlap / 2
                correction_y = math.sin(angle) * overlap / 2
                if not self.freezemode:
                    self.x += correction_x
                    self.y += correction_y
                if not other_ball.freezemode:
                    other_ball.x -= correction_x
                    other_ball.y -= correction_y
            

            nx = dx / distance if distance > 0 else 1
            ny = dy / distance if distance > 0 else 0
            
            vrel_x = self.vx - other_ball.vx
            vrel_y = self.vy - other_ball.vy
            
            vrel_n = vrel_x * nx + vrel_y * ny
            

            if vrel_n > 0:
                return
            
            # Коэффициент упругости
            e = 1
            
            m1 = self.mass
            m2 = other_ball.mass
            
            # Импульс
            impulse = (1 + e) * vrel_n / (1/m1 + 1/m2)
            
            if not self.freezemode:
                self.vx -= impulse * nx / m1
                self.vy -= impulse * ny / m1
            if not other_ball.freezemode:
                other_ball.vx += impulse * nx / m2
                other_ball.vy += impulse * ny / m2
            
            pass
    
    # Проверяет, находится ли точка внутри шара
    def is_point_inside(self, event_x, event_y):
        return ((self.x - event_x)**2 + (self.y - event_y)**2) < self.radius**2
    
    def grab_ball(self):
        self.grabbed = True
    
    def release_ball(self):
        self.grabbed = False
    
    # Перемещает шар при помощи мышки
    def drag_ball(self, event_x, event_y):

        if self.grabbed:
            self.x = event_x
            self.y = event_y

        pass
    
    def update_radius(self, new_radius):

        old_radius = self.radius
        self.radius = new_radius
        self.mass = new_radius / 10
        self.x += (new_radius - old_radius)
        self.y += (new_radius - old_radius)
    
    def update_acceleration(self, new_ay):
        self.ay = new_ay
    
    def update_wind(self, new_wind):
        self.wind = new_wind
    
    def get_position(self):
        return (self.x, self.y)
    
    def get_radius(self):
        return self.radius
    
    def get_acceleration(self):
        return self.ay
    
    def get_wind(self):
        return self.wind
    
    def set_color(self, color):
        self.color = color
    
    def get_color(self):
        return self.color
    
    def toggle_freezemode(self):
        
        self.freezemode = not self.freezemode

        if self.freezemode:
            self.vx = 0
            self.vy = 0

        pass
    
    def set_freezemode(self, value):
        self.freezemode = value
        if self.freezemode:
            self.vx = 0
            self.vy = 0
        pass
    
    def get_freezemode(self):
        return self.freezemode
    
    def get_config(self):
        
        d = {
            'x': self.x,
            'y': self.y,
            'radius': self.radius,
            'color': self.color,
            'vx': self.vx,
            'vy': self.vy,
            'ay': self.ay,
            'wind': self.wind,
            'mass': self.mass,
            'freezemode': self.freezemode
        }
        return d;