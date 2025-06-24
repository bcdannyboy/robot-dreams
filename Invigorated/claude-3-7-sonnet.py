#!/usr/bin/env python3
import pygame
import random
import math
import colorsys
from pygame import gfxdraw
import threading
import time

# Initialize pygame
pygame.init()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Invigorated")

# Colors
background = (10, 10, 15)
particle_colors = []

# Generate vibrant colors
for i in range(12):
    h = 0.55 + (i / 35)  # Primarily blues with some purples and cyans
    s = 0.85 + random.random() * 0.15
    v = 0.9 + random.random() * 0.1
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    particle_colors.append((int(r * 255), int(g * 255), int(b * 255)))

# Energy sources
energy_sources = []
for _ in range(4):
    energy_sources.append({
        'x': random.randint(100, width - 100),
        'y': random.randint(100, height - 100),
        'radius': random.randint(5, 15),
        'pulse': 0,
        'frequency': random.uniform(0.02, 0.05)
    })

# Particles
class Particle:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Start from a random energy source
        source = random.choice(energy_sources)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, source['radius'])
        
        self.x = source['x'] + math.cos(angle) * distance
        self.y = source['y'] + math.sin(angle) * distance
        self.size = random.uniform(1.5, 4)
        self.color = random.choice(particle_colors)
        self.speed = random.uniform(2.0, 6.0)
        
        # Direction is dynamic, influenced by "vigor"
        self.direction = random.uniform(0, 2 * math.pi)
        self.lifetime = random.uniform(1.5, 3.5)
        self.lived = 0
        self.alpha = 255
        self.energy = random.uniform(0.7, 1.0)
        
        # Trail effect
        self.trail = []
        self.trail_length = int(15 * self.speed / 3)
        
    def update(self, dt):
        # Update position based on speed and direction
        self.x += math.cos(self.direction) * self.speed * dt * 60
        self.y += math.sin(self.direction) * self.speed * dt * 60
        
        # Adjust direction based on energy fields
        self.adjust_direction()
        
        # Add position to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
        
        # Update lifetime and alpha
        self.lived += dt
        life_ratio = self.lived / self.lifetime
        
        # Alpha changes in a non-linear way, creating a more dynamic fade
        if life_ratio < 0.7:
            self.alpha = 255
        else:
            self.alpha = int(255 * (1 - ((life_ratio - 0.7) / 0.3)))
        
        # Adjust energy over time - particles gain and lose energy
        self.energy += random.uniform(-0.1, 0.2) * dt
        self.energy = max(0.4, min(1.2, self.energy))
        
        # Adjust speed based on energy
        self.speed = 2.0 + 4.0 * self.energy
        
        # Reset if lifetime is over or out of bounds
        if self.lived >= self.lifetime or not (0 < self.x < width and 0 < self.y < height):
            self.reset()
    
    def adjust_direction(self):
        # Dynamic direction changes based on energy fields and current energy level
        for source in energy_sources:
            dx = source['x'] - self.x
            dy = source['y'] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Particles are influenced by energy sources but not uniformly
            if distance < 200:
                # Direction to source
                target_direction = math.atan2(dy, dx)
                
                # Influence decreases with distance and varies with energy
                influence = (1 - distance/200) * 0.2 * self.energy
                
                # Add some randomness for more organic movement
                influence *= random.uniform(0.8, 1.2)
                
                # Calculate direction change
                angle_diff = (target_direction - self.direction + math.pi) % (2 * math.pi) - math.pi
                self.direction += angle_diff * influence
        
        # Add some random movement to make it more lively
        self.direction += random.uniform(-0.15, 0.15) * self.energy
    
    def draw(self, surface):
        # Draw trail with fading alpha
        if len(self.trail) > 1:
            points = self.trail.copy()
            alpha_step = self.alpha / len(points)
            
            for i in range(len(points) - 1):
                start_pos = points[i]
                end_pos = points[i + 1]
                
                # Calculate alpha for this segment
                segment_alpha = int(alpha_step * (i + 1))
                
                # Draw line with alpha
                color_with_alpha = (*self.color, segment_alpha)
                pygame.draw.line(
                    surface,
                    color_with_alpha,
                    start_pos,
                    end_pos,
                    max(1, int(self.size * (i / len(points)) * 0.8))
                )
        
        # Draw the particle with glow effect
        size_with_energy = self.size * (0.8 + self.energy * 0.4)
        
        # Draw with alpha
        s = pygame.Surface((int(size_with_energy * 3), int(size_with_energy * 3)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, self.alpha), 
                          (int(size_with_energy * 1.5), int(size_with_energy * 1.5)), 
                          int(size_with_energy))
        
        # Draw glow
        glow_size = size_with_energy * 2
        glow_surface = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
        
        # Create radial gradient for glow
        for i in range(int(glow_size), 0, -1):
            alpha = int((i / glow_size) * 50 * (self.energy * 0.7 + 0.3) * (self.alpha / 255))
            pygame.draw.circle(
                glow_surface, 
                (*self.color, alpha),
                (int(glow_size), int(glow_size)), 
                i
            )
        
        # Blit glow and particle
        surface.blit(
            glow_surface, 
            (self.x - glow_size, self.y - glow_size), 
            special_flags=pygame.BLEND_ADD
        )
        surface.blit(
            s, 
            (self.x - size_with_energy * 1.5, self.y - size_with_energy * 1.5)
        )

# Create particle system
particles = [Particle() for _ in range(200)]

# Audio pulse thread
def audio_pulse_thread():
    while True:
        for source in energy_sources:
            source['pulse'] = min(1.0, source['pulse'] + 0.5)
        time.sleep(0.7)  # Pulse rhythm

threading.Thread(target=audio_pulse_thread, daemon=True).start()

# Main loop
running = True
clock = pygame.time.Clock()
last_time = time.time()

# Energy field visualizer
def draw_energy_fields(surface):
    for source in energy_sources:
        # Update pulse
        source['pulse'] = max(0, source['pulse'] - 0.02)
        
        # Base size and pulse effect
        base_size = source['radius']
        pulse_size = base_size * (1 + source['pulse'] * 3)
        
        # Draw energy source
        for i in range(int(pulse_size), int(base_size), -1):
            alpha = int(50 * (i / pulse_size))
            color = random.choice(particle_colors)
            pygame.draw.circle(surface, (*color, alpha), (int(source['x']), int(source['y'])), i)
        
        # Draw core
        pygame.draw.circle(
            surface, 
            (255, 255, 255, 200), 
            (int(source['x']), int(source['y'])), 
            int(base_size * 0.7)
        )

while running:
    current_time = time.time()
    dt = current_time - last_time
    dt = min(dt, 0.05)  # Cap delta time to avoid large jumps
    last_time = current_time
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Clear screen with slight trail effect
    screen.fill(background)
    
    # Draw semi-transparent background for trail effect
    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.fill((10, 10, 15, 20))
    screen.blit(s, (0, 0))
    
    # Update energy sources positions with gentle movements
    for source in energy_sources:
        source['x'] += math.cos(time.time() * source['frequency']) * 0.5
        source['y'] += math.sin(time.time() * source['frequency'] * 1.3) * 0.5
    
    # Draw energy fields
    draw_energy_fields(screen)
    
    # Update and draw particles
    for particle in particles:
        particle.update(dt)
        particle.draw(screen)
    
    # Add occasional bursts of energy
    if random.random() < 0.02:
        source = random.choice(energy_sources)
        source['pulse'] = 1.0
        
        # Create a burst of particles
        for _ in range(15):
            p = random.choice(particles)
            p.reset()
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()