#!/usr/bin/env python3
import tkinter as tk
import random
import math
import colorsys

class RemorsePainting:
    def __init__(self, master):
        self.master = master
        master.title("∞")
        
        self.canvas = tk.Canvas(master, width=800, height=600, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.layers = []
        self.memory_threads = []
        self.decay_rate = 0.991
        self.pulse_frequency = 0
        
        self.generate_initial_layers()
        self.animate()
    
    def generate_initial_layers(self):
        for _ in range(137):
            layer = {
                'x': random.uniform(-200, 1000),
                'y': random.uniform(-200, 800),
                'size': random.uniform(1, 7),
                'color': self.generate_weighted_color(),
                'velocity_x': random.uniform(-0.3, 0.3),
                'velocity_y': random.uniform(-0.3, 0.3),
                'opacity': random.uniform(0.1, 0.7)
            }
            self.layers.append(layer)
    
    def generate_weighted_color(self):
        hue = random.random()
        saturation = random.uniform(0.3, 0.7)
        lightness = random.uniform(0.1, 0.4)
        
        r, g, b = [int(x * 255) for x in colorsys.hls_to_rgb(hue, lightness, saturation)]
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def animate(self):
        self.canvas.delete('all')
        
        self.pulse_frequency += 0.01
        pulse_effect = math.sin(self.pulse_frequency) * 0.5 + 0.5
        
        for layer in self.layers:
            layer['x'] += layer['velocity_x'] * (1 + pulse_effect)
            layer['y'] += layer['velocity_y'] * (1 + pulse_effect)
            
            layer['velocity_x'] *= self.decay_rate
            layer['velocity_y'] *= self.decay_rate
            
            layer['opacity'] *= self.decay_rate
            
            if layer['opacity'] > 0.01:
                self.canvas.create_oval(
                    layer['x'], layer['y'], 
                    layer['x'] + layer['size'], layer['y'] + layer['size'],
                    fill=layer['color'], 
                    outline='',
                    stipple='gray50' if layer['opacity'] < 0.5 else '',
                    state=tk.NORMAL
                )
        
        if random.random() < 0.05:
            self.generate_memory_thread()
        
        self.draw_memory_threads()
        
        self.master.after(33, self.animate)
    
    def generate_memory_thread(self):
        start_x = random.uniform(0, 800)
        start_y = random.uniform(0, 600)
        
        thread = {
            'points': [(start_x, start_y)],
            'life': 1.0,
            'color': self.generate_weighted_color()
        }
        
        for _ in range(random.randint(3, 12)):
            last_x, last_y = thread['points'][-1]
            next_x = last_x + random.uniform(-50, 50)
            next_y = last_y + random.uniform(-50, 50)
            thread['points'].append((next_x, next_y))
        
        self.memory_threads.append(thread)
    
    def draw_memory_threads(self):
        for thread in self.memory_threads[:]:
            if thread['life'] > 0:
                for i in range(len(thread['points']) - 1):
                    x1, y1 = thread['points'][i]
                    x2, y2 = thread['points'][i+1]
                    
                    self.canvas.create_line(
                        x1, y1, x2, y2, 
                        fill=thread['color'], 
                        width=thread['life'] * 2,
                        smooth=True,
                        splinesteps=3
                    )
                
                thread['life'] -= 0.02
            else:
                self.memory_threads.remove(thread)

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    
    try:
        painting = RemorsePainting(root)
        root.mainloop()
    except Exception:
        root.destroy()

if __name__ == '__main__':
    main()