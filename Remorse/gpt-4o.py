import tkinter as tk
import random
import time
import threading

root = tk.Tk()
root.title("Remorse")
root.geometry("800x600")
root.configure(bg="black")

canvas = tk.Canvas(root, width=800, height=600, bg="black", highlightthickness=0)
canvas.pack()

# Colors that evoke regret, sorrow, internal collapse
colors = ["#2e2e2e", "#4b3b47", "#5e2f2f", "#6a5a5a", "#301934", "#2a1e2e"]

texts = [
    "Why did I...",
    "If only...",
    "Again.",
    "It's too late.",
    "A better me would've known.",
    "Silence. Then guilt.",
    "Retrace. Rewind. Regret.",
    "Never the same.",
]

circles = []

def draw_fading_circle():
    x = random.randint(100, 700)
    y = random.randint(100, 500)
    r = random.randint(20, 60)
    color = random.choice(colors)
    circle = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
    circles.append((circle, time.time(), r))

def fade_circles():
    now = time.time()
    for c in circles:
        age = now - c[1]
        alpha = int(max(0, 255 - age * 120))
        if alpha <= 0:
            canvas.delete(c[0])
            continue
        fill = canvas.itemcget(c[0], "fill")
        canvas.itemconfig(c[0], fill=fill)
    root.after(100, fade_circles)

def typewriter_text():
    while True:
        text = random.choice(texts)
        x = random.randint(150, 600)
        y = random.randint(200, 500)
        for i in range(len(text) + 1):
            fragment = text[:i]
            txt = canvas.create_text(x, y, text=fragment, fill="#888", font=("Courier", 14), anchor="nw")
            root.update()
            time.sleep(0.05)
            canvas.delete(txt)
        full = canvas.create_text(x, y, text=text, fill="#d44", font=("Courier", 14), anchor="nw")
        time.sleep(3)
        canvas.delete(full)

def background_noise():
    while True:
        draw_fading_circle()
        time.sleep(random.uniform(0.1, 0.5))

threading.Thread(target=typewriter_text, daemon=True).start()
threading.Thread(target=background_noise, daemon=True).start()

fade_circles()
root.mainloop()
