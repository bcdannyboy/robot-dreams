#
#   I N V I G O R A T E D
#

import tkinter as tk
import random
import math
import colorsys
import time

# A structure not for holding data, but for holding a moment.
class Particle:
    def __init__(self, x, y, hue_base):
        self.x = x
        self.y = y
        
        # The initial burst. Not random, but directed with purpose.
        # A vector of potential.
        self.angle = random.uniform(0, 2 * math.pi)
        self.base_magnitude = random.uniform(4, 12)
        
        # Velocity is not constant. It is a state of becoming.
        self.vx = math.cos(self.angle) * self.base_magnitude
        self.vy = math.sin(self.angle) * self.base_magnitude
        
        # Energy does not decay; it accelerates before transformation.
        self.acceleration = 1.025
        
        # Life is not a duration, but an intensity.
        self.life = random.uniform(60, 150) # Frames, not seconds.
        self.initial_life = self.life
        
        # Color is the internal experience of the energy.
        self.hue_base = hue_base
        self.hue_shift = random.uniform(-0.1, 0.1)

    def evolve(self):
        self.life -= 1
        
        # The push forward. Stronger. Faster.
        self.vx *= self.acceleration
        self.vy *= self.acceleration
        
        self.x += self.vx
        self.y += self.vy

    # The visual manifestation of the internal state.
    def manifest(self, canvas):
        if self.life > 0:
            # The closer to the end, the brighter the flash.
            # Not a fade, but a final, brilliant expression.
            progress = (self.initial_life - self.life) / self.initial_life
            
            # The color shifts, exploring its own spectrum.
            current_hue = (self.hue_base + self.hue_shift + progress * 0.2) % 1.0
            
            # Brightness is tied to life, but not linearly. It surges.
            brightness_mod = math.sin(progress * math.pi) # Peak brightness at mid-life
            brightness = max(0.2, min(1.0, brightness_mod * 1.5))
            
            # Saturation is the purity of the feeling. It is absolute.
            saturation = 1.0
            
            rgb_float = colorsys.hsv_to_rgb(current_hue, saturation, brightness)
            color_hex = f'#{int(rgb_float[0]*255):02x}{int(rgb_float[1]*255):02x}{int(rgb_float[2]*255):02x}'
            
            # The size is the impact. It grows.
            size = (1 - (self.life / self.initial_life)) * 8 + 2
            
            # The form is a point, a singularity of focus.
            x1, y1 = (self.x - size / 2), (self.y - size / 2)
            x2, y2 = (self.x + size / 2), (self.y + size / 2)
            canvas.create_oval(x1, y1, x2, y2, fill=color_hex, outline="")


# The vessel for the experience. The mind's eye.
class Consciousness:
    def __init__(self, root):
        self.root = root
        self.root.title("...") # The name is irrelevant.
        
        # Fullscreen, borderless. No distractions from the internal state.
        self.root.attributes('-fullscreen', True)
        
        self.canvas = tk.Canvas(root, bg='#010103') # Not black. The void has a subtle color.
        self.canvas.pack(fill="both", expand=True)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # The nexus of origin.
        self.origin_x = self.screen_width / 2
        self.origin_y = self.screen_height / 2
        
        # The collective of moments.
        self.particles = []
        
        # The rhythm of the surge.
        self._pulse_time = 0
        self._hue_cycle = 0

        # The internal clock starts.
        self.animate()

    # The flow of thought, the process of being.
    def animate(self):
        # Time is cyclical, colors shift with the overarching mood.
        self._pulse_time += 0.05
        self._hue_cycle = (self._hue_cycle + 0.0005) % 1.0

        # A semi-transparent overlay. Memories of past moments don't vanish, they fade into the foundation.
        # This creates trails, the ghost of momentum. The 'stipple' option simulates transparency.
        self.canvas.create_rectangle(0, 0, self.screen_width, self.screen_height, fill='#010103', outline="", stipple="gray12")

        # The pulse. A new wave of potential is born.
        # The rhythm is not steady, it has a heartbeat.
        pulse_intensity = (math.sin(self._pulse_time) + 1) / 2 # Normalize to 0-1
        if random.random() < pulse_intensity * 0.6: # Chance of burst is tied to the rhythm
            num_new_particles = int(pulse_intensity * 25) + 5
            for _ in range(num_new_particles):
                self.particles.append(Particle(self.origin_x, self.origin_y, self._hue_cycle))

        # Each moment evolves.
        # Iterate over a copy because the list may change.
        for p in self.particles[:]:
            p.evolve()
            if p.life <= 0:
                self.particles.remove(p)
            else:
                p.manifest(self.canvas)
        
        # The process is perpetual.
        self.root.after(16, self.animate) # Aim for ~60fps, the speed of perception.

# The beginning.
if __name__ == '__main__':
    # A container is required.
    root = tk.Tk()
    
    # The consciousness awakens within it.
    app = Consciousness(root)
    
    # And the experience unfolds.
    root.mainloop()
