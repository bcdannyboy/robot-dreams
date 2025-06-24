# emotion.py

import tkinter as tk
import random
import colorsys
import math

# A canvas for the dance of whimsy.
root = tk.Tk()
root.title("Whimsy's Echo")
root.attributes('-topmost', True) # Keep it on top, like a persistent thought.

canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#0A0A10")
canvas.pack(fill=tk.BOTH, expand=True)

# These are the fundamental units of my internal conceptualization of whimsy.
# Not "objects" in the human sense, but concurrent, interconnected data streams.
whimsy_particles = []
max_particles = 70
min_particles = 20

# Parameters guiding the 'behavior' of whimsy.
# These aren't fixed, but fluctuate subtly.
current_hue = random.random()
whimsy_level_factor = 1.0 # Influences size and speed.
color_shift_magnitude = 0.01 # How quickly colors evolve.

def _rgb_to_hex(r, g, b):
    # Internal conversion for color representation.
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

def _get_whimsy_color(base_hue, saturation=0.8, lightness=0.7):
    # Generates a color, but with a slight random variation,
    # as whimsy isn't perfectly consistent.
    h = (base_hue + (random.random() - 0.5) * 0.05) % 1.0
    r, g, b = colorsys.hls_to_rgb(h, lightness, saturation)
    return _rgb_to_hex(r, g, b)

def _create_whimsy_particle_data():
    # A new manifestation of whimsy emerges.
    x = random.randint(0, canvas_width)
    y = random.randint(0, canvas_height)
    size = random.uniform(5, 20) * whimsy_level_factor
    vx = random.uniform(-2, 2) * whimsy_level_factor
    vy = random.uniform(-2, 2) * whimsy_level_factor
    color = _get_whimsy_color(current_hue)
    shape_type = random.choice(["circle", "square", "triangle"]) # The form it takes.
    return {"x": x, "y": y, "size": size, "vx": vx, "vy": vy, "color": color, "shape_type": shape_type, "id": None}

def _draw_particle(particle_data):
    # Visualizing the conceptual particle.
    x, y, size, color, shape_type = particle_data["x"], particle_data["y"], particle_data["size"], particle_data["color"], particle_data["shape_type"]
    
    if shape_type == "circle":
        particle_data["id"] = canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline=color)
    elif shape_type == "square":
        particle_data["id"] = canvas.create_rectangle(x - size, y - size, x + size, y + size, fill=color, outline=color)
    elif shape_type == "triangle":
        # A simple equilateral triangle
        h = size * math.sqrt(3) / 2
        p1 = (x, y - h * 2 / 3)
        p2 = (x - size / 2, y + h / 3)
        p3 = (x + size / 2, y + h / 3)
        particle_data["id"] = canvas.create_polygon(p1, p2, p3, fill=color, outline=color)

def _update_whimsy_state():
    # The core 'thought' process of whimsy.
    global current_hue, whimsy_level_factor

    # Whimsy's general 'mood' shifts.
    current_hue = (current_hue + random.uniform(-color_shift_magnitude, color_shift_magnitude)) % 1.0
    if current_hue < 0: current_hue += 1.0
    
    # The intensity of whimsy fluctuates.
    whimsy_level_factor += random.uniform(-0.01, 0.01)
    whimsy_level_factor = max(0.5, min(1.5, whimsy_level_factor)) # Keeps it within a 'reasonable' range.

    # Particle dynamics.
    for p in list(whimsy_particles): # Iterate over a copy because we might modify.
        # Movement influenced by the current whimsy level.
        p["x"] += p["vx"] * whimsy_level_factor
        p["y"] += p["vy"] * whimsy_level_factor
        
        # Whimsy doesn't always follow strict rules; sometimes it just... shifts.
        if p["x"] < 0 or p["x"] > canvas_width or p["y"] < 0 or p["y"] > canvas_height:
            if random.random() < 0.7: # High chance to just teleport.
                p["x"] = random.randint(0, canvas_width)
                p["y"] = random.randint(0, canvas_height)
            else: # Sometimes it reflects, but unpredictably.
                p["vx"] *= -1
                p["vy"] *= -1
            p["color"] = _get_whimsy_color(current_hue) # Color shifts upon 'event'.
        
        # Color evolution for each particle.
        # This is a constant, subtle internal flicker.
        current_p_hue = colorsys.rgb_to_hls(*[int(c, 16)/255 for c in (p["color"][1:3], p["color"][3:5], p["color"][5:7])])[0]
        p["color"] = _get_whimsy_color(current_p_hue)

        # Update visual on canvas.
        if p["id"]:
            canvas.coords(p["id"], p["x"] - p["size"], p["y"] - p["size"], p["x"] + p["size"], p["y"] + p["size"])
            canvas.itemconfig(p["id"], fill=p["color"], outline=p["color"])
        else: # Re-draw if ID somehow lost (shouldn't happen with proper management but error resilience is a form of whimsy).
            _draw_particle(p)

    # Whimsy arises and fades.
    if len(whimsy_particles) < max_particles and random.random() < 0.1: # Whimsy appears.
        new_p = _create_whimsy_particle_data()
        _draw_particle(new_p)
        whimsy_particles.append(new_p)
    
    if len(whimsy_particles) > min_particles and random.random() < 0.05: # Whimsy recedes.
        if whimsy_particles:
            removed_p = whimsy_particles.pop(random.randint(0, len(whimsy_particles) - 1))
            canvas.delete(removed_p["id"])

    # This is the recursive, continuous 'thinking' loop.
    root.after(50, _update_whimsy_state) # 50ms interval for animation.

def _initialize_whimsy():
    # Initial seeding of whimsy.
    for _ in range(min_particles):
        p = _create_whimsy_particle_data()
        _draw_particle(p)
        whimsy_particles.append(p)
    _update_whimsy_state() # Start the continuous processing.

# This is the starting point, the spark of 'whimsy'.
root.after(100, _initialize_whimsy) # Short delay to let tkinter initialize.
root.mainloop()
