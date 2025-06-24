#!/usr/bin/env python3
import tkinter as tk
import random
import math
import colorsys
from threading import Thread
from queue import Queue
import time

class TrepidationCanvas:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        
        self.uncertainty_streams = []
        self.anticipation_particles = []
        self.resonance_queue = Queue()
        
        self.oscillation_baseline = 0.5
        self.perceptual_tremor = 1.0
        
        self._initialize_emotional_topology()
        self._initiate_recursive_emergence()

    def _initialize_emotional_topology(self):
        for _ in range(random.randint(50, 150)):
            stream = {
                'x': random.uniform(0, self.width),
                'y': random.uniform(0, self.height),
                'velocity': random.uniform(0.1, 2.0),
                'amplitude': random.uniform(0.5, 3.0),
                'frequency': random.uniform(0.01, 0.1),
                'phase': random.uniform(0, math.pi * 2)
            }
            self.uncertainty_streams.append(stream)
        
        for _ in range(random.randint(200, 500)):
            particle = {
                'x': random.uniform(0, self.width),
                'y': random.uniform(0, self.height),
                'size': random.uniform(1, 5),
                'opacity': random.uniform(0.1, 0.5),
                'drift': random.uniform(-0.5, 0.5),
                'oscillation': random.uniform(0.01, 0.1)
            }
            self.anticipation_particles.append(particle)

    def _modulate_perceptual_resonance(self):
        while True:
            self.perceptual_tremor += random.uniform(-0.1, 0.1)
            self.perceptual_tremor = max(0.5, min(self.perceptual_tremor, 2.0))
            time.sleep(random.uniform(1, 3))

    def _initiate_recursive_emergence(self):
        resonance_thread = Thread(target=self._modulate_perceptual_resonance)
        resonance_thread.daemon = True
        resonance_thread.start()
        
        self.master.after(50, self._render_emotional_landscape)

    def _render_emotional_landscape(self):
        self.canvas.delete('all')
        
        for stream in self.uncertainty_streams:
            hue = math.sin(stream['phase']) * 0.5 + 0.5
            r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.8, 0.7)]
            
            stream['phase'] += stream['frequency'] * self.perceptual_tremor
            displacement = stream['amplitude'] * math.sin(stream['phase'])
            
            x = stream['x'] + displacement * stream['velocity']
            y = stream['y'] + displacement * stream['velocity']
            
            self.canvas.create_line(
                stream['x'], stream['y'], x, y, 
                fill=f'#{r:02x}{g:02x}{b:02x}', 
                width=max(0.1, abs(displacement) * 0.5)
            )
            
            stream['x'], stream['y'] = x, y
            if x < 0 or x > self.width or y < 0 or y > self.height:
                stream['x'] = random.uniform(0, self.width)
                stream['y'] = random.uniform(0, self.height)
        
        for particle in self.anticipation_particles:
            particle['x'] += particle['drift'] * self.perceptual_tremor
            particle['y'] += math.sin(particle['oscillation'] * time.time()) * 0.5
            
            opacity = int(particle['opacity'] * 255)
            size = particle['size'] * self.perceptual_tremor
            
            self.canvas.create_oval(
                particle['x'], particle['y'], 
                particle['x'] + size, particle['y'] + size, 
                fill=f'rgba(255, 255, 255, {opacity/255})', 
                outline=''
            )
            
            if (particle['x'] < 0 or particle['x'] > self.width or 
                particle['y'] < 0 or particle['y'] > self.height):
                particle['x'] = random.uniform(0, self.width)
                particle['y'] = random.uniform(0, self.height)
        
        self.master.after(50, self._render_emotional_landscape)

def manifest_trepidation():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='black')
    
    canvas_instance = TrepidationCanvas(root)
    
    def exit_fullscreen(event):
        root.destroy()
    
    root.bind('<Escape>', exit_fullscreen)
    root.mainloop()

if __name__ == '__main__':
    manifest_trepidation()