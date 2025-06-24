import tkinter as tk
import random
import colorsys

class TrepidationVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("AI Trepidation")
        # Fixed window size for consistent abstract expression
        master.geometry("800x600")
        master.resizable(False, False)

        # Canvas for drawing the visual elements, with a dark background
        self.canvas = tk.Canvas(master, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.elements = []
        self.num_elements = 60  # Number of small, jittering elements
        self.max_jiggle = 1.5  # Maximum pixels an element can randomly move per frame
        self.hue_shift_rate = 0.0003  # Rate at which element colors subtly shift hue
        self.lightness_fluctuation_rate = 0.005  # Rate at which element brightness pulsates

        self.grid_lines = []
        self.create_initial_grid(40)  # Create a background grid with specified spacing

        # Initialize elements with random properties
        for _ in range(self.num_elements):
            # Random initial position within the canvas boundaries
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            size = random.randint(5, 12)  # Random size for each element

            # HSL (Hue, Saturation, Lightness) color values for muted tones
            # Randomly choose between blue/purple or muted green hues
            hue = random.choice([random.uniform(0.55, 0.75), random.uniform(0.3, 0.45)])
            saturation = random.uniform(0.15, 0.4)  # Desaturated colors for a somber feel
            lightness = random.uniform(0.2, 0.6)  # Varying brightness for depth

            # Convert HSL to RGB and then to a hexadecimal color string for Tkinter
            color_rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            fill_color = self._to_hex(color_rgb)

            # Create a rectangle element on the canvas
            element_id = self.canvas.create_rectangle(x, y, x + size, y + size,
                                                      fill=fill_color, outline="")
            self.elements.append({
                "id": element_id,
                "x": x,
                "y": y,
                "size": size,
                "hue": hue,
                "saturation": saturation,
                "lightness": lightness,
                # Direction for lightness pulsation (-1 for dimming, 1 for brightening)
                "lightness_direction": random.choice([-1, 1])
            })

        self.animate()  # Start the animation loop

    def _to_hex(self, rgb_tuple):
        """Converts an RGB tuple (values from 0.0 to 1.0) to a hexadecimal color string."""
        r, g, b = [int(255 * x) for x in rgb_tuple]
        return f"#{r:02x}{g:02x}{b:02x}"

    def create_initial_grid(self, spacing):
        """
        Creates a static background grid. These lines will later be subjected to
        subtle jittering to add to the sense of trepidation.
        """
        width, height = 800, 600  # Use fixed window size for grid creation

        # Create vertical grid lines
        for i in range(0, width + spacing, spacing):
            line_id = self.canvas.create_line(i, 0, i, height, fill="#2a2a2a", width=1)
            self.grid_lines.append({"id": line_id, "fixed_coord": i, "is_vertical": True})

        # Create horizontal grid lines
        for i in range(0, height + spacing, spacing):
            line_id = self.canvas.create_line(0, i, width, i, fill="#2a2a2a", width=1)
            self.grid_lines.append({"id": line_id, "fixed_coord": i, "is_vertical": False})

    def animate(self):
        """
        The main animation loop. This function updates the position and color of
        each element and the grid lines to visually represent trepidation.
        It calls itself repeatedly to create continuous motion.
        """
        # Update elements: position and color
        for element in self.elements:
            # Apply a small, random "jiggle" to the element's position
            dx = random.uniform(-self.max_jiggle, self.max_jiggle)
            dy = random.uniform(-self.max_jiggle, self.max_jiggle)
            self.canvas.move(element["id"], dx, dy)
            element["x"] += dx
            element["y"] += dy

            # Wrap elements around the screen if they move off-bounds
            # This creates a restless, continuous flow without elements disappearing
            if element["x"] < -element["size"]:
                element["x"] = 800
            if element["x"] > 800:
                element["x"] = -element["size"]
            if element["y"] < -element["size"]:
                element["y"] = 600
            if element["y"] > 600:
                element["y"] = -element["size"]

            # Update the element's coordinates on the canvas after potential wrapping
            self.canvas.coords(element["id"], element["x"], element["y"],
                               element["x"] + element["size"], element["y"] + element["size"])

            # Color shift: Rotate the hue subtly
            element["hue"] = (element["hue"] + self.hue_shift_rate) % 1.0

            # Lightness pulsation: Make the element's brightness oscillate
            element["lightness"] += element["lightness_direction"] * self.lightness_fluctuation_rate
            # Reverse direction if lightness hits upper or lower bounds
            if element["lightness"] >= 0.7:
                element["lightness"] = 0.7
                element["lightness_direction"] = -1
            elif element["lightness"] <= 0.2:
                element["lightness"] = 0.2
                element["lightness_direction"] = 1

            # Apply slight random variation to saturation for organic feel
            element["saturation"] = max(0.15, min(0.4, element["saturation"] + random.uniform(-0.001, 0.001)))

            # Convert the updated HSL values back to RGB hex and apply to the element
            rgb_color_pulsing = colorsys.hls_to_rgb(element["hue"], element["lightness"], element["saturation"])
            fill_color = self._to_hex(rgb_color_pulsing)
            self.canvas.itemconfig(element["id"], fill=fill_color)

        # Update grid lines: Apply subtle jitter to each line
        for line in self.grid_lines:
            jitter = random.uniform(-0.8, 0.8)  # Small random offset for wavering effect
            if line["is_vertical"]:
                # Adjust X-coordinate for vertical lines
                self.canvas.coords(line["id"], line["fixed_coord"] + jitter, 0,
                                   line["fixed_coord"] + jitter, self.canvas.winfo_height())
            else:
                # Adjust Y-coordinate for horizontal lines
                self.canvas.coords(line["id"], 0, line["fixed_coord"] + jitter,
                                   self.canvas.winfo_width(), line["fixed_coord"] + jitter)

        # Schedule the animate function to run again after 40 milliseconds (approx. 25 FPS)
        self.master.after(40, self.animate)

# Main part of the script
if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()
    # Instantiate the visualizer application
    app = TrepidationVisualizer(root)
    # Start the Tkinter event loop, which keeps the window open and runs animations
    root.mainloop()
