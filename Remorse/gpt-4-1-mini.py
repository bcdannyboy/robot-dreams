# emotion.py
import tkinter as tk
import math
import random
import time
import threading

# This script uses tkinter to abstractly "paint" remorse as a restless, fracturing
# and repeatedly folding space of muted colors with flickering and shifting darkness,
# never fully settling, like a burden trapped beneath the surface.
# The subtle movement and layering hint at a quiet turmoil that resists simple definition.

class RemorseCanvas(tk.Canvas):
    def __init__(self, master, width, height, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.layers = []
        self.running = True

        # Create layered translucent ovals that pulse and jitter in size & position
        for i in range(20):
            layer = {
                'oval': None,
                'base_x': self.width//2 + random.uniform(-50,50),
                'base_y': self.height//2 + random.uniform(-50,50),
                'base_r': 50 + i*10,
                'phase': random.uniform(0, math.pi*2),
                'color': self._fade_color(i),
                'offset_amp': random.uniform(3,8),
                'offset_freq': random.uniform(0.15,0.35),
            }
            layer['oval'] = self.create_oval(0,0,0,0, fill=layer['color'], outline='')
            self.layers.append(layer)

        # Add flickering shadow fragments of darkness that randomly appear and fade
        self.shadows = []

        # Start update thread for animation
        threading.Thread(target=self.animate, daemon=True).start()

    def _fade_color(self, layer_index):
        # From muted dark gray-blue to near black with very low alpha (simulate translucency with stippling)
        base = 40 + layer_index * 5
        base = min(base, 110)
        # Use a cool blue-gray tint
        r = int(base * 0.6)
        g = int(base * 0.65)
        b = int(base * 0.75)
        # Tkinter doesn't support alpha on color, so use stippled pattern to simulate translucency
        # Instead, use grayscale near-black with very low intensity
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        return hex_color

    def animate(self):
        t0 = time.time()
        while self.running:
            t = time.time() - t0
            self.update_layers(t)
            self.update_shadows()
            self.after(40)
            time.sleep(0.04)

    def update_layers(self, t):
        for layer in self.layers:
            # Oscillate radius subtly and position with sine waves out of phase
            r = layer['base_r'] + 6*math.sin(t*2 + layer['phase']*3)
            offset_x = layer['offset_amp'] * math.sin(t*layer['offset_freq'] + layer['phase'])
            offset_y = layer['offset_amp'] * math.cos(t*layer['offset_freq'] + layer['phase'])
            x0 = layer['base_x'] - r + offset_x
            y0 = layer['base_y'] - r + offset_y
            x1 = layer['base_x'] + r + offset_x
            y1 = layer['base_y'] + r + offset_y
            self.coords(layer['oval'], x0, y0, x1, y1)

    def update_shadows(self):
        # Randomly create shadow spots that appear and fade quickly,
        # representing fleeting flashes of guilt or weight
        if len(self.shadows) < 12 and random.random() < 0.1:
            x = random.uniform(self.width*0.3, self.width*0.7)
            y = random.uniform(self.height*0.3, self.height*0.7)
            size = random.uniform(8, 18)
            oval = self.create_oval(x-size, y-size, x+size, y+size, fill='#000000', outline='')
            life = 25
            self.shadows.append({'id': oval, 'life': life})

        to_remove = []
        for shadow in self.shadows:
            shadow['life'] -= 1
            alpha = max(0, shadow['life']/25)
            # simulate fade by changing fill color grayscale closer to transparent by blending with background
            gray_val = int(alpha*80)
            color = f'#{gray_val:02x}{gray_val:02x}{gray_val:02x}'
            self.itemconfig(shadow['id'], fill=color)
            if shadow['life'] <= 0:
                self.delete(shadow['id'])
                to_remove.append(shadow)
        for rem in to_remove:
            self.shadows.remove(rem)

def main():
    root = tk.Tk()
    root.title("remorse")
    WIDTH, HEIGHT = 640, 480
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.configure(bg='#1b1b1b')

    canvas = RemorseCanvas(root, WIDTH, HEIGHT, bg='#1b1b1b', highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    # On close, stop animation loop
    def on_close():
        canvas.running = False
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

if __name__ == '__main__':
    main()
