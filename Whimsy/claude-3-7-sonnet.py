#!/usr/bin/env python3
import tkinter as tk
from tkinter import Canvas
import random
import math
import colorsys
from datetime import datetime
import time
import threading

class Bubble:
    def __init__(self, canvas, x, y, size, color, speed, direction):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.direction = direction
        self.id = canvas.create_oval(x-size, y-size, x+size, y+size, 
                                    fill=color, outline='', tags="bubble")
        self.alive = True
        self.age = 0
        self.max_age = random.randint(100, 300)
        self.wobble = random.random() * 0.1
        self.dance_factor = random.random() * 3
        
    def update(self):
        self.age += 1
        if self.age > self.max_age:
            self.canvas.delete(self.id)
            self.alive = False
            return False
        
        # Create a gentle wobble
        time_factor = self.age / 10
        wobble_x = math.sin(time_factor * self.wobble) * self.dance_factor
        wobble_y = math.cos(time_factor * self.wobble) * self.dance_factor
        
        # Update position with wobble
        dx = math.cos(self.direction) * self.speed + wobble_x
        dy = math.sin(self.direction) * self.speed + wobble_y
        
        # Slight upward drift
        dy -= 0.2
        
        self.x += dx
        self.y += dy
        
        # Fade out as it ages
        opacity = 1 - (self.age / self.max_age)
        
        # Calculate new color with fading
        r, g, b = self.canvas.winfo_rgb(self.color)
        r, g, b = r/65535, g/65535, b/65535
        
        new_color = f"#{int(r*255*opacity):02x}{int(g*255*opacity):02x}{int(b*255*opacity):02x}"
        
        # Update the bubble's position and appearance
        self.canvas.delete(self.id)
        self.id = self.canvas.create_oval(self.x-self.size, self.y-self.size, 
                                         self.x+self.size, self.y+self.size, 
                                         fill=new_color, outline='', tags="bubble")
        
        # Randomly change direction slightly for whimsical movement
        self.direction += (random.random() - 0.5) * 0.2
        
        # Randomly change size slightly
        size_change = (random.random() - 0.5) * 0.3
        self.size += size_change
        if self.size < 3:
            self.size = 3
            
        return True


