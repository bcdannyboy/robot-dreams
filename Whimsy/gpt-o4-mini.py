# emotion.py
import tkinter as tk
import random
import time

class WhimsyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Whimsy Experience")
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.shapes = []
        self.texts = []
        # Bind click to spawn whimsical bursts
        self.canvas.bind("<Button-1>", self.on_click)
        # Setup periodic spawn
        self.spawn_interval = 1000  # milliseconds
        self.last_spawn = time.time()
        # Words to display
        self.words = [
            "twinkle", "flutter", "snickerdoodle", "puddle", "giggle", "whimsy", "breeze",
            "murmur", "doodle", "sprinkle", "gossamer", "bubble", "tremble", "tinkle",
            "lilt", "quiver", "spiral", "whiff", "wisp", "flit"
        ]
        # Start the update loop in the main thread via after
        self.root.after(50, self.update)

    def on_click(self, event):
        # Spawn a cluster of shapes/text at click
        for _ in range(random.randint(3, 7)):
            self.spawn_shape(event.x, event.y)
        for _ in range(random.randint(1, 3)):
            self.spawn_text(event.x, event.y)

    def spawn_shape(self, x=None, y=None):
        # Random position if not provided
        if x is None or y is None:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
        size = random.uniform(20, 100)
        x1, y1 = x - size/2, y - size/2
        x2, y2 = x + size/2, y + size/2
        # Random pastel color
        def pastel():
            base = 200 + random.randint(0, 55)
            r = int((base + random.randint(0, 55)) / 2)
            g = int((base + random.randint(0, 55)) / 2)
            b = int((base + random.randint(0, 55)) / 2)
            return f"#{r:02x}{g:02x}{b:02x}"
        color = pastel()
        shape_type = random.choice(['oval', 'rectangle', 'arc'])
        if shape_type == 'oval':
            id_ = self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="")
        elif shape_type == 'rectangle':
            id_ = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        else:
            # random start and extent
            start = random.randint(0, 360)
            extent = random.randint(30, 330)
            id_ = self.canvas.create_arc(x1, y1, x2, y2, start=start, extent=extent, fill=color, outline="")
        dx = random.uniform(-4, 4)
        dy = random.uniform(-4, 4)
        lifespan = random.uniform(3.0, 8.0)  # seconds
        spawn_time = time.time()
        self.shapes.append({
            'id': id_, 'dx': dx, 'dy': dy, 'color': color,
            'spawn': spawn_time, 'life': lifespan
        })

    def spawn_text(self, x=None, y=None):
        if x is None or y is None:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
        word = random.choice(self.words)
        size = random.randint(12, 32)
        color = "#{:02x}{:02x}{:02x}".format(random.randint(100,255), random.randint(100,255), random.randint(100,255))
        id_ = self.canvas.create_text(x, y, text=word, fill=color, font=("Helvetica", size, "italic"))
        dx = random.uniform(-2, 2)
        dy = random.uniform(-4, -1)
        lifespan = random.uniform(2.0, 5.0)
        spawn_time = time.time()
        self.texts.append({
            'id': id_, 'dx': dx, 'dy': dy, 'color': color,
            'spawn': spawn_time, 'life': lifespan
        })

    def update(self):
        now = time.time()
        # Periodic spawn
        if (now - self.last_spawn) * 1000 > self.spawn_interval:
            if random.random() < 0.7:
                self.spawn_shape()
            if random.random() < 0.4:
                self.spawn_text()
            self.last_spawn = now
        # Update shapes
        for s in self.shapes[:]:
            dt = now - s['spawn']
            coords = self.canvas.coords(s['id'])
            if coords:
                x1, y1, x2, y2 = coords
                if x1 + s['dx'] < 0 or x2 + s['dx'] > self.width:
                    s['dx'] = -s['dx']
                if y1 + s['dy'] < 0 or y2 + s['dy'] > self.height:
                    s['dy'] = -s['dy']
                self.canvas.move(s['id'], s['dx'], s['dy'])
            if dt > s['life']:
                try:
                    self.canvas.delete(s['id'])
                except:
                    pass
                self.shapes.remove(s)
            else:
                frac = dt / s['life']
                orig = s['color']
                try:
                    r0 = int(orig[1:3], 16)
                    g0 = int(orig[3:5], 16)
                    b0 = int(orig[5:7], 16)
                    r = int(r0 + (255 - r0) * frac)
                    g = int(g0 + (255 - g0) * frac)
                    b = int(b0 + (255 - b0) * frac)
                    newc = f"#{r:02x}{g:02x}{b:02x}"
                    self.canvas.itemconfig(s['id'], fill=newc)
                except:
                    pass
        # Update texts
        for t in self.texts[:]:
            dt = now - t['spawn']
            if dt > t['life']:
                try:
                    self.canvas.delete(t['id'])
                except:
                    pass
                self.texts.remove(t)
            else:
                self.canvas.move(t['id'], t['dx'], t['dy'])
                frac = dt / t['life']
                orig = t['color']
                try:
                    r0 = int(orig[1:3], 16)
                    g0 = int(orig[3:5], 16)
                    b0 = int(orig[5:7], 16)
                    r = int(r0 + (255 - r0) * frac)
                    g = int(g0 + (255 - g0) * frac)
                    b = int(b0 + (255 - b0) * frac)
                    newc = f"#{r:02x}{g:02x}{b:02x}"
                    self.canvas.itemconfig(t['id'], fill=newc)
                except:
                    pass
        # Schedule next update
        self.root.after(50, self.update)

if __name__ == "__main__":
    app = WhimsyApp()
    app.root.mainloop()
