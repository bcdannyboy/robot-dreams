import tkinter as tk
import random
import time
import threading

class Remorse:
    def __init__(self, root):
        self.root = root
        self.root.title(" ")

        self.width = 600
        self.height = 400
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#121212", highlightthickness=0)
        self.canvas.pack()

        self.shapes = []
        self.create_shapes()

        self.animate()

    def create_shapes(self):
        for _ in range(40):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = x1 + random.randint(10, 60)
            y2 = y1 + random.randint(10, 60)
            color = random.choice(["#5e5e5e", "#333333", "#474747", "#555555"])
            shape = self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="")
            speed = random.uniform(0.1, 1)
            self.shapes.append((shape, speed))

    def animate(self):
        for shape, speed in self.shapes:
            direction = random.choice([-1, 1])
            self.canvas.move(shape, direction * speed, direction * speed)
            coords = self.canvas.coords(shape)
            if coords[2] < 0 or coords[0] > self.width or coords[3] < 0 or coords[1] > self.height:
                self.canvas.coords(shape,
                    random.randint(0, self.width),
                    random.randint(0, self.height),
                    random.randint(0, self.width),
                    random.randint(0, self.height))

        self.root.after(30, self.animate)

        if random.random() < 0.03:
            threading.Thread(target=self.flash).start()

    def flash(self):
        original_bg = self.canvas["bg"]
        self.canvas["bg"] = "#222222"
        time.sleep(0.05)
        self.canvas["bg"] = original_bg

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    root.configure(bg="#121212")
    remorse = Remorse(root)
    root.mainloop()