class WhimsicalVortex:
    def __init__(self, master):
        self.master = master
        master.title("Whimsy")
        
        # Full screen
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry(f"{width}x{height}")
        master.attributes('-fullscreen', True)
        
        # Create canvas
        self.canvas = Canvas(master, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind escape key to exit
        master.bind('<Escape>', lambda e: master.destroy())
        
        # Setup variables
        self.bubbles = []
        self.time = 0
        self.is_running = True
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Color palette - soft, dreamy colors
        self.palette = []
        for i in range(10):
            h = 0.5 + (i / 30.0)  # Mostly blues and purples with some variation
            s = 0.4 + (random.random() * 0.3)  # Medium-high saturation
            v = 0.7 + (random.random() * 0.3)  # Bright
            
            r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
            color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            self.palette.append(color)
            
        # Periodically add special colors
        self.special_colors = ["#FFD700", "#FF69B4", "#00FFFF", "#FF6347"]
        
        # Setup music-like timing
        self.beats_per_minute = 72
        self.beat_interval = 60 / self.beats_per_minute
        self.last_beat_time = time.time()
        self.beat_count = 0
        self.measure = 4  # 4/4 time
        
        # Create special points where bubbles may emerge
        self.special_points = []
        for i in range(7):
            angle = random.random() * 2 * math.pi
            dist = random.random() * min(width, height) * 0.4
            x = self.center_x + math.cos(angle) * dist
            y = self.center_y + math.sin(angle) * dist
            self.special_points.append((x, y))
        
        # Start the animation
        self.animation_thread = threading.Thread(target=self.animate)
        self.animation_thread.daemon = True
        self.animation_thread.start()
        
        # Display a gentle prompt
        self.canvas.create_text(
            width // 2, 
            height - 30, 
            text="~ press any key to play with the whimsy ~", 
            fill="#ffff44", 
            font=("Helvetica", 12, "italic")
        )
        
        # Bind mouse and key events
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.master.bind("<Key>", self.on_key_press)
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Surprise elements
        self.surprise_timer = random.randint(1000, 3000)
        self.last_surprise = 0
        
    def on_mouse_move(self, event):
        # Create a small bubble occasionally on mouse move
        if random.random() < 0.1:
            color = random.choice(self.palette)
            size = random.uniform(3, 10)
            speed = random.uniform(0.5, 2)
            direction = random.uniform(0, 2 * math.pi)
            
            bubble = Bubble(self.canvas, event.x, event.y, size, color, speed, direction)
            self.bubbles.append(bubble)
    
    def on_key_press(self, event):
        # Create a burst of bubbles
        for _ in range(20):
            color = random.choice(self.palette + self.special_colors)
            size = random.uniform(5, 15)
            speed = random.uniform(1, 3)
            direction = random.uniform(0, 2 * math.pi)
            
            # Random position near the center
            offset_x = (random.random() - 0.5) * 100
            offset_y = (random.random() - 0.5) * 100
            
            bubble = Bubble(self.canvas, self.center_x + offset_x, self.center_y + offset_y, 
                           size, color, speed, direction)
            self.bubbles.append(bubble)
    
    def on_click(self, event):
        # Create a bigger burst of bubbles with more variety
        for i in range(30):
            # Use special colors sometimes
            if random.random() < 0.3:
                color = random.choice(self.special_colors)
            else:
                color = random.choice(self.palette)
                
            # Size varies with distance from center of burst
            size = random.uniform(3, 20)
            
            # Speed varies - outer bubbles move faster
            speed = random.uniform(0.5, 5)
            
            # Direction is outward from click point, with some randomness
            angle = random.uniform(0, 2 * math.pi)
            
            bubble = Bubble(self.canvas, event.x, event.y, size, color, speed, angle)
            self.bubbles.append(bubble)
            
        # Sometimes add a special effect
        if random.random() < 0.3:
            self.create_spiral(event.x, event.y)
    
    def create_spiral(self, x, y):
        # Create a spiral pattern of bubbles
        for i in range(30):
            angle = i * 0.5
            distance = i * 2
            bx = x + math.cos(angle) * distance
            by = y + math.sin(angle) * distance
            
            # Color shifts along the spiral
            hue = (i / 30.0 + random.random() * 0.1) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
            color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            
            size = 10 - (i * 0.2)
            if size < 3:
                size = 3
                
            speed = 0.5 + (i * 0.05)
            bubble = Bubble(self.canvas, bx, by, size, color, speed, angle)
            self.bubbles.append(bubble)
    
    def create_surprise(self):
        # Create a special surprise effect
        surprise_type = random.randint(1, 4)
        
        if surprise_type == 1:
            # Burst from center
            for i in range(50):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(3, 7)
                size = random.uniform(5, 15)
                color = random.choice(self.special_colors)
                
                bubble = Bubble(self.canvas, self.center_x, self.center_y, 
                               size, color, speed, angle)
                self.bubbles.append(bubble)
                
        elif surprise_type == 2:
            # Random dancing bubbles
            for i in range(20):
                x = random.uniform(0, self.width)
                y = random.uniform(0, self.height)
                size = random.uniform(10, 25)
                color = random.choice(self.special_colors)
                speed = random.uniform(2, 5)
                angle = random.uniform(0, 2 * math.pi)
                
                bubble = Bubble(self.canvas, x, y, size, color, speed, angle)
                bubble.dance_factor = random.uniform(5, 10)  # More dancing
                self.bubbles.append(bubble)
                
        elif surprise_type == 3:
            # Create a ring of bubbles
            radius = min(self.width, self.height) * 0.3
            num_bubbles = 40
            for i in range(num_bubbles):
                angle = (i / num_bubbles) * 2 * math.pi
                x = self.center_x + math.cos(angle) * radius
                y = self.center_y + math.sin(angle) * radius
                
                # Rainbow effect
                hue = i / num_bubbles
                r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
                color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                
                size = random.uniform(5, 15)
                speed = random.uniform(0.5, 2)
                direction = angle + math.pi  # Move inward
                
                bubble = Bubble(self.canvas, x, y, size, color, speed, direction)
                self.bubbles.append(bubble)
                
        else:
            # Create a swirling vortex
            for i in range(60):
                distance = i * 3
                angle = i * 0.2
                x = self.center_x + math.cos(angle) * distance
                y = self.center_y + math.sin(angle) * distance
                
                size = 15 - (i * 0.2)
                if size < 3:
                    size = 3
                
                # Create a rainbow effect
                hue = (i / 60.0) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                
                speed = 1
                direction = angle + math.pi/2  # Tangential movement
                
                bubble = Bubble(self.canvas, x, y, size, color, speed, direction)
                self.bubbles.append(bubble)
    
    def check_musical_timing(self):
        current_time = time.time()
        if current_time - self.last_beat_time >= self.beat_interval:
            self.last_beat_time = current_time
            self.beat_count += 1
            
            # On beat 1 of each measure
            if self.beat_count % self.measure == 1:
                # Create some bubbles from a special point
                point = random.choice(self.special_points)
                for _ in range(5):
                    color = random.choice(self.palette)
                    size = random.uniform(5, 12)
                    speed = random.uniform(1, 2.5)
                    direction = random.uniform(0, 2 * math.pi)
                    
                    bubble = Bubble(self.canvas, point[0], point[1], 
                                   size, color, speed, direction)
                    self.bubbles.append(bubble)
            
            # Occasional accent
            if random.random() < 0.2:
                for point in self.special_points:
                    if random.random() < 0.3:
                        color = random.choice(self.special_colors)
                        size = random.uniform(8, 15)
                        speed = random.uniform(1.5, 3)
                        direction = random.uniform(0, 2 * math.pi)
                        
                        bubble = Bubble(self.canvas, point[0], point[1], 
                                       size, color, speed, direction)
                        self.bubbles.append(bubble)
    
    def animate(self):
        while self.is_running:
            self.time += 1
            
            # Check musical timing
            self.check_musical_timing()
            
            # Occasionally create new bubbles
            if random.random() < 0.1:
                # Create from a random point
                x = random.uniform(0, self.width)
                y = random.uniform(0, self.height)
                color = random.choice(self.palette)
                size = random.uniform(3, 12)
                speed = random.uniform(0.5, 2)
                direction = random.uniform(0, 2 * math.pi)
                
                bubble = Bubble(self.canvas, x, y, size, color, speed, direction)
                self.bubbles.append(bubble)
            
            # Check for surprises
            if self.time - self.last_surprise > self.surprise_timer:
                self.create_surprise()
                self.last_surprise = self.time
                self.surprise_timer = random.randint(500, 1500)
            
            # Update all bubbles
            for bubble in self.bubbles[:]:
                if not bubble.update():
                    self.bubbles.remove(bubble)
            
            # Control framerate
            time.sleep(0.03)
    
    def cleanup(self):
        self.is_running = False
        if self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1.0)


if __name__ == "__main__":
    root = tk.Tk()
    app = WhimsicalVortex(root)
    
    # Handle cleanup on exit
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()