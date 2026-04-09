import tkinter as tk
import random
import math
import time
from threading import Lock, Thread

class GrowingCircle:
    def __init__(self, canvas, x, y, radius, color, thread_id, creation_time):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.original_color = color
        self.thread_id = thread_id
        self.creation_time = creation_time
        self.growing = True                 # Расширяется или сужается
        self.growth_rate = 1.0              # Скорость роста/сжатия
        self.collision_count = 0
        self.is_active = True
        self.lock = Lock()
        
    def draw(self):
        
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        
        self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=self.color,
            outline='black',
            width=2
        )
        
        # ID и время жизни круга
        if self.radius > 15:
            age = time.time() - self.creation_time
            self.canvas.create_text(
                self.x, self.y - 5,
                text=f"#{self.thread_id}",
                fill='white',
                font=('Arial', 10, 'bold')
            )
            self.canvas.create_text(
                self.x, self.y + 5,
                text=f"{age:.1f}s",
                fill='white',
                font=('Arial', 8)
            )
        pass

    # Обновляет размер круга
    def update_size(self):
        with self.lock:
            if self.growing:
                self.radius += self.growth_rate
            else:
                self.radius -= self.growth_rate
                
            # Проверка минимального размера
            if self.radius <= 2:
                self.radius = 2

                self.growing = True
                self.collision_count = 0
                self.growth_rate = 1.0
                self.creation_time = time.time()
                return True
                
        return False
    
    # Проверка на столкновение с другим кругом
    def collide_with(self, other_circle):

        if not (self.is_active and other_circle.is_active):
            return False
            
        distance = math.sqrt((self.x - other_circle.x)**2 + (self.y - other_circle.y)**2)

        if distance < (self.radius + other_circle.radius):
            return True
        return False
    
    # Инверсия цвета
    def invert_color(self, color):

        color_map = {
            'red': '#FF0000',
            'green': '#00FF00',
            'blue': '#0000FF',
            'yellow': '#FFFF00',
            'cyan': '#00FFFF',
            'magenta': '#FF00FF',
            'orange': '#FFA500',
            'purple': '#800080',
            'pink': '#FFC0CB',
            'brown': '#A52A2A'
        }
        
        hex_color = color_map.get(color, color)
        
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = 255 - r
        g = 255 - g
        b = 255 - b
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def get_radius(self):
        with self.lock:
            return self.radius
    
    def get_age(self):
        return time.time() - self.creation_time
    
    def stop(self):
        self.is_active = False

    pass


