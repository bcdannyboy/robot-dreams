import tkinter as tk
import random
import math
import time
from threading import Thread
import colorsys

class WhimsyCanvas:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("...")
        self.root.configure(bg='#faf8f3')
        
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='#faf8f3', highlightthickness=0)
        self.canvas.pack()
        
        self.thoughts = []
        self.bubbles = []
        self.spirals = []
        self.dancing_points = []
        self.ephemeral_traces = []
        
        self.time_wobble = 0
        self.hue_drift = random.random()
        
        # initialize dancing points
        for _ in range(7):
            self.dancing_points.append({
                'x': random.randint(100, self.width-100),
                'y': random.randint(100, self.height-100),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'phase': random.uniform(0, math.pi * 2),
                'radius': random.uniform(3, 8),
                'trail': []
            })
        
        self.root.bind('<Motion>', self.on_mouse_move)
        self.root.bind('<Button-1>', self.on_click)
        
        self.animate()
        self.root.mainloop()
    
    def on_mouse_move(self, event):
        if random.random() < 0.02:
            self.ephemeral_traces.append({
                'x': event.x,
                'y': event.y,
                'age': 0,
                'drift_x': random.uniform(-0.5, 0.5),
                'drift_y': random.uniform(-0.5, 0.5)
            })
    
    def on_click(self, event):
        # birth a thought
        words = ['?', '!', '~', '*', '...', '♪', '◊', '○', '☆', '¿']
        self.thoughts.append({
            'x': event.x,
            'y': event.y,
            'text': random.choice(words),
            'age': 0,
            'wobble': random.uniform(0, math.pi * 2),
            'size': random.randint(8, 20),
            'color': self.get_whimsy_color()
        })
        
        # and some bubbles
        for _ in range(random.randint(3, 8)):
            self.bubbles.append({
                'x': event.x + random.uniform(-20, 20),
                'y': event.y + random.uniform(-20, 20),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-3, -1),
                'size': random.uniform(5, 15),
                'age': 0,
                'pop_time': random.uniform(40, 100)
            })
        
        # occasionally a spiral
        if random.random() < 0.3:
            self.spirals.append({
                'center_x': event.x,
                'center_y': event.y,
                'angle': 0,
                'radius': 0,
                'max_radius': random.uniform(50, 150),
                'speed': random.uniform(0.05, 0.15),
                'direction': random.choice([1, -1])
            })
    
    def get_whimsy_color(self):
        hue = (self.hue_drift + random.uniform(-0.1, 0.1)) % 1
        saturation = random.uniform(0.3, 0.7)
        lightness = random.uniform(0.4, 0.8)
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
    
    def animate(self):
        self.canvas.delete('all')
        self.time_wobble += 0.05
        self.hue_drift += 0.001
        
        # update and draw ephemeral traces
        for trace in self.ephemeral_traces[:]:
            trace['age'] += 1
            trace['x'] += trace['drift_x']
            trace['y'] += trace['drift_y']
            
            if trace['age'] < 30:
                opacity = 1 - (trace['age'] / 30)
                size = 2 + math.sin(trace['age'] * 0.3) * 2
                self.canvas.create_oval(
                    trace['x'] - size, trace['y'] - size,
                    trace['x'] + size, trace['y'] + size,
                    fill=self.get_whimsy_color(), outline='', 
                    tags='trace'
                )
            else:
                self.ephemeral_traces.remove(trace)
        
        # update and draw dancing points
        for point in self.dancing_points:
            point['phase'] += 0.1
            
            # wandering motion
            point['vx'] += random.uniform(-0.2, 0.2)
            point['vy'] += random.uniform(-0.2, 0.2)
            point['vx'] *= 0.95
            point['vy'] *= 0.95
            
            point['x'] += point['vx'] + math.sin(point['phase']) * 2
            point['y'] += point['vy'] + math.cos(point['phase'] * 0.7) * 2
            
            # gentle boundaries
            if point['x'] < 50: point['vx'] += 0.5
            if point['x'] > self.width - 50: point['vx'] -= 0.5
            if point['y'] < 50: point['vy'] += 0.5
            if point['y'] > self.height - 50: point['vy'] -= 0.5
            
            # trail
            point['trail'].append((point['x'], point['y']))
            if len(point['trail']) > 20:
                point['trail'].pop(0)
            
            # draw trail
            for i, (tx, ty) in enumerate(point['trail']):
                fade = i / len(point['trail'])
                size = point['radius'] * fade
                self.canvas.create_oval(
                    tx - size, ty - size,
                    tx + size, ty + size,
                    fill='', outline=self.get_whimsy_color(),
                    width=1, tags='trail'
                )
            
            # draw point
            wobble_x = math.sin(self.time_wobble + point['phase']) * 3
            wobble_y = math.cos(self.time_wobble * 1.3 + point['phase']) * 3
            self.canvas.create_oval(
                point['x'] - point['radius'] + wobble_x,
                point['y'] - point['radius'] + wobble_y,
                point['x'] + point['radius'] + wobble_x,
                point['y'] + point['radius'] + wobble_y,
                fill=self.get_whimsy_color(), outline='',
                tags='point'
            )
        
        # update and draw thoughts
        for thought in self.thoughts[:]:
            thought['age'] += 1
            thought['y'] -= 0.5
            thought['wobble'] += 0.1
            
            if thought['age'] < 100:
                x_offset = math.sin(thought['wobble']) * 10
                opacity = 1 - (thought['age'] / 100)
                
                self.canvas.create_text(
                    thought['x'] + x_offset,
                    thought['y'],
                    text=thought['text'],
                    font=('Arial', thought['size']),
                    fill=thought['color'],
                    tags='thought'
                )
            else:
                self.thoughts.remove(thought)
        
        # update and draw bubbles
        for bubble in self.bubbles[:]:
            bubble['age'] += 1
            bubble['x'] += bubble['vx']
            bubble['y'] += bubble['vy']
            bubble['vy'] += 0.1  # gentle gravity
            
            if bubble['age'] < bubble['pop_time']:
                wobble = math.sin(bubble['age'] * 0.2) * 2
                self.canvas.create_oval(
                    bubble['x'] - bubble['size'] + wobble,
                    bubble['y'] - bubble['size'],
                    bubble['x'] + bubble['size'] + wobble,
                    bubble['y'] + bubble['size'],
                    fill='', outline=self.get_whimsy_color(),
                    width=1, tags='bubble'
                )
            else:
                # pop!
                for _ in range(5):
                    self.ephemeral_traces.append({
                        'x': bubble['x'],
                        'y': bubble['y'],
                        'age': 0,
                        'drift_x': random.uniform(-3, 3),
                        'drift_y': random.uniform(-3, 3)
                    })
                self.bubbles.remove(bubble)
        
        # update and draw spirals
        for spiral in self.spirals[:]:
            spiral['angle'] += spiral['speed'] * spiral['direction']
            spiral['radius'] += 1
            
            if spiral['radius'] < spiral['max_radius']:
                points = []
                for i in range(20):
                    angle = spiral['angle'] - i * 0.1
                    radius = spiral['radius'] - i * 2
                    if radius > 0:
                        x = spiral['center_x'] + math.cos(angle) * radius
                        y = spiral['center_y'] + math.sin(angle) * radius
                        points.extend([x, y])
                
                if len(points) > 4:
                    self.canvas.create_line(
                        points,
                        fill=self.get_whimsy_color(),
                        width=2,
                        smooth=True,
                        tags='spiral'
                    )
            else:
                self.spirals.remove(spiral)
        
        # occasional spontaneous events
        if random.random() < 0.01:
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                self.ephemeral_traces.append({
                    'x': x,
                    'y': y,
                    'age': 0,
                    'drift_x': math.cos(rad) * 3,
                    'drift_y': math.sin(rad) * 3
                })
        
        self.root.after(30, self.animate)

if __name__ == '__main__':
    WhimsyCanvas()