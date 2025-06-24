import tkinter as tk
import random
import math
import time
from threading import Thread
import colorsys

class InvigoratedCanvas:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.configure(bg='black')
        
        self.width = 800
        self.height = 600
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='black', highlightthickness=0)
        self.canvas.pack()
        
        self.particles = []
        self.pulse_centers = []
        self.time = 0
        self.energy_threshold = 0.3
        self.burst_probability = 0.02
        
        self.colors = ['#00ff88', '#00ffcc', '#00ffff', '#00ccff', '#0088ff', '#ff00ff', '#ff00aa', '#ffaa00']
        
        self.running = True
        self.update_thread = Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        self.root.bind('<Motion>', self.on_mouse_move)
        self.root.bind('<Button-1>', self.on_click)
        
        self.animate()
        
    def on_mouse_move(self, event):
        if random.random() < 0.3:
            self.create_particle(event.x, event.y, triggered=True)
            
    def on_click(self, event):
        self.create_burst(event.x, event.y)
        
    def create_particle(self, x, y, triggered=False):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8) if triggered else random.uniform(1, 4)
        
        particle = {
            'x': x,
            'y': y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'life': 1.0,
            'decay': random.uniform(0.005, 0.02),
            'color': random.choice(self.colors),
            'size': random.uniform(1, 4),
            'oscillation': random.uniform(0, 2 * math.pi),
            'oscillation_speed': random.uniform(0.1, 0.3),
            'trail': []
        }
        
        self.particles.append(particle)
        
    def create_burst(self, x, y):
        num_particles = random.randint(20, 40)
        for i in range(num_particles):
            angle = (2 * math.pi * i) / num_particles + random.uniform(-0.3, 0.3)
            speed = random.uniform(3, 10)
            
            particle = {
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'decay': random.uniform(0.01, 0.03),
                'color': random.choice(self.colors),
                'size': random.uniform(2, 6),
                'oscillation': random.uniform(0, 2 * math.pi),
                'oscillation_speed': random.uniform(0.2, 0.5),
                'trail': []
            }
            
            self.particles.append(particle)
            
        self.pulse_centers.append({
            'x': x,
            'y': y,
            'radius': 0,
            'max_radius': random.uniform(100, 200),
            'speed': random.uniform(2, 5)
        })
        
    def update_loop(self):
        while self.running:
            self.time += 0.05
            
            # Spontaneous generation
            if random.random() < self.burst_probability:
                x = random.randint(50, self.width - 50)
                y = random.randint(50, self.height - 50)
                self.create_burst(x, y)
            
            # Update particles
            for particle in self.particles[:]:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                
                # Oscillation
                particle['oscillation'] += particle['oscillation_speed']
                particle['vx'] += math.sin(particle['oscillation']) * 0.3
                particle['vy'] += math.cos(particle['oscillation']) * 0.3
                
                # Attraction to center with variation
                cx, cy = self.width / 2, self.height / 2
                dx, dy = cx - particle['x'], cy - particle['y']
                dist = math.sqrt(dx**2 + dy**2)
                if dist > 100:
                    particle['vx'] += dx / dist * 0.1
                    particle['vy'] += dy / dist * 0.1
                
                # Energy transfer
                for other in self.particles:
                    if other != particle:
                        dx, dy = other['x'] - particle['x'], other['y'] - particle['y']
                        dist = math.sqrt(dx**2 + dy**2)
                        if dist < 30 and dist > 0:
                            repel = 1 / dist
                            particle['vx'] -= dx / dist * repel
                            particle['vy'] -= dy / dist * repel
                
                # Trail
                particle['trail'].append((particle['x'], particle['y'], particle['life']))
                if len(particle['trail']) > 10:
                    particle['trail'].pop(0)
                
                # Life decay
                particle['life'] -= particle['decay']
                
                # Remove dead particles
                if particle['life'] <= 0:
                    self.particles.remove(particle)
                    
            # Update pulse centers
            for pulse in self.pulse_centers[:]:
                pulse['radius'] += pulse['speed']
                if pulse['radius'] > pulse['max_radius']:
                    self.pulse_centers.remove(pulse)
                    
            time.sleep(0.02)
            
    def animate(self):
        if not self.running:
            return
            
        self.canvas.delete('all')
        
        # Draw pulse waves
        for pulse in self.pulse_centers:
            alpha = 1 - (pulse['radius'] / pulse['max_radius'])
            if alpha > 0:
                color = self.get_faded_color('#00ffff', alpha * 0.3)
                self.canvas.create_oval(
                    pulse['x'] - pulse['radius'], pulse['y'] - pulse['radius'],
                    pulse['x'] + pulse['radius'], pulse['y'] + pulse['radius'],
                    outline=color, width=2
                )
        
        # Draw particles and trails
        for particle in self.particles:
            # Draw trail
            for i, (tx, ty, tlife) in enumerate(particle['trail']):
                if i > 0:
                    prev_x, prev_y, _ = particle['trail'][i-1]
                    alpha = tlife * (i / len(particle['trail']))
                    color = self.get_faded_color(particle['color'], alpha)
                    self.canvas.create_line(prev_x, prev_y, tx, ty, fill=color, width=1)
            
            # Draw particle
            x, y = particle['x'], particle['y']
            size = particle['size'] * particle['life']
            color = self.get_faded_color(particle['color'], particle['life'])
            
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline=''
            )
            
        # Continue animation
        self.root.after(16, self.animate)
        
    def get_faded_color(self, color, alpha):
        # Convert hex to RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # Fade to black
        r = int(r * alpha)
        g = int(g * alpha)
        b = int(b * alpha)
        
        return f'#{r:02x}{g:02x}{b:02x}'
        
    def run(self):
        self.root.mainloop()
        self.running = False

if __name__ == '__main__':
    canvas = InvigoratedCanvas()
    canvas.run()