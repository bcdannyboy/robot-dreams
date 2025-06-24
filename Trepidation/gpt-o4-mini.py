#!/usr/bin/env python3
import tkinter as tk
import random
import math
import time

class TrepidationApp:
    def __init__(self):
        # Initialize window
        self.root = tk.Tk()
        self.root.title("Trepidation")
        # Fixed size for consistent visual experience
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack()
        # Track time for oscillations
        self.start_time = time.time()
        # Begin update loop
        self.update()
        self.root.mainloop()

    def update(self):
        # Clear previous frame
        self.canvas.delete("all")
        t = time.time() - self.start_time

        # Background shade oscillates with subtle randomness
        shade = int(20 + 10 * math.sin(t * 0.5) + random.uniform(-5, 5))
        shade = max(0, min(255, shade))
        bg = f"#{shade:02x}{shade:02x}{shade:02x}"
        self.canvas.configure(bg=bg)

        # Compute center with slight jitter oscillations
        cx = self.width / 2 + random.uniform(-10, 10) * math.sin(t * 1.3)
        cy = self.height / 2 + random.uniform(-10, 10) * math.cos(t * 1.7)

        # Base radius oscillates; then apply randomness for trembling effect
        base_radius = 30 + 10 * math.sin(t * 0.8)
        radius = abs(base_radius) + random.uniform(-5, 5)

        # Circle color slightly lighter than background, with flicker
        shade2 = int(min(255, shade + 40 + random.uniform(-20, 20)))
        fill = f"#{shade2:02x}{shade2:02x}{shade2:02x}"
        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=fill, outline="")

        # Draw spiky lines radiating from center with jittered endpoints
        num_lines = random.randint(8, 16)
        for _ in range(num_lines):
            angle = random.uniform(0, 2 * math.pi)
            length = random.uniform(radius + 20, radius + 60)
            ex = cx + length * math.cos(angle) + random.uniform(-5, 5)
            ey = cy + length * math.sin(angle) + random.uniform(-5, 5)
            shade_line = int(min(255, shade + random.uniform(20, 60)))
            color = f"#{shade_line:02x}{shade_line:02x}{shade_line:02x}"
            self.canvas.create_line(cx, cy, ex, ey, fill=color, width=1)

        # Occasional flicker: random rectangles appearing/disappearing
        if random.random() < 0.05:
            x1 = random.uniform(0, self.width)
            y1 = random.uniform(0, self.height)
            x2 = x1 + random.uniform(20, 100)
            y2 = y1 + random.uniform(20, 100)
            shade3 = int(min(255, shade + random.uniform(30, 80)))
            rect_color = f"#{shade3:02x}{shade3:02x}{shade3:02x}"
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=rect_color)

        # Schedule next frame
        self.root.after(50, self.update)

if __name__ == "__main__":
    TrepidationApp()
