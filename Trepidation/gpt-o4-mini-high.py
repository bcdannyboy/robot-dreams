#!/usr/bin/env python3
import tkinter as tk
import random

# Dimensions and flicker settings
WIDTH, HEIGHT = 800, 600
BASE_BRIGHTNESS = 20
FLICKER_AMPLITUDE = 20
NUM_GLIMMERS = 60

class TrepidationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trepidation")
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()
        self.center = (WIDTH // 2, HEIGHT // 2)
        self.update()

    def update(self):
        # Clear previous frame
        self.canvas.delete("all")
        # Random flicker of background darkness
        b = BASE_BRIGHTNESS + random.randint(-FLICKER_AMPLITUDE, FLICKER_AMPLITUDE)
        b = max(0, min(255, b))
        bg = f'#{b:02x}{b:02x}{b:02x}'
        self.canvas.config(bg=bg)
        # Sparse, fleeting glimmers in the void
        for _ in range(NUM_GLIMMERS):
            if random.random() < 0.05:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                r = random.randint(1, 5)
                shade = random.randint(30, 100)
                color = f'#{shade:02x}{shade:02x}{shade:02x}'
                self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color)
        # A single form at the center, trembling
        cx, cy = self.center
        jitter_x = random.randint(-3, 3)
        jitter_y = random.randint(-3, 3)
        r = 8
        self.canvas.create_oval(
            cx + jitter_x - r, cy + jitter_y - r,
            cx + jitter_x + r, cy + jitter_y + r,
            fill='black', outline=''
        )
        # Next frame
        self.root.after(50, self.update)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    TrepidationApp().run()
