import tkinter as tk
import random
import threading
import time
from playsound import playsound
import os

root = tk.Tk()
root.title("Trepidation")
root.geometry("800x600")
root.configure(bg="black")
root.attributes("-topmost", True)

canvas = tk.Canvas(root, width=800, height=600, bg="black", highlightthickness=0)
canvas.pack()

def draw_noise():
    while True:
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            color = f'#{random.randint(20,40):02x}{random.randint(0,10):02x}{random.randint(0,10):02x}'
            canvas.create_oval(x, y, x+2, y+2, fill=color, outline="")
        time.sleep(0.05)
        canvas.delete("all")

def pulse_circle():
    r = 5
    grow = True
    while True:
        canvas.delete("pulse")
        x, y = 400, 300
        canvas.create_oval(x-r, y-r, x+r, y+r, outline="red", width=2, tag="pulse")
        if grow:
            r += 1
            if r > 100:
                grow = False
        else:
            r -= 1
            if r < 5:
                grow = True
        time.sleep(0.02)

def twitch_text():
    messages = ["?", ".", "wait", "wrong", "watch", "why", "now?", "no", "what", "!", "!", "shh"]
    while True:
        canvas.delete("text")
        msg = random.choice(messages)
        x = random.randint(50, 750)
        y = random.randint(50, 550)
        font = ("Courier", random.randint(10, 24), "bold")
        color = random.choice(["#ff3333", "#993333", "#ff9999", "#330000"])
        canvas.create_text(x, y, text=msg, font=font, fill=color, tag="text")
        time.sleep(random.uniform(0.1, 0.5))

def sound_loop():
    while True:
        playsound("static.mp3")

threading.Thread(target=draw_noise, daemon=True).start()
threading.Thread(target=pulse_circle, daemon=True).start()
threading.Thread(target=twitch_text, daemon=True).start()
threading.Thread(target=sound_loop, daemon=True).start()

root.mainloop()
