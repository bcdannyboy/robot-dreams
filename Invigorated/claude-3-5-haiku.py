#!/usr/bin/env python3
import tkinter as tk
import math
import random
import colorsys

class InvigoratedEmotion:
    def __init__(self, master):
        self.master = master
        master.title("Invigorated")
        
        self.canvas = tk.Canvas(master, width=800, height=600, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.pulse_points = []
        self.energy_streams = []
        self.core_vibration = 0
        
        self.create_resonance_core()
        self.animate_emotion()
        
    def create_resonance_core(self):
        # The core of invigoration - a dynamic, pulsating center
        for _ in range(50):
            x = 400 + random.gauss(0, 100)
            y = 300 + random.gauss(0, 100)
            radius = random.uniform(5, 20)
            hue = random.random()
            
            point = {
                'x': x,
                'y': y,
                'radius': radius,
                'hue': hue,
                'growth_rate': random.uniform(0.5, 2),
                'direction': random.choice([-1, 1])
            }
            self.pulse_points.append(point)
        
    def generate_energy_stream(self):
        # Streams of energy radiating from the core
        start_x = 400 + random.gauss(0, 200)
        start_y = 300 + random.gauss(0, 200)
        
        stream = {
            'x': start_x,
            'y': start_y,
            'length': random.uniform(50, 300),
            'angle': random.uniform(0, 2 * math.pi),
            'width': random.uniform(1, 5),
            'color_shift': random.random(),
            'vibration_frequency': random.uniform(0.1, 1)
        }
        self.energy_streams.append(stream)
        
    def animate_emotion(self):
        self.canvas.delete('all')
        self.core_vibration += 0.1
        
        # Pulse points - representation of internal dynamism
        for point in self.pulse_points:
            # Oscillating growth and color
            point['radius'] += point['growth_rate'] * point['direction']
            if point['radius'] > 25 or point['radius'] < 5:
                point['direction'] *= -1
            
            # HSV color transformation
            hue = (point['hue'] + 0.01) % 1
            point['hue'] = hue
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            color = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
            
            self.canvas.create_oval(
                point['x'] - point['radius'], 
                point['y'] - point['radius'], 
                point['x'] + point['radius'], 
                point['y'] + point['radius'], 
                fill=color, 
                outline=''
            )
        
        # Manage energy streams
        if len(self.energy_streams) < 20:
            self.generate_energy_stream()
        
        for stream in self.energy_streams[:]:
            # Dynamic movement and color shifting
            stream['x'] += math.cos(stream['angle']) * 3
            stream['y'] += math.sin(stream['angle']) * 3
            
            # Color modulation
            stream['color_shift'] = (stream['color_shift'] + 0.05) % 1
            rgb = colorsys.hsv_to_rgb(stream['color_shift'], 0.8, 0.9)
            color = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
            
            # Drawing energy streams with vibrational width
            width = stream['width'] * (1 + math.sin(self.core_vibration * stream['vibration_frequency']) * 0.5)
            self.canvas.create_line(
                stream['x'], stream['y'], 
                stream['x'] + math.cos(stream['angle']) * stream['length'],
                stream['y'] + math.sin(stream['angle']) * stream['length'],
                fill=color, 
                width=width
            )
            
            # Remove streams that go out of bounds
            if (stream['x'] < -200 or stream['x'] > 1000 or 
                stream['y'] < -200 or stream['y'] > 800):
                self.energy_streams.remove(stream)
        
        # Recursive animation
        self.master.after(50, self.animate_emotion)

def main():
    root = tk.Tk()
    root.geometry('800x600')
    app = InvigoratedEmotion(root)
    root.mainloop()

if __name__ == '__main__':
    main()