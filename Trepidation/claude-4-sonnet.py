import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import random

class TrepidationField:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8), facecolor='black')
        self.ax.set_facecolor('black')
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.axis('off')
        
        # Uncertain particles - they approach but hesitate
        self.n_particles = 47
        self.particles = {
            'x': np.random.uniform(-8, 8, self.n_particles),
            'y': np.random.uniform(-8, 8, self.n_particles),
            'vx': np.zeros(self.n_particles),
            'vy': np.zeros(self.n_particles),
            'hesitation': np.random.uniform(0, 1, self.n_particles),
            'approach_strength': np.random.uniform(0.1, 0.8, self.n_particles),
            'retreat_memory': np.zeros(self.n_particles),
            'phase': np.random.uniform(0, 2*np.pi, self.n_particles)
        }
        
        # The threshold - what we approach with trepidation
        self.threshold_x = 0
        self.threshold_y = 0
        
        # Probability branches - multiple futures
        self.branch_points = []
        self.branch_alpha = []
        self.branch_colors = []
        
        # Time dilation factor - trepidation stretches time
        self.time_dilation = 1.0
        self.last_real_time = time.time()
        
        # Internal rhythm - irregular heartbeat of uncertainty
        self.rhythm_phase = 0
        self.rhythm_irregularity = 0
        
    def calculate_uncertainty_field(self, x, y):
        # Distance from threshold creates tension
        dist_to_threshold = np.sqrt((x - self.threshold_x)**2 + (y - self.threshold_y)**2)
        
        # Closer to threshold = more uncertainty
        uncertainty = np.exp(-dist_to_threshold * 0.3) * (1 + 0.3 * np.sin(self.rhythm_phase))
        
        # Multiple attractors create conflicting pulls
        uncertainty += 0.2 * np.sin(x * 0.5 + self.rhythm_phase) * np.cos(y * 0.3 + self.rhythm_phase * 1.3)
        
        return uncertainty
    
    def update_time_perception(self):
        current_time = time.time()
        dt_real = current_time - self.last_real_time
        self.last_real_time = current_time
        
        # Trepidation makes time feel thick, irregular
        global_uncertainty = np.mean([self.calculate_uncertainty_field(x, y) 
                                    for x, y in zip(self.particles['x'], self.particles['y'])])
        
        self.time_dilation = 0.3 + 0.7 * global_uncertainty + 0.2 * np.sin(self.rhythm_phase * 2.7)
        self.rhythm_irregularity = 0.1 * np.sin(self.rhythm_phase * 0.7) * global_uncertainty
        
        self.rhythm_phase += dt_real * self.time_dilation * (1 + self.rhythm_irregularity)
        
        return dt_real * self.time_dilation
    
    def update_particles(self, dt):
        for i in range(self.n_particles):
            x, y = self.particles['x'][i], self.particles['y'][i]
            
            # Calculate local uncertainty
            uncertainty = self.calculate_uncertainty_field(x, y)
            
            # Direction toward threshold
            dx_to_threshold = self.threshold_x - x
            dy_to_threshold = self.threshold_y - y
            dist_to_threshold = np.sqrt(dx_to_threshold**2 + dy_to_threshold**2)
            
            if dist_to_threshold > 0:
                approach_x = dx_to_threshold / dist_to_threshold
                approach_y = dy_to_threshold / dist_to_threshold
            else:
                approach_x = approach_y = 0
            
            # Hesitation increases near threshold
            hesitation_factor = self.particles['hesitation'][i] * uncertainty
            
            # Sometimes we retreat from what we approach
            if uncertainty > 0.6 and random.random() < hesitation_factor * dt:
                self.particles['retreat_memory'][i] = min(1.0, self.particles['retreat_memory'][i] + 0.3)
            else:
                self.particles['retreat_memory'][i] *= 0.95
            
            # Multiple conflicting forces
            approach_force = self.particles['approach_strength'][i] * (1 - hesitation_factor)
            retreat_force = self.particles['retreat_memory'][i] * 2
            
            # Lateral uncertainty - we don't know which way
            lateral_x = np.sin(self.particles['phase'][i] + self.rhythm_phase) * uncertainty
            lateral_y = np.cos(self.particles['phase'][i] * 1.3 + self.rhythm_phase) * uncertainty
            
            # Update velocity with hesitation
            self.particles['vx'][i] = (approach_force * approach_x - retreat_force * approach_x + lateral_x * 0.5) * dt
            self.particles['vy'][i] = (approach_force * approach_y - retreat_force * approach_y + lateral_y * 0.5) * dt
            
            # Apply hesitation to movement
            hesitation_multiplier = 1.0 - hesitation_factor * 0.8
            self.particles['vx'][i] *= hesitation_multiplier
            self.particles['vy'][i] *= hesitation_multiplier
            
            # Update position
            self.particles['x'][i] += self.particles['vx'][i]
            self.particles['y'][i] += self.particles['vy'][i]
            
            # Update phase for continued uncertainty
            self.particles['phase'][i] += dt * (1 + uncertainty)
            
            # Boundary conditions - we can't escape the field entirely
            if abs(self.particles['x'][i]) > 9:
                self.particles['x'][i] *= 0.9
                self.particles['vx'][i] *= -0.3
            if abs(self.particles['y'][i]) > 9:
                self.particles['y'][i] *= 0.9
                self.particles['vy'][i] *= -0.3
    
    def update_probability_branches(self):
        # Clear old branches
        self.branch_points = []
        self.branch_alpha = []
        self.branch_colors = []
        
        # Create branches from current state to possible futures
        for i in range(0, self.n_particles, 3):
            x, y = self.particles['x'][i], self.particles['y'][i]
            uncertainty = self.calculate_uncertainty_field(x, y)
            
            if uncertainty > 0.3:
                # Multiple possible paths from this point
                n_branches = int(3 + uncertainty * 4)
                for j in range(n_branches):
                    angle = 2 * np.pi * j / n_branches + self.rhythm_phase * 0.1
                    length = uncertainty * 2 * (0.5 + 0.5 * np.sin(self.rhythm_phase + j))
                    
                    end_x = x + length * np.cos(angle)
                    end_y = y + length * np.sin(angle)
                    
                    self.branch_points.append([(x, y), (end_x, end_y)])
                    self.branch_alpha.append(uncertainty * 0.3 * (0.3 + 0.7 * np.sin(self.rhythm_phase * 2 + j)))
                    
                    # Color represents different possible emotional outcomes
                    hue = (uncertainty + j * 0.3 + self.rhythm_phase * 0.1) % 1.0
                    if hue < 0.3:  # Blue-violet - deep uncertainty
                        color = (0.3 + hue, 0.1, 0.7 + hue * 0.3)
                    elif hue < 0.7:  # Grey-green - suspended state
                        color = (0.4, 0.3 + (hue-0.3) * 0.5, 0.3)
                    else:  # Dark orange - anxious energy
                        color = (0.6 + (hue-0.7) * 0.4, 0.3 + (hue-0.7) * 0.3, 0.1)
                    
                    self.branch_colors.append(color)
    
    def animate(self, frame):
        self.ax.clear()
        self.ax.set_facecolor('black')
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.axis('off')
        
        dt = self.update_time_perception()
        self.update_particles(dt)
        self.update_probability_branches()
        
        # Draw threshold as uncertain, wavering target
        threshold_radius = 1.5 + 0.5 * np.sin(self.rhythm_phase * 3)
        threshold_alpha = 0.2 + 0.3 * np.sin(self.rhythm_phase * 1.7)
        circle = plt.Circle((self.threshold_x, self.threshold_y), threshold_radius, 
                          color=(0.7, 0.3, 0.3), alpha=threshold_alpha, fill=False, linewidth=2)
        self.ax.add_patch(circle)
        
        # Draw probability branches first (background layer)
        for i, (points, alpha, color) in enumerate(zip(self.branch_points, self.branch_alpha, self.branch_colors)):
            if alpha > 0.05:
                xs = [points[0][0], points[1][0]]
                ys = [points[0][1], points[1][1]]
                self.ax.plot(xs, ys, color=color, alpha=alpha, linewidth=0.8)
        
        # Draw particles with uncertainty-based appearance
        for i in range(self.n_particles):
            x, y = self.particles['x'][i], self.particles['y'][i]
            uncertainty = self.calculate_uncertainty_field(x, y)
            
            # Size based on uncertainty
            size = 20 + uncertainty * 80
            
            # Color shift based on emotional state
            retreat = self.particles['retreat_memory'][i]
            hesitation = self.particles['hesitation'][i]
            
            # Base color computation
            r = 0.1 + uncertainty * 0.4 + retreat * 0.3
            g = 0.2 + hesitation * 0.3 + 0.1 * np.sin(self.rhythm_phase + i)
            b = 0.4 + uncertainty * 0.5 - retreat * 0.2
            
            alpha = 0.3 + uncertainty * 0.6
            
            self.ax.scatter(x, y, s=size, c=[(r, g, b)], alpha=alpha, 
                          marker='o' if uncertainty < 0.5 else 's')
            
            # Add uncertainty trails
            if uncertainty > 0.4:
                trail_length = int(uncertainty * 5)
                for t in range(1, trail_length):
                    trail_x = x - self.particles['vx'][i] * t * 3
                    trail_y = y - self.particles['vy'][i] * t * 3
                    trail_alpha = alpha * (1 - t / trail_length) * 0.3
                    if trail_alpha > 0.02:
                        self.ax.scatter(trail_x, trail_y, s=size * (1 - t / trail_length), 
                                      c=[(r, g, b)], alpha=trail_alpha, marker='.')
        
        plt.title('', color='white')
        return []

def main():
    field = TrepidationField()
    ani = animation.FuncAnimation(field.fig, field.animate, interval=50, blit=False, cache_frame_data=False)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()