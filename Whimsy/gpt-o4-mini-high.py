#!/usr/bin/env python3
import tkinter as tk
import random
import math

# A whimsical dance of shapes and colors

WIDTH, HEIGHT = 800, 600
SHAPE_COUNT = 30
PALETTE = ["#FFC0CB", "#FFB6C1", "#E0FFFF", "#FFFACD", "#E6E6FA", "#F0FFF0", "#FFE4E1", "#F5DEB3"]

class WhimsyShape:
    def __init__(self, canvas):
        self.canvas = canvas
        self.type = random.choice(['circle', 'star'])
        self.size = random.uniform(20, 60)
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(0.5, 2)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.color = random.choice(PALETTE)
        self.id = None

    def draw(self):
        if self.id:
            self.canvas.delete(self.id)
        if self.type == 'circle':
            self.id = self.canvas.create_oval(
                self.x - self.size/2, self.y - self.size/2,
                self.x + self.size/2, self.y + self.size/2,
                fill=self.color, outline=""
            )
        else:
            points = []
            r_outer = self.size / 2
            r_inner = r_outer * 0.5
            for i in range(10):
                angle = math.pi/5 * i
                r = r_outer if i % 2 == 0 else r_inner
                px = self.x + math.cos(angle) * r
                py = self.y + math.sin(angle) * r
                points.extend([px, py])
            self.id = self.canvas.create_polygon(points, fill=self.color, outline="")

    def update(self):
        # gentle drift with occasional whim
        self.x += self.dx + random.uniform(-0.3, 0.3)
        self.y += self.dy + random.uniform(-0.3, 0.3)
        # wrap-around
        if self.x < -self.size: self.x = WIDTH + self.size
        if self.x > WIDTH + self.size: self.x = -self.size
        if self.y < -self.size: self.y = HEIGHT + self.size
        if self.y > HEIGHT + self.size: self.y = -self.size
        self.draw()

def animate(shapes, canvas):
    for s in shapes:
        s.update()
    canvas.after(50, animate, shapes, canvas)

def main():
    root = tk.Tk()
    root.title("Whimsy")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=random.choice(PALETTE))
    canvas.pack()
    shapes = [WhimsyShape(canvas) for _ in range(SHAPE_COUNT)]
    animate(shapes, canvas)
    root.mainloop()

if __name__ == "__main__":
    main()
