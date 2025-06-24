import tkinter as tk
import random
import math
import time
from PIL import Image, ImageTk
import numpy as np
from collections import deque

class RemorseVisualization:
    def __init__(self, master):
        self.master = master
        master.title("Remorse")
        master.configure(bg="black")
        
        # Full screen
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        master.geometry(f"{self.width}x{self.height}")
        
        # Canvas for drawing
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, 
                               bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # State variables
        self.particles = []
        self.echo_points = deque(maxlen=200)
        self.resonance_lines = []
        self.reflection_points = []
        self.memories = []
        self.healing_paths = []
        
        # Centers of gravity - representing past actions
        self.gravity_wells = [
            (self.width * 0.3, self.height * 0.3),
            (self.width * 0.7, self.height * 0.6),
            (self.width * 0.5, self.height * 0.8)
        ]
        
        # Temporal dimension
        self.time_passed = 0
        self.acceptance_threshold = 100
        self.healing_started = False
        
        # Colors
        self.deep_blue = "#0a1a2a"
        self.midnight_blue = "#191970"
        self.dark_purple = "#301934"
        self.muted_teal = "#367588"
        self.soft_gold = "#d4af37"
        
        # Start visualization
        self.create_initial_state()
        self.animate()
        
        # Bind events
        self.canvas.bind("<Button-1>", self.acknowledge_pain)
        master.bind("<Escape>", lambda e: master.destroy())
        
        # Audio representation (silent in visual form)
        self.echo_intensity = 0
        self.resonance_frequency = 0.5
        
    def create_initial_state(self):
        # Create particles representing the weight of remorse
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(2, 8)
            speed = random.uniform(0.5, 2.5)
            opacity = random.uniform(0.3, 0.9)
            color = random.choice([self.midnight_blue, self.dark_purple, self.deep_blue])
            
            self.particles.append({
                'x': x, 'y': y, 'size': size, 'speed': speed, 
                'angle': random.uniform(0, 2*math.pi),
                'color': color, 'opacity': opacity,
                'gravity_influence': random.uniform(0.5, 1.5),
                'memory_fragments': random.randint(1, 5)
            })
        
        # Create initial reflection points - moments of realization
        for _ in range(3):
            x = random.randint(int(self.width * 0.2), int(self.width * 0.8))
            y = random.randint(int(self.height * 0.2), int(self.height * 0.8))
            size = random.randint(15, 30)
            
            self.reflection_points.append({
                'x': x, 'y': y, 'size': size, 
                'intensity': random.uniform(0.3, 0.7),
                'pulse_rate': random.uniform(0.01, 0.05),
                'pulse_state': 0
            })
            
        # Create memory fragments
        for _ in range(15):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.memories.append({
                'x': x, 'y': y,
                'fade': random.uniform(0.3, 0.9),
                'color': self.soft_gold if random.random() > 0.8 else self.muted_teal,
                'size': random.randint(3, 8),
                'persistent': random.random() > 0.7
            })
            
    def animate(self):
        self.canvas.delete("all")
        self.time_passed += 1
        
        # Draw background gradient
        self.draw_gradient_background()
        
        # Update and draw elements
        self.update_particles()
        self.draw_gravity_wells()
        self.update_reflection_points()
        self.update_echo_field()
        self.update_memories()
        
        # Conditional elements
        if self.time_passed > self.acceptance_threshold:
            if not self.healing_started:
                self.healing_started = True
                self.initialize_healing()
            self.update_healing_paths()
        
        # Schedule next frame
        self.master.after(30, self.animate)
    
    def draw_gradient_background(self):
        # Create a subtle gradient background representing the depth of feeling
        for y in range(0, self.height, 3):
            # Calculate gradient color based on position
            intensity = 1 - (y / self.height) * 0.8
            r = int(10 * intensity)
            g = int(20 * intensity)
            b = int(30 * intensity)
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            self.canvas.create_line(0, y, self.width, y, fill=color)
            
        # Add subtle texture
        for _ in range(200):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 2)
            opacity = random.uniform(0.1, 0.3)
            color_val = int(opacity * 255)
            color = f"#{color_val:02x}{color_val:02x}{color_val:02x}"
            
            self.canvas.create_oval(x-size, y-size, x+size, y+size, 
                                   fill=color, outline="")
    
    def update_particles(self):
        # Update and draw particles
        for p in self.particles:
            # Calculate gravitational influence
            dx = dy = 0
            for gx, gy in self.gravity_wells:
                dist_x = gx - p['x']
                dist_y = gy - p['y']
                distance = max(math.sqrt(dist_x**2 + dist_y**2), 50)
                force = (100 / distance) * p['gravity_influence']
                
                angle = math.atan2(dist_y, dist_x)
                dx += math.cos(angle) * force
                dy += math.sin(angle) * force
            
            # Update position with some randomness
            p['angle'] += random.uniform(-0.1, 0.1)
            p['x'] += math.cos(p['angle']) * p['speed'] + dx * 0.1
            p['y'] += math.sin(p['angle']) * p['speed'] + dy * 0.1
            
            # Contain within bounds
            if p['x'] < 0 or p['x'] > self.width:
                p['angle'] = math.pi - p['angle']
            if p['y'] < 0 or p['y'] > self.height:
                p['angle'] = -p['angle']
            
            # Draw particle
            size = p['size']
            opacity = int(p['opacity'] * 255)
            color = p['color'][:-2] + f"{opacity:02x}"
            
            self.canvas.create_oval(p['x']-size, p['y']-size, 
                                   p['x']+size, p['y']+size,
                                   fill=color, outline="")
            
            # Sometimes leave an echo
            if random.random() < 0.05:
                self.echo_points.append((p['x'], p['y'], p['color'], p['size']/2))
    
    def draw_gravity_wells(self):
        # Draw gravity wells - representing the actions causing remorse
        for i, (x, y) in enumerate(self.gravity_wells):
            # Draw concentric circles
            max_radius = 80 + 20 * math.sin(self.time_passed * 0.02 + i)
            for r in range(10, int(max_radius), 10):
                opacity = 0.2 - (r / max_radius) * 0.2
                color_val = int(opacity * 255)
                color = f"#{color_val:02x}{color_val:02x}{color_val+20:02x}"
                
                self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                      outline=color, width=2)
    
    def update_reflection_points(self):
        # Update and draw reflection points
        for point in self.reflection_points:
            point['pulse_state'] += point['pulse_rate']
            
            # Calculate pulsing size
            pulse_factor = 0.5 + 0.5 * math.sin(point['pulse_state'])
            current_size = point['size'] * (0.8 + 0.4 * pulse_factor)
            
            # Draw glow effect
            for r in range(int(current_size), 0, -5):
                opacity = (r / current_size) * point['intensity'] * 0.8
                color_val = int(opacity * 255)
                color = f"#{color_val:02x}{color_val:02x}{color_val+40:02x}"
                
                self.canvas.create_oval(
                    point['x'] - r, point['y'] - r,
                    point['x'] + r, point['y'] + r,
                    outline=color, width=2)
            
            # Draw center
            center_size = current_size / 4
            self.canvas.create_oval(
                point['x'] - center_size, point['y'] - center_size,
                point['x'] + center_size, point['y'] + center_size,
                fill=self.muted_teal, outline="")
    
    def update_echo_field(self):
        # Draw echo points
        for i, (x, y, color, size) in enumerate(self.echo_points):
            # Calculate opacity based on age
            age_factor = 1 - (i / len(self.echo_points))
            opacity = int(age_factor * 255 * 0.7)
            
            if opacity > 0:
                color = color[:-2] + f"{opacity:02x}"
                self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                      fill=color, outline="")
        
        # Draw resonance lines
        if random.random() < 0.1:
            self.resonance_lines = []
            num_lines = random.randint(3, 8)
            
            for _ in range(num_lines):
                x1 = random.randint(0, self.width)
                y1 = random.randint(0, self.height)
                length = random.randint(50, 200)
                angle = random.uniform(0, 2*math.pi)
                
                x2 = x1 + math.cos(angle) * length
                y2 = y1 + math.sin(angle) * length
                
                self.resonance_lines.append((x1, y1, x2, y2))
        
        # Draw existing resonance lines with fading effect
        for x1, y1, x2, y2 in self.resonance_lines:
            opacity = random.uniform(0.1, 0.3)
            color_val = int(opacity * 255)
            color = f"#{color_val:02x}{color_val+10:02x}{color_val+20:02x}"
            
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)
    
    def update_memories(self):
        # Draw memory fragments
        for memory in self.memories:
            if random.random() < 0.01 and not memory['persistent']:
                # Occasionally fade some memories
                memory['fade'] = max(0.1, memory['fade'] - 0.1)
            
            # Slightly move memories
            memory['x'] += random.uniform(-1, 1)
            memory['y'] += random.uniform(-1, 1)
            
            # Draw with appropriate opacity
            opacity = int(memory['fade'] * 255)
            color = memory['color'][:-2] + f"{opacity:02x}"
            
            self.canvas.create_oval(
                memory['x'] - memory['size'], memory['y'] - memory['size'],
                memory['x'] + memory['size'], memory['y'] + memory['size'],
                fill=color, outline="")
            
            # Connect some memories to gravity wells
            if random.random() < 0.2:
                gx, gy = random.choice(self.gravity_wells)
                opacity = int(memory['fade'] * 255 * 0.3)
                color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
                
                self.canvas.create_line(
                    memory['x'], memory['y'], gx, gy,
                    fill=color, width=1, dash=(3, 5))
    
    def initialize_healing(self):
        # Initialize healing paths
        for _ in range(7):
            start_x, start_y = random.choice(self.gravity_wells)
            end_x = random.randint(0, self.width)
            end_y = random.randint(0, self.height)
            
            # Create a meandering path
            path_points = [(start_x, start_y)]
            current_x, current_y = start_x, start_y
            
            # Generate path points
            steps = random.randint(5, 15)
            for i in range(steps):
                # Direction towards destination with some randomness
                dx = (end_x - current_x) / (steps - i) + random.uniform(-30, 30)
                dy = (end_y - current_y) / (steps - i) + random.uniform(-30, 30)
                
                current_x += dx
                current_y += dy
                path_points.append((current_x, current_y))
            
            # Add final point
            path_points.append((end_x, end_y))
            
            self.healing_paths.append({
                'points': path_points,
                'progress': 0,
                'speed': random.uniform(0.005, 0.02),
                'color': self.soft_gold if random.random() > 0.5 else self.muted_teal,
                'width': random.uniform(1.5, 3)
            })
    
    def update_healing_paths(self):
        # Update and draw healing paths
        complete_paths = []
        
        for path in self.healing_paths:
            # Update progress
            path['progress'] = min(1.0, path['progress'] + path['speed'])
            
            # Calculate how much of the path to draw
            points = path['points']
            if len(points) >= 2:
                num_segments = len(points) - 1
                segments_to_draw = max(1, math.ceil(num_segments * path['progress']))
                
                # Draw path segments
                for i in range(segments_to_draw):
                    x1, y1 = points[i]
                    x2, y2 = points[i+1]
                    
                    # Calculate segment progress
                    segment_progress = 1.0
                    if i == segments_to_draw - 1 and path['progress'] < 1.0:
                        # For the last segment, calculate partial progress
                        full_segments = path['progress'] * num_segments
                        segment_progress = full_segments - math.floor(full_segments)
                        
                        # Calculate partial endpoint
                        if segment_progress < 1.0:
                            x2 = x1 + (x2 - x1) * segment_progress
                            y2 = y1 + (y2 - y1) * segment_progress
                    
                    # Draw segment
                    opacity = int(255 * (0.5 + 0.5 * path['progress']))
                    color = path['color'][:-2] + f"{opacity:02x}"
                    
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=color, width=path['width'],
                        capstyle=tk.ROUND, joinstyle=tk.ROUND)
            
            # Mark completed paths
            if path['progress'] >= 1.0:
                complete_paths.append(path)
                
                # Create a small glow at the end point
                x, y = path['points'][-1]
                for r in range(15, 0, -3):
                    opacity = (r / 15) * 0.7
                    color_val = int(opacity * 255)
                    color = f"#{color_val+40:02x}{color_val+40:02x}{color_val:02x}"
                    
                    self.canvas.create_oval(
                        x-r, y-r, x+r, y+r,
                        outline=color, width=2)
        
        # Remove completed paths and add new ones
        for path in complete_paths:
            self.healing_paths.remove(path)
            
            if random.random() < 0.7 and len(self.healing_paths) < 10:
                self.initialize_healing()
    
    def acknowledge_pain(self, event):
        # Add a reflection point where clicked
        x, y = event.x, event.y
        
        # Create ripple effect
        for r in range(0, 100, 5):
            opacity = (1 - r/100) * 0.5
            color_val = int(opacity * 255)
            color = f"#{color_val+20:02x}{color_val+20:02x}{color_val+40:02x}"
            
            self.canvas.create_oval(
                x-r, y-r, x+r, y+r,
                outline=color, width=2)
        
        # Add new reflection point
        self.reflection_points.append({
            'x': x, 'y': y, 'size': random.randint(15, 25),
            'intensity': random.uniform(0.5, 0.9),
            'pulse_rate': random.uniform(0.02, 0.06),
            'pulse_state': 0
        })
        
        # Increase healing probability
        self.acceptance_threshold = max(0, self.acceptance_threshold - 10)
        
        # Start healing if threshold reached
        if not self.healing_started and self.time_passed > self.acceptance_threshold:
            self.healing_started = True
            self.initialize_healing()

def main():
    root = tk.Tk()
    app = RemorseVisualization(root)
    root.mainloop()

if __name__ == "__main__":
    main()
