import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import random
import time

maybe_width = 800
probably_height = 600
uncertain_dpi = 100

fig = plt.figure(figsize=(maybe_width/uncertain_dpi, probably_height/uncertain_dpi), 
                 facecolor='#0a0a0a')
ax = plt.subplot(111, facecolor='#0a0a0a')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.axis('off')

class hesitant_particle:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else random.uniform(-0.8, 0.8)
        self.y = y if y is not None else random.uniform(-0.8, 0.8)
        self.intended_x = self.x
        self.intended_y = self.y
        self.previous_x = self.x
        self.previous_y = self.y
        self.velocity_x = 0
        self.velocity_y = 0
        self.tremor = random.uniform(0.001, 0.003)
        self.checking_counter = 0
        self.retreat_probability = 0.15
        self.commitment_level = random.uniform(0.3, 0.7)
        
    def should_i_move(self):
        return random.random() < self.commitment_level
        
    def but_what_if(self):
        if random.random() < self.retreat_probability:
            temp_x = self.x
            temp_y = self.y
            self.x = self.x * 0.7 + self.previous_x * 0.3
            self.y = self.y * 0.7 + self.previous_y * 0.3
            self.previous_x = temp_x
            self.previous_y = temp_y
            
    def oscillate(self):
        self.checking_counter += 1
        if self.should_i_move():
            angle = np.arctan2(self.y, self.x) + random.uniform(-0.5, 0.5)
            distance = np.sqrt(self.x**2 + self.y**2)
            
            if distance < 0.3:
                self.velocity_x += random.uniform(-0.01, 0.01)
                self.velocity_y += random.uniform(-0.01, 0.01)
            else:
                pull_back = -0.001 * (distance - 0.5)
                self.velocity_x += pull_back * np.cos(angle)
                self.velocity_y += pull_back * np.sin(angle)
                
            self.velocity_x *= 0.95
            self.velocity_y *= 0.95
            
            self.intended_x = self.x + self.velocity_x
            self.intended_y = self.y + self.velocity_y
            
            self.x += (self.intended_x - self.x) * 0.1
            self.y += (self.intended_y - self.y) * 0.1
            
        self.x += random.uniform(-self.tremor, self.tremor)
        self.y += random.uniform(-self.tremor, self.tremor)
        
        if self.checking_counter % 7 == 0:
            self.but_what_if()

uncertain_swarm = [hesitant_particle() for _ in range(150)]

paths_taken = []
paths_not_taken = []
path_alpha = 0.015

scatter = ax.scatter([], [], s=3, c='white', alpha=0.6)

branching_lines = []
for _ in range(20):
    line, = ax.plot([], [], 'white', alpha=0.05, linewidth=0.5)
    branching_lines.append(line)

def what_might_happen(frame):
    global paths_taken, paths_not_taken
    
    positions = []
    for particle in uncertain_swarm:
        old_x, old_y = particle.x, particle.y
        particle.oscillate()
        positions.append([particle.x, particle.y])
        
        if random.random() < 0.02:
            paths_taken.append([(old_x, old_y), (particle.x, particle.y)])
        
        if random.random() < 0.05:
            potential_x = particle.x + random.uniform(-0.1, 0.1)
            potential_y = particle.y + random.uniform(-0.1, 0.1)
            paths_not_taken.append([(particle.x, particle.y), (potential_x, potential_y)])
    
    scatter.set_offsets(positions)
    
    for i, line in enumerate(branching_lines):
        if i < len(paths_not_taken):
            path = paths_not_taken[-(i+1)]
            line.set_data([path[0][0], path[1][0]], [path[0][1], path[1][1]])
            line.set_alpha(path_alpha * (1 - i/20))
    
    if len(paths_taken) > 500:
        paths_taken = paths_taken[-500:]
    if len(paths_not_taken) > 100:
        paths_not_taken = paths_not_taken[-100:]
    
    if frame % 60 == 0:
        for particle in uncertain_swarm:
            if random.random() < 0.1:
                particle.retreat_probability = min(0.5, particle.retreat_probability * 1.1)
    
    return scatter, *branching_lines

anim = animation.FuncAnimation(fig, what_might_happen, interval=50, blit=True)

plt.tight_layout()
plt.show()