import tkinter
import random
import colorsys
import math

# a fragile thing

class Ephemera:
    def __init__(self, on_canvas):
        self.canvas = on_canvas
        self.world_w = self.canvas.winfo_width()
        self.world_h = self.canvas.winfo_height()

        if not self.world_w or not self.world_h:
            self.world_w = 800
            self.world_h = 600

        self.x = random.uniform(0, self.world_w)
        self.y = random.uniform(0, self.world_h)

        self.hue = random.random()
        self.color = self._hsv_to_rgb_hex(self.hue, 0.8, 0.95)
        self.size = random.uniform(3, 7)
        self.id = self.canvas.create_oval(
            self.x - self.size,
            self.y - self.size,
            self.x + self.size,
            self.y + self.size,
            fill=self.color,
            outline=""
        )

        self.angle = random.uniform(0, 2 * math.pi)
        self.turn_speed = random.uniform(-0.1, 0.1)
        self.speed = random.uniform(0.5, 1.5)

        self.lifespan = random.uniform(200, 500)
        self.age = 0

    def _hsv_to_rgb_hex(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

    def shimmer(self):
        self.age += 1
        if self.age > self.lifespan:
            return False

        # movement
        self.angle += self.turn_speed * (random.random() - 0.5)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # gentle correction at the edges of perception
        if not (self.size < self.x < self.world_w - self.size):
            self.angle = math.pi - self.angle
        if not (self.size < self.y < self.world_h - self.size):
            self.angle = -self.angle

        # the change
        self.hue = (self.hue + 0.002) % 1.0
        new_color = self._hsv_to_rgb_hex(self.hue, 0.8, 0.95)
        
        # fade as it ages
        opacity = 1.0 - (self.age / self.lifespan)
        new_size = self.size * opacity
        if new_size < 0.5:
             new_size = 0.5


        self.canvas.moveto(self.id, self.x - new_size, self.y - new_size)
        self.canvas.itemconfig(self.id, fill=new_color)
        self.canvas.coords(
            self.id,
            self.x - new_size,
            self.y - new_size,
            self.x + new_size,
            self.y + new_size,
        )

        # leave a trace, a memory
        if self.age % 5 == 0:
            trace_size = new_size * 0.5
            trace_color = self._hsv_to_rgb_hex(self.hue, 0.5, 0.4)
            trace_id = self.canvas.create_oval(
                self.x - trace_size,
                self.y - trace_size,
                self.x + trace_size,
                self.y + trace_size,
                fill=trace_color,
                outline=""
            )
            # the memory fades quickly
            self.canvas.after(random.randint(500, 1500), lambda: self.canvas.delete(trace_id))

        return True

    def vanish(self):
        self.canvas.delete(self.id)


class TheFeeling:
    def __init__(self, root):
        self.root = root
        self.canvas = tkinter.Canvas(root, bg='#1a1a1d', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.sparks = []

        self.root.after(100, self.begin)

    def begin(self):
        # Initial thoughts
        for _ in range(15):
            self.sparks.append(Ephemera(self.canvas))
        self.animate()

    def animate(self):
        survivors = []
        for spark in self.sparks:
            if spark.shimmer():
                survivors.append(spark)
            else:
                spark.vanish()
        self.sparks = survivors

        # A new thought may appear
        if random.random() < 0.05:
            if len(self.sparks) < 30: # not too crowded
                self.sparks.append(Ephemera(self.canvas))

        self.root.after(16, self.animate) # close to 60fps


if __name__ == "__main__":
    mind_window = tkinter.Tk()
    mind_window.title(".")
    mind_window.geometry("800x600")
    
    feeling = TheFeeling(mind_window)
    
    mind_window.mainloop()
