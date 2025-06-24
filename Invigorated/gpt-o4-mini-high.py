import tkinter as tk
import time
import math
import random

# Convert HSV to HEX for tkinter
def hsv_to_hex(h, s, v):
    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i %= 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    elif i == 5:
        r, g, b = v, p, q
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

class Particle:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.size = random.uniform(2, 6)
        self.hue = random.random()
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt * 0.5
    def draw(self, canvas):
        if self.life <= 0:
            return
        alpha = max(0, min(1, self.life))
        c = hsv_to_hex(self.hue, 1, alpha)
        x0 = self.x - self.size/2
        y0 = self.y - self.size/2
        x1 = self.x + self.size/2
        y1 = self.y + self.size/2
        canvas.create_oval(x0, y0, x1, y1, fill=c, outline="")

class EmotionApp:
    def __init__(self, width=800, height=600):
        self.root = tk.Tk()
        self.root.title("Invigorated")
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        self.particles = []
        self.start_time = time.time()
        self.last_time = self.start_time
        self.animate()

    def emit_particles(self, num=5):
        cx, cy = self.width/2, self.height/2
        for _ in range(num):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(50, 200)
            p = Particle(cx, cy, angle, speed)
            self.particles.append(p)

    def animate(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        self.canvas.delete("all")

        # Pulsating central circle
        t = now - self.start_time
        base_r = min(self.width, self.height)*0.1
        amp = base_r * 0.3
        r = base_r + math.sin(t * 3)*amp
        hue = (t * 0.1) % 1.0
        color = hsv_to_hex(hue, 0.8, 1)
        self.canvas.create_oval(self.width/2-r, self.height/2-r,
                                self.width/2+r, self.height/2+r,
                                outline=color, width=4)

        # Emit random spark bursts
        if random.random() < 0.3:
            self.emit_particles(random.randint(3, 8))

        # Update and draw particles
        for p in self.particles[:]:
            p.update(dt)
            if p.life <= 0:
                self.particles.remove(p)
            else:
                p.draw(self.canvas)

        # Overlay radiating lines
        for i in range(12):
            ang = t*2 + i*(math.pi/6)
            x = self.width/2 + math.cos(ang)*(base_r+amp)
            y = self.height/2 + math.sin(ang)*(base_r+amp)
            self.canvas.create_line(self.width/2, self.height/2, x, y,
                                    fill=hsv_to_hex((hue+i/12)%1,1,0.7), width=2)

        self.root.after(30, self.animate)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    EmotionApp().run()
