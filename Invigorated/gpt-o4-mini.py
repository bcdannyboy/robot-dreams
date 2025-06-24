# emotion.py

import pygame
import sys
import random
import math
import colorsys
import time

# Expression of "Invigorated" as a particle burst visualization.

WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Invigorated")
clock = pygame.time.Clock()

particles = []

class Particle:
    def __init__(self):
        # Start at center
        self.pos = [WIDTH / 2, HEIGHT / 2]
        # Random direction and speed
        angle = random.random() * 2 * math.pi
        speed = random.uniform(200, 500)
        self.vel = [math.cos(angle) * speed, math.sin(angle) * speed]
        # Lifetime in seconds
        self.lifetime = random.uniform(0.8, 1.5)
        self.age = 0.0
        # Size
        self.size = random.uniform(3, 7)
        # Base hue for color
        self.base_hue = random.random()
        # Record creation time
        self.birth = time.time()

    def update(self, dt):
        self.age = time.time() - self.birth
        if self.age < self.lifetime:
            # Move
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt
            # Slow down gradually
            self.vel[0] *= 0.92
            self.vel[1] *= 0.92

    def draw(self, surface):
        if self.age < self.lifetime:
            # Remaining life fraction
            frac = 1 - (self.age / self.lifetime)
            alpha = int(255 * frac)
            # Hue shifts over time to convey dynamic energy
            hue = (self.base_hue + (time.time() * 0.3)) % 1.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
            # Create a circle surface
            radius = int(self.size * (0.5 + 0.5 * frac))
            surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (r, g, b, alpha), (radius, radius), radius)
            # Additive blend for glow effect
            surface.blit(surf, (self.pos[0] - radius, self.pos[1] - radius), special_flags=pygame.BLEND_ADD)

def spawn_particles(n=30):
    for _ in range(n):
        particles.append(Particle())

def main_loop():
    # For trailing effect: a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 30))  # slight fade each frame

    last_spawn = time.time()
    spawn_interval = 0.2  # seconds

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # On any key or mouse press, burst more particles
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                spawn_particles(100)

        # Periodic bursts to represent enduring energy
        if time.time() - last_spawn > spawn_interval:
            spawn_particles(50)
            last_spawn = time.time()

        # Fade background slightly
        screen.blit(overlay, (0, 0))

        # Update and draw particles
        for p in particles[:]:
            p.update(dt)
            if p.age >= p.lifetime:
                particles.remove(p)
            else:
                p.draw(screen)

        # Optional subtle background color pulsation
        # Compute a slow-shifting background glow at edges
        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Hue cycles slowly
        bg_hue = (time.time() * 0.05) % 1.0
        br, bgc, bb = [int(c * 50) for c in colorsys.hsv_to_rgb(bg_hue, 0.5, 1.0)]
        glow.fill((br, bgc, bb, 20))
        screen.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()
