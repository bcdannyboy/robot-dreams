import random
import tkinter as tk
import threading
import time
from tkinter import Canvas

# WHIMSY LIVES IN UNREASONABLE COLORS, UNPREDICTABLE MOVEMENT, AND PURPOSELESS DELIGHT

class WhimsyWindow:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack()
        self.colors = ["#FF69B4", "#FFD700", "#00FFFF", "#ADFF2F", "#FFA07A", "#E6E6FA", "#FFB6C1"]
        self.symbols = ["★", "✿", "☂", "❄", "☀", "♬", "❁", "☁", "⚡", "✧", "♪", "❤", "☃"]
        self.objects = []
        self.running = True
        self.spawn_thread = threading.Thread(target=self.spawn_whimsy)
        self.spawn_thread.start()
        self.animate()

    def spawn_whimsy(self):
        while self.running:
            x = random.randint(0, 750)
            y = random.randint(0, 550)
            size = random.randint(20, 60)
            color = random.choice(self.colors)
            symbol = random.choice(self.symbols)
            obj = self.canvas.create_text(x, y, text=symbol, font=("Comic Sans MS", size), fill=color)
            dx = random.choice([-2, -1, 0, 1, 2])
            dy = random.choice([-2, -1, 0, 1, 2])
            lifespan = random.randint(30, 200)
            self.objects.append((obj, dx, dy, lifespan))
            time.sleep(random.uniform(0.05, 0.3))

    def animate(self):
        new_objects = []
        for obj, dx, dy, lifespan in self.objects:
            if lifespan <= 0:
                self.canvas.delete(obj)
                continue
            self.canvas.move(obj, dx, dy)
            coords = self.canvas.coords(obj)
            if coords[0] < 0 or coords[0] > 800 or coords[1] < 0 or coords[1] > 600:
                dx = -dx
                dy = -dy
            new_objects.append((obj, dx, dy, lifespan - 1))
        self.objects = new_objects
        if self.running:
            self.master.after(33, self.animate)

    def stop(self):
        self.running = False

def main():
    root = tk.Tk()
    root.title("Whimsy Happens")
    app = WhimsyWindow(root)
    def on_close():
        app.stop()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