class CircleThread:
    def __init__(self, circle_id, canvas, width, height, on_collision):
        self.circle_id = circle_id
        self.canvas = canvas
        self.width = width
        self.height = height
        self.on_collision = on_collision
        self.circle = None
        self.running = True
        self.paused = False
        self.creation_time = time.time()
    
    # Создает новый круг в случайной позиции
    def create_circle(self):
        radius = 20
        x = random.randint(radius + 10, self.width - radius - 10)
        y = random.randint(radius + 10, self.height - radius - 10)
        color = random.choice(['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'cyan', 'magenta'])
        
        self.circle = GrowingCircle(self.canvas, x, y, radius, color, self.circle_id, self.creation_time)
        return self.circle
    
    def run(self):
        while self.running:
            if not self.paused and self.circle and self.circle.is_active:
                reset_needed = self.circle.update_size()
                
                if reset_needed:
                    self.creation_time = time.time()
            
            time.sleep(0.05)
    
    def stop(self):
        self.running = False
        if self.circle:
            self.circle.stop()
    
    def pause(self):
        self.paused = True
    
    def resume(self):
        self.paused = False

    pass


class GrowingCirclesGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Растущие круги - многопоток")
        
        # Параметры
        self.width = 800
        self.height = 600
        self.threads = []
        self.circles = []
        self.next_id = 1
        self.running = True
        self.pause   = False
        self.collision_lock = Lock()
        
        # Создаем холст
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='white')
        self.canvas.pack(pady=10)
        
        # Панель управления
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        
        self.add_btn = tk.Button(control_frame, text="Добавить круг", command=self.add_circle, 
                                  bg='lightgreen', font=('Arial', 12))
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.start_btn = tk.Button(control_frame, text="Старт", command=self.start_all,
                                    bg='lightblue', font=('Arial', 12))
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(control_frame, text="Пауза", command=self.pause_all,
                                    bg='orange', font=('Arial', 12))
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(control_frame, text="Очистить всё", command=self.clear_all,
                                    bg='lightcoral', font=('Arial', 12))
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        info_frame = tk.Frame(root)
        info_frame.pack(pady=5)
        
        self.info_label = tk.Label(info_frame, text="Кругов: 0 | Активных: 0", 
                                    font=('Arial', 12, 'bold'))
        self.info_label.pack()
        
        stats_frame = tk.Frame(root)
        stats_frame.pack(pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Столкновений: 0", 
                                     font=('Arial', 10))
        self.stats_label.pack()
        
        self.collision_count = 0
        
        self.add_circle()
        self.animate()

        root.protocol("WM_DELETE_WINDOW", root.destroy)
    
    # Добавляет новый круг
    def add_circle(self):
        thread = CircleThread(self.next_id, self.canvas, self.width, self.height, self.on_collision)
        
        circle = thread.create_circle()
        
        if self.pause:
            thread.pause()

        self.threads.append(thread)
        self.circles.append(circle)
        

        t = Thread(target=thread.run, daemon=True)
        t.start()
        
        self.next_id += 1
        self.update_info()
        print(f"[{time.strftime('%H:%M:%S')}] Добавлен круг #{circle.thread_id} (возраст: 0.0с)")
        pass
    
    # Обработчик столкновения между кругами
    def on_collision(self, circle_id1, circle_id2):
        circle1 = None
        circle2 = None
        
        for c in self.circles:
            if c.thread_id == circle_id1:
                circle1 = c
            elif c.thread_id == circle_id2:
                circle2 = c
        
        if circle1 and circle2 and circle1.is_active and circle2.is_active:
            if circle1.collide_with(circle2):
                self.collision_count += 1
                self.stats_label.config(text=f"Столкновений: {self.collision_count}")
                
                age1 = circle1.get_age()
                age2 = circle2.get_age()
                
                print(f"[{time.strftime('%H:%M:%S')}] Столкновение! Круг #{circle1.thread_id} (возраст: {age1:.1f}с, радиус: {circle1.radius:.1f}) и #{circle2.thread_id} (возраст: {age2:.1f}с, радиус: {circle2.radius:.1f})")
                

                if age1 > age2:
                    # Круг 1 старше - он уменьшается
                    older, younger = circle1, circle2
                    print(f"  -> Старая сфера #{older.thread_id} (возраст: {age1:.1f}с, радиус: {older.radius:.1f}) уменьшается")
                else:
                    # Круг 2 старше - он уменьшается
                    older, younger = circle2, circle1
                    print(f"  -> Старая сфера #{older.thread_id} (возраст: {age2:.1f}с, радиус: {older.radius:.1f}) уменьшается")
                
                with self.collision_lock:
                    if older.growing:
                        older.growing = False
                        older.collision_count = 1
                        older.growth_rate = 1.5
                        older.color = older.invert_color(older.color)
                        print(f"  -> Круг #{older.thread_id} начинает сжиматься")
        pass
    
    # Проверяет столкновения между всеми кругами
    def check_all_collisions(self):
        if self.pause:
            return
        
        for i in range(len(self.circles)):
            for j in range(i + 1, len(self.circles)):
                circle1 = self.circles[i]
                circle2 = self.circles[j]
                
                if circle1.is_active and circle2.is_active:
                    if circle1.collide_with(circle2):
                        self.on_collision(circle1.thread_id, circle2.thread_id)
    
    # Анимирует все круги
    def animate(self):
        if not self.running:
            return
        
        self.canvas.delete("all")
        self.check_all_collisions()
        
        active_count = 0
        max_radius = 0
        for circle in self.circles:
            if circle.is_active:
                circle.draw()
                active_count += 1
                if circle.radius > max_radius:
                    max_radius = circle.radius
        
        self.update_info()
        self.root.after(50, self.animate)

        pass
    
    def start_all(self):
        self.pause = False
        for thread in self.threads:
            thread.resume()
        print(f"[{time.strftime('%H:%M:%S')}] Все потоки запущены")
    
    def pause_all(self):
        self.pause = True
        for thread in self.threads:
            thread.pause()
        print(f"[{time.strftime('%H:%M:%S')}] Все потоки на паузе")
    
    def clear_all(self):
        for thread in self.threads:
            thread.stop()
        self.pause = False
        self.threads.clear()
        self.circles.clear()
        self.next_id = 1
        self.collision_count = 0
        self.stats_label.config(text="Столкновений: 0")
        self.update_info()
        print(f"[{time.strftime('%H:%M:%S')}] Все круги удалены")
        self.add_circle()
    
    def update_info(self):
        active = sum(1 for c in self.circles if c.is_active)
        max_radius = max([c.radius for c in self.circles if c.is_active], default=0)
        self.info_label.config(text=f"Кругов: {len(self.circles)} | Активных: {active} | Макс. радиус: {max_radius:.0f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GrowingCirclesGame(root)
    root.mainloop()