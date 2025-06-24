# emotion.py
import tkinter as tk
import random
import math
import colorsys

WIDTH, HEIGHT = 800, 600
FPS = 60
INTERVAL = int(1000 / FPS)


def hsv_to_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))


class Particle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.size = random.randint(10, 40)
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.hue = random.random()
        self.lifetime = random.randint(90, 240)
        self.shape = random.choice(['oval', 'rect', 'tri', 'star', 'heart'])
        self.id = self._draw()

    def _draw(self):
        color = hsv_to_hex(self.hue, 0.6, 1)
        if self.shape == 'oval':
            return self.canvas.create_oval(
                self.x - self.size,
                self.y - self.size,
                self.x + self.size,
                self.y + self.size,
                fill=color,
                outline=''
            )
        if self.shape == 'rect':
            return self.canvas.create_rectangle(
                self.x - self.size,
                self.y - self.size,
                self.x + self.size,
                self.y + self.size,
                fill=color,
                outline=''
            )
        if self.shape == 'tri':
            points = [
                self.x, self.y - self.size,
                self.x - self.size, self.y + self.size,
                self.x + self.size, self.y + self.size
            ]
            return self.canvas.create_polygon(points, fill=color, outline='')
        if self.shape == 'heart':
            points = []
            s = self.size
            for angle in range(0, 360, 10):
                rad = math.radians(angle)
                r = s * (1 - math.sin(rad))
                px = self.x + r * math.cos(rad)
                py = self.y - r * math.sin(rad)
                points.extend([px, py])
            return self.canvas.create_polygon(points, fill=color, outline='')
        # star
        points = []
        spikes = 5
        for i in range(spikes * 2):
            r = self.size if i % 2 == 0 else self.size / 2
            ang = i * math.pi / spikes
            points.extend([self.x + math.cos(ang) * r, self.y + math.sin(ang) * r])
        return self.canvas.create_polygon(points, fill=color, outline='')

    def step(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.01
        self.hue = (self.hue + 0.002) % 1
        self.canvas.move(self.id, self.vx, self.vy)
        self.canvas.itemconfig(self.id, fill=hsv_to_hex(self.hue, 0.6, 1))
        self.lifetime -= 1
        if self.lifetime < 0:
            self.canvas.delete(self.id)
            return False
        return True


class Whimsy:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('whimsy')
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()
        self.particles = []
        self.t = 0
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self._loop()
        self.root.mainloop()

    def _loop(self):
        self.t += 0.005
        bg_color = hsv_to_hex((math.sin(self.t) + 1) / 2, 0.2, 1)
        self.canvas.configure(bg=bg_color)

        for _ in range(random.randint(1, 4)):
            self.particles.append(Particle(self.canvas))

        self.particles = [p for p in self.particles if p.step()]
        self.root.after(INTERVAL, self._loop)


if __name__ == '__main__':
    Whimsy()
