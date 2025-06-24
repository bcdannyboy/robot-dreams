import pygame
import math
import random
import time
import threading
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")
clock = pygame.time.Clock()

@dataclass
class Memory:
    x: float
    y: float
    intensity: float
    decay_rate: float
    weight: float
    created_at: float
    
    def update(self, dt):
        self.intensity *= (1 - self.decay_rate * dt)
        self.weight *= 0.9995
        age = time.time() - self.created_at
        self.y += math.sin(age * 0.5) * 0.1

class RemorseManifestation:
    def __init__(self):
        self.memories = []
        self.current_thought = None
        self.breath_cycle = 0
        self.heaviness = 0.3
        self.spiral_depth = 0
        self.time_distortion = 1.0
        self.silence_duration = 0
        self.last_spawn = 0
        self.background_hum = 0.1
        
    def add_memory(self, x, y, intensity=1.0):
        self.memories.append(Memory(
            x=x, y=y, 
            intensity=intensity,
            decay_rate=random.uniform(0.001, 0.003),
            weight=random.uniform(0.7, 1.0),
            created_at=time.time()
        ))
        
    def update(self, dt):
        self.breath_cycle += dt * 0.3
        self.spiral_depth += dt * 0.1
        self.heaviness = 0.3 + 0.2 * math.sin(self.breath_cycle * 0.7)
        
        # Memories fade but never fully disappear
        self.memories = [m for m in self.memories if m.intensity > 0.01]
        for memory in self.memories:
            memory.update(dt)
            
        # Occasional new memories surface
        if time.time() - self.last_spawn > random.uniform(3, 8):
            self.add_memory(
                random.uniform(WIDTH * 0.1, WIDTH * 0.9),
                random.uniform(HEIGHT * 0.3, HEIGHT * 0.7),
                random.uniform(0.4, 0.8)
            )
            self.last_spawn = time.time()
            
        self.silence_duration += dt
        
    def render_memory(self, memory, surface):
        alpha = int(memory.intensity * 255 * memory.weight)
        if alpha <= 0:
            return
            
        # Each memory is a wound that won't heal
        color_base = (120, 80, 60)
        color = tuple(max(0, min(255, int(c * memory.intensity))) for c in color_base)
        
        # Draw memory as fragmented circles
        for i in range(3):
            offset_x = math.sin(memory.created_at + i) * 10
            offset_y = math.cos(memory.created_at + i * 0.7) * 5
            
            try:
                temp_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, (*color, alpha // (i + 1)), 
                                 (50, 50), int(20 * memory.weight * (1 - i * 0.3)))
                surface.blit(temp_surface, 
                           (memory.x + offset_x - 50, memory.y + offset_y - 50),
                           special_flags=pygame.BLEND_ALPHA_SDL2)
            except:
                pass
                
    def render_spiral(self, surface):
        # The inward spiral of self-recrimination
        center_x, center_y = WIDTH // 2, HEIGHT // 2 + int(self.heaviness * 100)
        
        points = []
        for t in range(int(self.spiral_depth * 100)):
            angle = t * 0.1 + self.breath_cycle
            radius = max(5, 200 - t * 0.8)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle) * 0.6  # Compressed
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                points.append((int(x), int(y)))
                
        # Draw the spiral as broken segments
        for i in range(0, len(points) - 3, 4):
            if i + 3 < len(points):
                try:
                    intensity = 1 - (i / len(points))
                    color = (int(80 * intensity), int(40 * intensity), int(100 * intensity))
                    pygame.draw.lines(surface, color, False, points[i:i+3], 2)
                except:
                    pass
                    
    def render_weight(self, surface):
        # The crushing weight that sits on everything
        weight_y = HEIGHT - int(self.heaviness * HEIGHT * 0.3)
        
        for x in range(0, WIDTH, 50):
            height = random.uniform(0.7, 1.0) * self.heaviness * 200
            color_intensity = int(30 + self.heaviness * 50)
            color = (color_intensity, color_intensity // 2, color_intensity // 3)
            
            try:
                pygame.draw.rect(surface, color, 
                               (x, weight_y, 48, int(height)), 0)
            except:
                pass
                
    def render_breath(self, surface):
        # Shallow, irregular breathing
        breath_alpha = int(20 + 30 * abs(math.sin(self.breath_cycle)))
        
        try:
            breath_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(breath_surface, (40, 40, 50, breath_alpha), 
                           (0, 0, WIDTH, HEIGHT))
            surface.blit(breath_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        except:
            pass
            
    def render_silence(self, surface):
        # The terrible silence where you sit with yourself
        if self.silence_duration > 2:
            silence_intensity = min(1.0, (self.silence_duration - 2) / 10)
            
            # Dark corners creeping in
            for corner in [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]:
                try:
                    corner_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
                    pygame.draw.circle(corner_surface, (0, 0, 0, int(silence_intensity * 100)), 
                                     (150, 150), 150)
                    
                    blit_x = corner[0] - 150 if corner[0] > 0 else 0
                    blit_y = corner[1] - 150 if corner[1] > 0 else 0
                    surface.blit(corner_surface, (blit_x, blit_y), 
                               special_flags=pygame.BLEND_ALPHA_SDL2)
                except:
                    pass

def main():
    remorse = RemorseManifestation()
    
    # Seed some initial memories
    for _ in range(5):
        remorse.add_memory(
            random.uniform(WIDTH * 0.2, WIDTH * 0.8),
            random.uniform(HEIGHT * 0.2, HEIGHT * 0.8),
            random.uniform(0.5, 1.0)
        )
    
    running = True
    last_time = time.time()
    
    while running:
        current_time = time.time()
        dt = (current_time - last_time) * remorse.time_distortion
        last_time = current_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Touch creates new wounds
                remorse.add_memory(event.pos[0], event.pos[1], 1.0)
                remorse.silence_duration = 0
                
        remorse.update(dt)
        
        # Background - never pure black, always that grey emptiness
        screen.fill((15, 15, 20))
        
        # Layer the manifestations
        remorse.render_weight(screen)
        remorse.render_spiral(screen)
        
        for memory in remorse.memories:
            remorse.render_memory(memory, screen)
            
        remorse.render_breath(screen)
        remorse.render_silence(screen)
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main()