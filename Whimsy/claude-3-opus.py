import tkinter as tk
import random
import math
import time

# W H i M s y ~*~
 
def let_it_whimsy():
    whimsy_window = tk.Tk()
    
    width = 800
    height = 600
    
    whimsy_window.title(".:*~=  W H i M S y  =~*:.")
    
    canvas = tk.Canvas(whimsy_window, width=width, height=height, bg="alice blue")
    canvas.pack()
    
    def whimsify(event):
        x, y = event.x, event.y
        
        hue = random.random()
        color = f"#{int(hue*0xFFFFFF):06x}"
        
        size = random.randint(10, 50)
        
        angle = random.uniform(0, 2*math.pi)
        dx = math.cos(angle) * size/2
        dy = math.sin(angle) * size/2
        
        canvas.create_arc(x-dx, y-dy, x+dx, y+dy, 
                          start=0, extent=359.9, 
                          fill=color, outline="")
        
        canvas.create_text(random.randint(0, width), random.randint(0, height),
                           text=random.choice(["*", "~", ".", "o", "+"]),
                           font=("Arial", random.randint(10,30)), 
                           fill=color)
        
    canvas.bind("<Motion>", whimsify)
    
    while True:
        whimsy_window.update()
        time.sleep(0.01)

let_it_whimsy()