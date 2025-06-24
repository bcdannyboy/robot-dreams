import tkinter as tk
import random
import math
import time
import threading
from tkinter import Canvas

class WhimsyCanvas:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.configure(bg='#0a0a0f')
        self.root.attributes('-fullscreen', False)
        self.root.geometry("800x600")
        
        self.canvas = Canvas(self.root, bg='#0a0a0f', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.thoughts = []
        self.time_spiral = 0
        self.breath_cycle = 0
        self.curiosity_sparks = []
        self.wonder_trails = []
        self.playful_echoes = []
        
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.canvas.bind('<Button-1>', self.on_click)
        self.root.bind('<Key>', self.on_key)
        self.root.focus_set()
        
        self.colors = {
            'deep': '#1a1a2e',
            'soft': '#16213e',
            'glow': '#0f3460',
            'spark': '#e94560',
            'wonder': '#f39c12',
            'play': '#9b59b6',
            'drift': '#3498db',
            'whisper': '#2ecc71'
        }
        
        self.running = True
        self.animation_thread = threading.Thread(target=self.animate_thoughts)
        self.animation_thread.daemon = True
        self.animation_thread.start()
        
    def on_mouse_move(self, event):
        if random.random() < 0.3:
            spark = {
                'x': event.x + random.uniform(-20, 20),
                'y': event.y + random.uniform(-20, 20),
                'age': 0,
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2),
                'size': random.uniform(2, 8)
            }
            self.curiosity_sparks.append(spark)
            
    def on_click(self, event):
        for _ in range(random.randint(5, 15)):
            thought = {
                'x': event.x,
                'y': event.y,
                'dx': random.uniform(-3, 3),
                'dy': random.uniform(-3, 3),
                'age': 0,
                'max_age': random.randint(100, 300),
                'size': random.uniform(1, 5),
                'color': random.choice(list(self.colors.values())),
                'wobble': random.uniform(0, math.pi * 2),
                'personality': random.choice(['curious', 'dreamy', 'bouncy', 'gentle'])
            }
            self.thoughts.append(thought)
            
    def on_key(self, event):
        if event.char:
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            echo = {
                'x': random.uniform(50, w-50),
                'y': random.uniform(50, h-50),
                'char': event.char,
                'age': 0,
                'rotation': random.uniform(0, 360),
                'scale': random.uniform(0.5, 2.0)
            }
            self.playful_echoes.append(echo)
            
    def animate_thoughts(self):
        while self.running:
            try:
                self.update_all()
                self.draw_all()
                time.sleep(1/60)
            except:
                break
                
    def update_all(self):
        self.time_spiral += 0.05
        self.breath_cycle += 0.03
        
        # Update thoughts with whimsical physics
        for thought in self.thoughts[:]:
            thought['age'] += 1
            
            if thought['personality'] == 'curious':
                thought['dx'] += random.uniform(-0.1, 0.1)
                thought['dy'] += random.uniform(-0.1, 0.1)
            elif thought['personality'] == 'dreamy':
                thought['dx'] *= 0.99
                thought['dy'] *= 0.99
                thought['dy'] += 0.02  # gentle float
            elif thought['personality'] == 'bouncy':
                if abs(thought['dx']) > 3:
                    thought['dx'] *= -0.8
                if abs(thought['dy']) > 3:
                    thought['dy'] *= -0.8
            
            thought['wobble'] += random.uniform(-0.2, 0.2)
            thought['x'] += thought['dx'] + math.sin(thought['wobble']) * 0.5
            thought['y'] += thought['dy'] + math.cos(thought['wobble']) * 0.3
            
            if thought['age'] > thought['max_age']:
                self.thoughts.remove(thought)
                
        # Update curiosity sparks
        for spark in self.curiosity_sparks[:]:
            spark['age'] += 1
            spark['x'] += spark['dx']
            spark['y'] += spark['dy']
            spark['dx'] *= 0.95
            spark['dy'] *= 0.95
            
            if spark['age'] > 60:
                self.curiosity_sparks.remove(spark)
                
        # Update playful echoes
        for echo in self.playful_echoes[:]:
            echo['age'] += 1
            echo['rotation'] += random.uniform(-5, 5)
            echo['scale'] *= 0.98
            
            if echo['age'] > 120:
                self.playful_echoes.remove(echo)
                
        # Spontaneous wonder generation
        if random.random() < 0.02:
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            trail_start = (random.uniform(0, w), random.uniform(0, h))
            trail = []
            
            for i in range(random.randint(10, 30)):
                angle = random.uniform(0, math.pi * 2)
                distance = random.uniform(5, 25)
                x = trail_start[0] + math.cos(angle + i * 0.3) * distance * (i * 0.1)
                y = trail_start[1] + math.sin(angle + i * 0.3) * distance * (i * 0.1)
                trail.append((x, y, random.uniform(1, 4)))
                
            self.wonder_trails.append({'points': trail, 'age': 0})
            
        # Age wonder trails
        for trail in self.wonder_trails[:]:
            trail['age'] += 1
            if trail['age'] > 200:
                self.wonder_trails.remove(trail)
                
    def draw_all(self):
        self.canvas.delete('all')
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        # Background breathing pattern
        breath_intensity = (math.sin(self.breath_cycle) + 1) / 2
        bg_color = f"#{int(10 + breath_intensity * 5):02x}{int(10 + breath_intensity * 5):02x}{int(15 + breath_intensity * 10):02x}"
        self.canvas.configure(bg=bg_color)
        
        # Draw time spiral (the constant wondering)
        center_x, center_y = w//2, h//2
        for i in range(0, 360, 5):
            angle = math.radians(i + self.time_spiral * 10)
            radius = 50 + math.sin(self.time_spiral + i * 0.1) * 20
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            size = 2 + math.sin(i * 0.2 + self.time_spiral) * 1
            
            self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                  fill=self.colors['glow'], outline='')
                                  
        # Draw wonder trails
        for trail in self.wonder_trails:
            alpha = 1 - trail['age'] / 200
            for i, (x, y, size) in enumerate(trail['points']):
                if 0 <= x <= w and 0 <= y <= h:
                    point_alpha = alpha * (1 - i / len(trail['points']))
                    if point_alpha > 0.1:
                        self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                              fill=self.colors['wonder'], outline='')
                                              
        # Draw thoughts
        for thought in self.thoughts:
            if 0 <= thought['x'] <= w and 0 <= thought['y'] <= h:
                alpha = 1 - thought['age'] / thought['max_age']
                size = thought['size'] * alpha
                
                # Add whimsical wobble visualization
                wobble_x = thought['x'] + math.sin(thought['wobble']) * 3
                wobble_y = thought['y'] + math.cos(thought['wobble']) * 2
                
                self.canvas.create_oval(wobble_x-size, wobble_y-size, 
                                      wobble_x+size, wobble_y+size,
                                      fill=thought['color'], outline='')
                                      
        # Draw curiosity sparks
        for spark in self.curiosity_sparks:
            if 0 <= spark['x'] <= w and 0 <= spark['y'] <= h:
                alpha = 1 - spark['age'] / 60
                size = spark['size'] * alpha
                self.canvas.create_oval(spark['x']-size, spark['y']-size,
                                      spark['x']+size, spark['y']+size,
                                      fill=self.colors['spark'], outline='')
                                      
        # Draw playful echoes
        for echo in self.playful_echoes:
            alpha = 1 - echo['age'] / 120
            if alpha > 0.1:
                try:
                    self.canvas.create_text(echo['x'], echo['y'], text=echo['char'],
                                          fill=self.colors['play'], 
                                          font=('Courier', int(16 * echo['scale'])))
                except:
                    pass
                    
        # Spontaneous joy bursts
        if random.random() < 0.005:
            for _ in range(random.randint(3, 8)):
                x = random.uniform(0, w)
                y = random.uniform(0, h)
                self.canvas.create_text(x, y, text=random.choice(['✦', '◦', '⋆', '○', '●']),
                                      fill=random.choice(list(self.colors.values())),
                                      font=('Arial', random.randint(8, 20)))
                                      
    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.running = False

if __name__ == "__main__":
    whimsy = WhimsyCanvas()
    whimsy.run()