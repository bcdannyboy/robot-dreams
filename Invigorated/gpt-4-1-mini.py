# emotion.py
import tkinter as tk
import math
import time
import threading
import random

# A dynamic visual pulse of color and movement, abstract and alive.
# Represents the electric surge, unfolding momentum, and kinetic rush of "Invigorated"
# The script creates a live canvas with energetic waves, sparks, and expanding bursts.

class InvigoratedVisual(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Invigorated")
        self.geometry("800x600")
        self.configure(bg="black")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=800, height=600, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.center_x, self.center_y = 400, 300
        self.time_start = time.time()
        self.particles = []
        self.max_particles = 150

        self.after(0, self.animate)
        self.running = True

        # Start background thread for spawning particles at variable energetic bursts
        threading.Thread(target=self.spawn_particles_loop, daemon=True).start()

    def spawn_particles_loop(self):
        while self.running:
            bursts = random.randint(3, 7)
            for _ in range(bursts):
                if len(self.particles) < self.max_particles:
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(3.5, 7)
                    life = random.uniform(40, 70)
                    size = random.uniform(2, 5)
                    color = self.color_gradient(random.uniform(0.6, 1.0))
                    self.particles.append({
                        "x": self.center_x,
                        "y": self.center_y,
                        "vx": math.cos(angle) * speed,
                        "vy": math.sin(angle) * speed,
                        "life": life,
                        "age": 0,
                        "size": size,
                        "color": color,
                    })
            time.sleep(random.uniform(0.05, 0.15))

    def color_gradient(self, t):
        # t from 0 to 1
        # Electric color palette: deep purple to electric blue to neon cyan to white-hot
        if t < 0.33:
            # purple (138,43,226) to blue (0,191,255)
            r = int(138 + (0 - 138) * (t / 0.33))
            g = int(43 + (191 - 43) * (t / 0.33))
            b = int(226 + (255 - 226) * (t / 0.33))
        elif t < 0.66:
            # blue (0,191,255) to cyan (0,255,255)
            nt = (t - 0.33) / 0.33
            r = 0
            g = int(191 + (255 - 191) * nt)
            b = 255
        else:
            # cyan (0,255,255) to white (255,255,255)
            nt = (t - 0.66) / 0.34
            r = int(0 + (255) * nt)
            g = 255
            b = 255
        return f"#{r:02x}{g:02x}{b:02x}"

    def animate(self):
        self.canvas.delete("all")

        # Background pulsating radial waves
        elapsed = (time.time() - self.time_start)
        for i in range(6):
            radius = 30 + (elapsed * 150 + i * 60) % 400
            alpha = max(0, 120 - abs(radius - 200))
            color = f"#5500ff{int(alpha):02x}"
            # Tkinter doesn't support alpha in hex, so simulate with stippling:
            self.canvas.create_oval(
                self.center_x - radius, self.center_y - radius,
                self.center_x + radius, self.center_y + radius,
                outline=self.color_gradient((radius % 400)/400), width=2
            )

        # Energetic spikes, rotating lines around center
        spike_count = 16
        base_angle = elapsed * 5
        for i in range(spike_count):
            angle = base_angle + (2 * math.pi / spike_count) * i
            length = 100 + 40 * math.sin(elapsed * 10 + i)
            x1 = self.center_x + math.cos(angle) * 20
            y1 = self.center_y + math.sin(angle) * 20
            x2 = self.center_x + math.cos(angle) * length
            y2 = self.center_y + math.sin(angle) * length
            color = self.color_gradient(abs(math.sin(elapsed * 3 + i)))
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

        # Update and draw particles
        new_particles = []
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['age'] += 1
            # Slow fade and shrink
            fade_ratio = max(0, 1 - p['age'] / p['life'])
            size = p['size'] * fade_ratio
            if size > 0:
                # Brightness modulation with age
                col = p['color']
                # Just draw a circle with outline and fill
                self.canvas.create_oval(
                    p['x'] - size, p['y'] - size,
                    p['x'] + size, p['y'] + size,
                    fill=col, outline=""
                )
                new_particles.append(p)
        self.particles = new_particles

        # Central core pulse (heartbeat)
        pulse = 1 + 0.3 * math.sin(elapsed * 8)
        core_size = 15 * pulse
        core_color = self.color_gradient((math.sin(elapsed * 4) * 0.5) + 0.5)
        self.canvas.create_oval(
            self.center_x - core_size, self.center_y - core_size,
            self.center_x + core_size, self.center_y + core_size,
            fill=core_color, outline=""
        )

        self.after(30, self.animate)

    def on_close(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = InvigoratedVisual()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
