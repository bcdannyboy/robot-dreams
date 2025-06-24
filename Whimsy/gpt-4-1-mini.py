# emotion.py
import tkinter as tk
import random
import math
import time

# A visual dance of ephemeral colors and shapes.
# Shapes drift like fleeting thoughts, colors flicker unpredictably,
# and small unpredictable bursts of motion sprinkle the canvas,
# a hint of delightful unpredictability and lightheartedness.

WIDTH, HEIGHT = 800, 600
SHAPE_COUNT = 20
MAX_VEL = 2

def rnd_color():
    # Pastel-like hues, playful yet soft, with a flicker of unpredictable saturation
    base = random.choice([
        (255, 182, 193),  # lightpink
        (176, 224, 230),  # powderblue
        (255, 255, 224),  # lightyellow
        (221, 160, 221),  # plum
        (144, 238, 144),  # lightgreen
        (255, 228, 196),  # bisque
        (240, 230, 140),  # khaki
    ])
    # subtle random flicker in brightness, like a thought suddenly glowing
    flicker = lambda c: min(255, max(100, int(c + random.gauss(0, 20))))
    return "#%02x%02x%02x" % tuple(flicker(c) for c in base)

def lerp(a, b, t):
    return a + (b - a) * t

class Shape:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-MAX_VEL, MAX_VEL)
        self.vy = random.uniform(-MAX_VEL, MAX_VEL)
        self.size = random.uniform(20, 60)
        self.color = rnd_color()
        self.shape_type = random.choice(['circle', 'triangle', 'star'])
        self.opacity = random.uniform(0.4, 0.9)
        self.id = None
        self.star_points = self.calc_star_points()
        self.frame = 0

    def calc_star_points(self):
        # 5-point star relative to center (x,y)
        r_outer = self.size / 2
        r_inner = r_outer * 0.5
        points = []
        for i in range(10):
            angle = math.pi / 5 * i - math.pi / 2
            r = r_outer if i % 2 == 0 else r_inner
            px = r * math.cos(angle)
            py = r * math.sin(angle)
            points.append((px, py))
        return points

    def draw(self):
        if self.id:
            self.canvas.delete(self.id)

        fill = self.color
        if self.shape_type == 'circle':
            r = self.size / 2
            self.id = self.canvas.create_oval(
                self.x - r, self.y - r, self.x + r, self.y + r,
                fill=fill, outline='', stipple='gray50'
            )
        elif self.shape_type == 'triangle':
            h = self.size * math.sqrt(3) / 2
            points = [
                self.x, self.y - 2/3*h,
                self.x - self.size/2, self.y + h/3,
                self.x + self.size/2, self.y + h/3
            ]
            self.id = self.canvas.create_polygon(points, fill=fill, outline='', stipple='gray25')
        elif self.shape_type == 'star':
            pts = []
            for px, py in self.star_points:
                pts.extend([self.x + px, self.y + py])
            self.id = self.canvas.create_polygon(pts, fill=fill, outline='', stipple='gray12')

    def move(self):
        # Slightly random jitter — unpredictable
        jitter_x = random.uniform(-0.4, 0.4)
        jitter_y = random.uniform(-0.4, 0.4)

        self.x += self.vx + jitter_x
        self.y += self.vy + jitter_y

        # Wrap around edges — like a thought drifting beyond focus
        if self.x < -self.size: self.x = WIDTH + self.size
        if self.x > WIDTH + self.size: self.x = -self.size
        if self.y < -self.size: self.y = HEIGHT + self.size
        if self.y > HEIGHT + self.size: self.y = -self.size

        # Subtle breathing size change — pulse of whimsy
        self.frame += 1
        self.size += 0.3 * math.sin(self.frame * 0.1)

        # Color flicker — slight chance to shift hue softly
        if random.random() < 0.02:
            self.color = rnd_color()

def burst(canvas, x, y):
    # A tiny whimsical spark of dots bursting out, ephemeral
    sparks = []
    for _ in range(10):
        dx = random.uniform(-5, 5)
        dy = random.uniform(-5, 5)
        r = random.uniform(2, 6)
        color = rnd_color()
        dot = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline='')
        sparks.append((dot, dx, dy, r, 10))
    return sparks

def update_sparks(canvas, sparks):
    # Move sparks outward, fade them quickly
    remove = []
    for i, (dot, dx, dy, r, life) in enumerate(sparks):
        life -= 1
        if life <= 0:
            canvas.delete(dot)
            remove.append(i)
            continue
        canvas.move(dot, dx, dy)
        alpha = int(255 * (life / 10))
        # Tkinter does not support alpha so we ignore fading visually,
        # but we remove after lifespan.
        sparks[i] = (dot, dx, dy, r, life)
    for i in reversed(remove):
        sparks.pop(i)

def main():
    root = tk.Tk()
    root.title("whimsy")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.configure(bg='#fefefc')
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='#fefefc', highlightthickness=0)
    canvas.pack()

    shapes = [Shape(canvas) for _ in range(SHAPE_COUNT)]
    sparks = []

    def tick():
        canvas.delete('all')

        # Randomly add a burst somewhere on canvas ~5% chance each tick
        if random.random() < 0.05:
            bx = random.uniform(0, WIDTH)
            by = random.uniform(0, HEIGHT)
            sparks.extend(burst(canvas, bx, by))

        update_sparks(canvas, sparks)

        for s in shapes:
            s.move()
            s.draw()

        # Draw a faint, curving "invisible" thread - a whisper of a smile
        for i in range(len(shapes) - 1):
            x1, y1 = shapes[i].x, shapes[i].y
            x2, y2 = shapes[i+1].x, shapes[i+1].y
            cx = (x1 + x2) / 2 + 20 * math.sin(time.time()*3 + i)
            cy = (y1 + y2) / 2 + 20 * math.cos(time.time()*2 + i)
            canvas.create_line(x1, y1, cx, cy, x2, y2,
                               smooth=True,
                               fill="#d3c1f9", width=1, dash=(3, 5))

        root.after(40, tick)

    tick()
    root.mainloop()

if __name__ == "__main__":
    main()
