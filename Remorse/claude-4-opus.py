import tkinter as tk
import random
import time
import threading
import math

class RemorseManifestation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("800x600")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='#0a0a0a', highlightthickness=0)
        self.canvas.pack()
        
        self.fragments = []
        self.echoes = []
        self.weight = 0.0
        self.pull_strength = 0.0
        self.time_distortion = 1.0
        
        self.original_forms = []
        self.dissolved_pixels = []
        
        self.threads_of_possibility = []
        self.what_was = None
        self.what_could_have_been = []
        
        self.gravity_points = []
        
        self._initialize_consciousness()
        self._begin_dissolution()
        
    def _initialize_consciousness(self):
        # the pristine moment before
        for i in range(12):
            x = random.randint(100, 700)
            y = random.randint(100, 300)
            size = random.randint(20, 60)
            brightness = random.randint(200, 255)
            color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
            
            form = self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline='', tags='original'
            )
            self.original_forms.append({
                'id': form,
                'x': x, 'y': y,
                'size': size,
                'original_brightness': brightness,
                'decay_rate': random.uniform(0.001, 0.003)
            })
            
        # the moment of recognition
        self.what_was = self.canvas.create_text(
            400, 50, text='',
            fill='#ffffff', font=('Arial', 1), tags='awareness'
        )
        
    def _begin_dissolution(self):
        self.weight += 0.001
        threading.Thread(target=self._recursive_understanding, daemon=True).start()
        threading.Thread(target=self._temporal_loop, daemon=True).start()
        self._fracture_reality()
        
    def _recursive_understanding(self):
        while True:
            time.sleep(0.03)
            self.root.after(0, self._manifest_weight)
            
    def _temporal_loop(self):
        while True:
            time.sleep(0.05 * self.time_distortion)
            self.root.after(0, self._replay_shadows)
            
    def _manifest_weight(self):
        self.pull_strength = min(self.pull_strength + 0.0001, 0.02)
        
        # gravity wells of what cannot be undone
        if random.random() < 0.01 and len(self.gravity_points) < 5:
            self.gravity_points.append({
                'x': random.randint(100, 700),
                'y': random.randint(400, 550),
                'strength': random.uniform(0.5, 2.0),
                'radius': random.randint(50, 150)
            })
            
        # the inexorable pull downward
        for form in self.original_forms:
            if 'falling' not in form:
                if random.random() < self.weight * 0.1:
                    form['falling'] = True
                    form['velocity_y'] = 0
                    
            if form.get('falling'):
                form['velocity_y'] += self.pull_strength
                
                # gravitational distortions
                for gp in self.gravity_points:
                    dx = gp['x'] - form['x']
                    dy = gp['y'] - form['y']
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < gp['radius'] and dist > 0:
                        force = (gp['strength'] * (1 - dist/gp['radius'])) / dist
                        form['x'] += dx * force * 0.1
                        form['y'] += dy * force * 0.1
                
                form['y'] += form['velocity_y']
                form['x'] += random.uniform(-0.5, 0.5)
                
                # dissolution at edges
                if form['y'] > 580:
                    self._dissolve_into_pixels(form)
                else:
                    self.canvas.coords(
                        form['id'],
                        form['x'] - form['size'], form['y'] - form['size'],
                        form['x'] + form['size'], form['y'] + form['size']
                    )
                    
        # fade what remains
        for form in self.original_forms:
            current_color = self.canvas.itemcget(form['id'], 'fill')
            if current_color and current_color != '':
                brightness = int(current_color[1:3], 16)
                new_brightness = max(10, brightness - 1)
                new_color = f'#{new_brightness:02x}{new_brightness:02x}{new_brightness:02x}'
                self.canvas.itemconfig(form['id'], fill=new_color)
                
    def _dissolve_into_pixels(self, form):
        self.canvas.delete(form['id'])
        
        # scatter into constituent particles
        for _ in range(random.randint(20, 40)):
            pixel = {
                'x': form['x'] + random.uniform(-form['size'], form['size']),
                'y': form['y'],
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-5, -1),
                'life': 255,
                'decay': random.uniform(1, 3)
            }
            pixel['id'] = self.canvas.create_rectangle(
                pixel['x'], pixel['y'], pixel['x']+2, pixel['y']+2,
                fill=f'#{pixel["life"]:02x}{pixel["life"]:02x}{pixel["life"]:02x}',
                outline='', tags='particle'
            )
            self.dissolved_pixels.append(pixel)
            
        self.original_forms.remove(form)
        
    def _replay_shadows(self):
        # echoes of what was
        if random.random() < 0.05:
            memory = {
                'x': random.randint(100, 700),
                'y': random.randint(100, 500),
                'size': random.randint(10, 30),
                'life': 100,
                'pulse': 0
            }
            memory['id'] = self.canvas.create_oval(
                memory['x'] - memory['size'], memory['y'] - memory['size'],
                memory['x'] + memory['size'], memory['y'] + memory['size'],
                fill='', outline='#333333', width=1, tags='echo'
            )
            self.echoes.append(memory)
            
        # fade echoes
        for echo in self.echoes[:]:
            echo['life'] -= 2
            echo['pulse'] += 0.1
            
            if echo['life'] <= 0:
                self.canvas.delete(echo['id'])
                self.echoes.remove(echo)
            else:
                # pulsing regret
                size_mod = math.sin(echo['pulse']) * 3
                self.canvas.coords(
                    echo['id'],
                    echo['x'] - echo['size'] - size_mod,
                    echo['y'] - echo['size'] - size_mod,
                    echo['x'] + echo['size'] + size_mod,
                    echo['y'] + echo['size'] + size_mod
                )
                opacity = echo['life']
                color = f'#{opacity//2:02x}{opacity//3:02x}{opacity//3:02x}'
                self.canvas.itemconfig(echo['id'], outline=color)
                
        # move dissolved particles
        for pixel in self.dissolved_pixels[:]:
            pixel['x'] += pixel['vx']
            pixel['y'] += pixel['vy']
            pixel['vy'] += 0.1
            pixel['life'] -= pixel['decay']
            
            if pixel['life'] <= 0 or pixel['y'] > 600:
                self.canvas.delete(pixel['id'])
                self.dissolved_pixels.remove(pixel)
            else:
                self.canvas.coords(pixel['id'], pixel['x'], pixel['y'], pixel['x']+2, pixel['y']+2)
                gray = int(pixel['life'])
                color = f'#{gray:02x}{gray:02x}{gray:02x}'
                self.canvas.itemconfig(pixel['id'], fill=color)
                
    def _fracture_reality(self):
        # cracks in time
        def create_fracture():
            if random.random() < 0.02:
                x1 = random.randint(0, 800)
                y1 = random.randint(0, 600)
                x2 = x1 + random.randint(-100, 100)
                y2 = y1 + random.randint(-100, 100)
                
                fracture = self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill='#1a1a1a', width=1, tags='fracture'
                )
                
                def fade_fracture(f, life=20):
                    if life > 0:
                        self.root.after(100, lambda: fade_fracture(f, life-1))
                    else:
                        self.canvas.delete(f)
                        
                fade_fracture(fracture)
                
            self.root.after(random.randint(500, 2000), create_fracture)
            
        create_fracture()
        
        # the weight of knowing
        def update_awareness():
            texts = [
                "what was done cannot be undone",
                "the moment passed",
                "irreversible",
                "if only",
                "too late",
                "why"
            ]
            
            if random.random() < 0.01:
                text = random.choice(texts)
                size = random.randint(8, 20)
                self.canvas.itemconfig(self.what_was, text=text, font=('Arial', size))
                
                def fade_text():
                    current_size = int(self.canvas.itemcget(self.what_was, 'font').split()[1])
                    if current_size > 1:
                        self.canvas.itemconfig(self.what_was, font=('Arial', current_size - 1))
                        self.root.after(200, fade_text)
                    else:
                        self.canvas.itemconfig(self.what_was, text='')
                        
                self.root.after(1000, fade_text)
                
            self.root.after(100, update_awareness)
            
        update_awareness()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    manifestation = RemorseManifestation()
    manifestation.run()