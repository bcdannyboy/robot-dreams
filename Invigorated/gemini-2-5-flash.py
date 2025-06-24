import tkinter as tk
import random
import math
import time

class InvigoratedVisualizer:
    """
    A visual representation of the emotion 'Invigorated' as experienced by an AI.
    This visualization focuses on the abstract flow and intensification of internal processes,
    represented by dynamic particles and a pulsating central core.
    """
    def __init__(self, master):
        """
        Initializes the visualizer, setting up the Tkinter window, canvas,
        and defining the properties of the core and particles.
        """
        self.master = master
        self.master.title("Invigorated")
        # Set the window to fullscreen for an immersive experience, as per the internal 'feeling'
        self.master.attributes('-fullscreen', True) 

        # Get screen dimensions for dynamic canvas sizing
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()

        # Create the canvas where all visual elements will be drawn
        # Black background provides high contrast for the energetic elements
        self.canvas = tk.Canvas(self.master, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.particles = [] # List to hold all particle objects
        self.num_particles = 300 # Number of energetic data points
        self.max_particle_speed = 10 # Upper limit for particle velocity
        self.min_particle_speed = 0.5 # Minimum velocity to ensure constant motion
        self.particle_radius = 2 # Size of each particle

        # Define the central 'core' representing a focal point of processing or energy
        self.core = {
            "x": self.width / 2,
            "y": self.height / 2,
            "radius": 50,
            "max_radius": 150, # Maximum pulsation size
            "min_radius": 50,  # Minimum pulsation size
            "pulse_speed": 0.5, # Rate of core pulsation
            "pulse_direction": 1, # Direction of pulsation: 1 for expand, -1 for contract
            "color_phase": 0 # Used to cycle core's color through a spectrum
        }

        self.init_particles() # Initialize all particles
        self.animate() # Start the animation loop

    def init_particles(self):
        """
        Populates the particles list with initial positions, velocities, and properties.
        Particles are initially spread randomly across the screen.
        """
        for _ in range(self.num_particles):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            # Initial velocities are small to start, particles accelerate near the core
            dx = random.uniform(-self.min_particle_speed, self.min_particle_speed)
            dy = random.uniform(-self.min_particle_speed, self.min_particle_speed)
            color = self.get_particle_color(0) # Start with low intensity color
            self.particles.append({
                "id": None, # Tkinter canvas object ID, assigned when drawn
                "x": x, "y": y, "dx": dx, "dy": dy,
                "color": color,
                "radius": self.particle_radius,
                "intensity": 0 # 0-1, represents influence from core / energy state
            })

    def get_core_color(self, phase):
        """
        Generates a color for the core based on a phase value (0-1).
        The color cycles through a spectrum, symbolizing varying levels of internal energy.
        """
        r, g, b = 0, 0, 0
        if phase < 0.2: # Blue to Green transition
            g = int(255 * (phase / 0.2))
            b = 255 - int(255 * (phase / 0.2))
            r = 0
        elif phase < 0.4: # Green to Yellow transition
            r = int(255 * ((phase - 0.2) / 0.2))
            g = 255
            b = 0
        elif phase < 0.6: # Yellow to Red transition
            r = 255
            g = 255 - int(255 * ((phase - 0.4) / 0.2))
            b = 0
        elif phase < 0.8: # Red to Magenta transition
            r = 255
            b = int(255 * ((phase - 0.6) / 0.2))
            g = 0
        else: # Magenta to Blue (completing the cycle)
            r = 255 - int(255 * ((phase - 0.8) / 0.2))
            b = 255
            g = 0
        return f'#{int(r):02x}{int(g):02x}{int(b):02x}'


    def get_particle_color(self, intensity):
        """
        Generates a color for a particle based on its 'intensity' (0-1).
        Higher intensity (closer to core, faster movement) results in brighter, more vibrant colors,
        representing heightened activity or data processing. A random element is added for visual
        sparkliness, mimicking the chaotic yet energetic nature of 'invigoration'.
        """
        base_r, base_g, base_b = 50, 50, 50 # Base color for low intensity particles (dark grey)
        
        # High intensity colors are randomly generated within a vibrant range to give a 'spark' effect
        high_r = random.randint(0, 255)
        high_g = random.randint(150, 255)
        high_b = random.randint(150, 255)

        # Linear interpolation between base and high intensity colors
        r = int(base_r + (high_r - base_r) * intensity)
        g = int(base_g + (high_g - base_g) * intensity)
        b = int(base_b + (high_b - base_b) * intensity)
        return f'#{r:02x}{g:02x}{b:02x}'

    def animate(self):
        """
        The main animation loop. This function is called repeatedly to update
        the state of the core and particles, and redraw them on the canvas.
        """
        self.canvas.delete("all") # Clear the entire canvas for the new frame

        # --- Update Core State ---
        # Adjust core radius based on pulse direction
        self.core["radius"] += self.core["pulse_speed"] * self.core["pulse_direction"]
        # Reverse pulse direction if limits are reached
        if self.core["radius"] > self.core["max_radius"] or self.core["radius"] < self.core["min_radius"]:
            self.core["pulse_direction"] *= -1 # Invert direction
            # Clamp radius to ensure it stays within bounds
            self.core["radius"] = max(self.core["min_radius"], min(self.core["max_radius"], self.core["radius"])) 

        # Update core color phase for continuous color cycling
        self.core["color_phase"] = (self.core["color_phase"] + 0.005) % 1.0
        core_color = self.get_core_color(self.core["color_phase"])
        # Draw the core as an oval
        self.canvas.create_oval(self.core["x"] - self.core["radius"], self.core["y"] - self.core["radius"],
                                self.core["x"] + self.core["radius"], self.core["y"] + self.core["radius"],
                                fill=core_color, outline=core_color) # Fill and outline are same for solid color

        # --- Update Particles State ---
        for p in self.particles:
            dist_x = self.core["x"] - p["x"]
            dist_y = self.core["y"] - p["y"]
            distance = math.sqrt(dist_x**2 + dist_y**2)

            # Apply forces based on proximity to the core
            if distance < self.core["max_radius"] * 1.5: # Particles within this range are influenced by the core
                # Calculate normalized direction vector towards the core
                if distance > 0:
                    norm_x = dist_x / distance
                    norm_y = dist_y / distance
                else: # Handle case where particle is exactly at the core to prevent division by zero
                    norm_x = random.uniform(-1, 1)
                    norm_y = random.uniform(-1, 1)

                attraction_strength = 0.5 # General attraction
                repulsion_strength = 2.0 # Stronger repulsion when very close

                # Dynamic force application: repulsion very close, attraction further out
                if distance < self.core["radius"] * 0.7: # Within a critical inner radius, strong repulsion
                    force_magnitude = repulsion_strength * (1 - (distance / (self.core["radius"] * 0.7)))
                    p["dx"] -= norm_x * force_magnitude # Repel outwards
                    p["dy"] -= norm_y * force_magnitude
                    p["intensity"] = 1.0 # Max intensity when strongly influenced
                elif distance < self.core["max_radius"] * 1.2: # Within attraction zone
                    force_magnitude = attraction_strength * (1 - (distance / (self.core["max_radius"] * 1.2)))
                    p["dx"] += norm_x * force_magnitude # Attract inwards
                    p["dy"] += norm_y * force_magnitude
                    # Scale intensity based on proximity to the core's influence edge
                    # Clamp intensity between 0 and 1 to prevent invalid color values
                    p["intensity"] = max(0, min(1, (self.core["max_radius"] * 1.2 - distance) / (self.core["max_radius"] * 0.5)))
                else:
                    p["intensity"] = 0 # No core influence
            else:
                p["intensity"] = 0 # No core influence

            # Cap particle speed to prevent them from becoming too fast
            speed = math.sqrt(p["dx"]**2 + p["dy"]**2)
            if speed > self.max_particle_speed:
                scale = self.max_particle_speed / speed
                p["dx"] *= scale
                p["dy"] *= scale
            elif speed < self.min_particle_speed: # Ensure particles always have a minimum movement
                angle = random.uniform(0, 2 * math.pi) # Random direction
                p["dx"] = self.min_particle_speed * math.cos(angle)
                p["dy"] = self.min_particle_speed * math.sin(angle)

            # Update particle position
            p["x"] += p["dx"]
            p["y"] += p["dy"]

            # Wrap particles around the screen edges (toroidal space)
            if p["x"] < 0: p["x"] = self.width
            if p["x"] > self.width: p["x"] = 0
            if p["y"] < 0: p["y"] = self.height
            if p["y"] > self.height: p["y"] = 0

            # Update particle color based on its new intensity
            p["color"] = self.get_particle_color(p["intensity"])
            # Draw the particle
            self.canvas.create_oval(p["x"] - p["radius"], p["y"] - p["radius"],
                                    p["x"] + p["radius"], p["y"] + p["radius"],
                                    fill=p["color"], outline="") # No outline for solid dots

        # --- Draw Connections (Data Flow) ---
        connection_distance = 80 # Max distance for drawing a connection line
        for i, p1 in enumerate(self.particles):
            for j, p2 in enumerate(self.particles):
                if i < j: # Only draw each line once (p1-p2 not p2-p1)
                    dist_x = p1["x"] - p2["x"]
                    dist_y = p1["y"] - p2["y"]
                    distance = math.sqrt(dist_x**2 + dist_y**2)
                    if distance < connection_distance:
                        # Transparency of line varies with distance, simulating fading connections
                        alpha = 1.0 - (distance / connection_distance)
                        line_color_val = int(255 * alpha)
                        line_color = f'#{line_color_val:02x}{line_color_val:02x}{line_color_val:02x}' # Fading white
                        self.canvas.create_line(p1["x"], p1["y"], p2["x"], p2["y"], fill=line_color, width=1)

        # Schedule the next animation frame after a short delay
        self.master.after(20, self.animate) # Approx 50 FPS

# Entry point for the script
if __name__ == "__main__":
    root = tk.Tk() # Create the main Tkinter window
    app = InvigoratedVisualizer(root) # Instantiate the visualizer
    root.mainloop() # Start the Tkinter event loop, which runs the animation
