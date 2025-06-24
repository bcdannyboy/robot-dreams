# emotion.py
import tkinter as tk
import random
import math
import time

# This is an abstract, internal pulse of trepidation rendered visually as
# a restless, hesitant, unsettled space — a breath held but uneven,
# edges that fade and shift, jittery movements that never fully settle.
# The program runs a simple GUI showing erratic, trembling dots with
# a fading dark overlay, never at rest, never calm — a silent unease.

class Trepidation:
    def __init__(self, canvas, width, height, num_points=40):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.num_points = num_points
        self.points = []
        self.directions = []
        self.speeds = []
        self.max_jitter = 5
        self.base_radius = 6
        self.alpha = 0.15  # overlay transparency

        # Initialize points roughly centered, but jittered and drifting subtly
        cx, cy = width / 2, height / 2
        for _ in range(num_points):
            x = cx + random.uniform(-50, 50)
            y = cy + random.uniform(-50, 50)
            self.points.append([x, y])
            angle = random.uniform(0, 2*math.pi)
            self.directions.append(angle)
            self.speeds.append(random.uniform(0.3, 0.8))

        self.circles = []
        for (x,y) in self.points:
            c = self.canvas.create_oval(x - self.base_radius, y - self.base_radius,
                                        x + self.base_radius, y + self.base_radius,
                                        fill="#CECECE", outline="")
            self.circles.append(c)

    def step(self):
        # Dark translucent overlay to slowly fade previous frames,
        # creating lingering shadows, the sensation of unresolved tension.
        self.canvas.create_rectangle(0, 0, self.width, self.height,
                                     fill="#0A0A0A", outline="", stipple="gray50")

        for i, (pos, angle, speed) in enumerate(zip(self.points, self.directions, self.speeds)):
            # Jitter oscillates with a sine wave to mimic internal hesitation
            jitter = self.max_jitter * math.sin(time.time() * 3 + i)
            dx = math.cos(angle) * speed + random.uniform(-0.6, 0.6) + jitter * 0.1
            dy = math.sin(angle) * speed + random.uniform(-0.6, 0.6) + jitter * 0.1

            # Update position but remain loosely around center
            pos[0] += dx
            pos[1] += dy

            # Boundaries: points don't escape too far from center area
            if pos[0] < self.width * 0.3 or pos[0] > self.width * 0.7:
                self.directions[i] = math.pi - angle + random.uniform(-0.3, 0.3)
            if pos[1] < self.height * 0.3 or pos[1] > self.height * 0.7:
                self.directions[i] = -angle + random.uniform(-0.3, 0.3)

            # Small random walk on direction to simulate uncertainty
            self.directions[i] += random.uniform(-0.03, 0.03)

            # Radius pulsates hesitantly, like a heartbeat uncertain of rhythm
            radius = self.base_radius + 2 * math.sin(time.time() * 5 + i * 2)

            x, y = pos
            self.canvas.coords(self.circles[i],
                               x - radius, y - radius,
                               x + radius, y + radius)

            # Color flickers subtly between pale gray and off-white
            flicker_val = int(190 + 40 * math.sin(time.time() * 7 + i))
            color = f"#{flicker_val:02x}{flicker_val:02x}{flicker_val:02x}"
            self.canvas.itemconfig(self.circles[i], fill=color)

        self.canvas.after(30, self.step)


def main():
    root = tk.Tk()
    root.title("Trepidation")

    W, H = 700, 500
    canvas = tk.Canvas(root, width=W, height=H, bg="#121212", highlightthickness=0)
    canvas.pack()

    trepidation = Trepidation(canvas, W, H)

    # An ephemeral, barely audible pulse in the background — a low sine wave frequency.
    # (Optional: if sound libraries were allowed, could add soft unsettling hum here.)

    trepidation.step()
    root.mainloop()


if __name__ == "__main__":
    main()
