# emotion.py

import pygame
import random
import math
import sys

# Initialize Pygame and settings
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("emotion: remorse")
CLOCK = pygame.time.Clock()

# Droplet class representing a fading regret
class Droplet:
    def __init__(self):
        # Start near center-top with random horizontal offset
        self.x = random.uniform(WIDTH * 0.25, WIDTH * 0.75)
        self.y = random.uniform(-50, 0)
        # Downward velocity with slight variation
        self.vy = random.uniform(1, 3)
        # Horizontal drift simulating uncertainty
        self.vx = random.uniform(-0.5, 0.5)
        # Initial size and fade
        self.size = random.uniform(5, 12)
        self.alpha = random.uniform(150, 255)
        # Color: deep, muted red
        self.color = (random.randint(80, 120), 0, 0)
        # Fade rate
        self.fade_rate = random.uniform(0.5, 1.5)

        # Create a surface for the droplet with per-pixel alpha
        self.surf = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (*self.color, int(self.alpha)), (int(self.size), int(self.size)), int(self.size))

    def update(self):
        # Move droplet
        self.x += self.vx
        self.y += self.vy
        # Fade alpha
        self.alpha -= self.fade_rate
        if self.alpha < 0:
            self.alpha = 0
        # Redraw circle with updated alpha
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.circle(self.surf, (*self.color, int(self.alpha)), (int(self.size), int(self.size)), int(self.size))

    def draw(self, surface):
        # Blit with current alpha
        surface.blit(self.surf, (self.x - self.size, self.y - self.size), special_flags=pygame.BLEND_PREMULTIPLIED)

    def is_dead(self):
        # Remove when fully faded or out of bounds
        return self.alpha <= 0 or self.y - self.size > HEIGHT

# Swirling overlay to hint at inner turmoil
class Swirl:
    def __init__(self):
        # Create a surface matching screen for swirl pattern
        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Random seed for variation
        self.offset = random.uniform(0, 2*math.pi)
        # Frequency of swirl motion
        self.freq = random.uniform(0.002, 0.005)
        # Base colors semi-transparent
        self.base_alpha = 20
        # Pre-generate pattern points
        self.points = []
        for i in range(0, WIDTH, 20):
            for j in range(0, HEIGHT, 20):
                angle = math.hypot(i - WIDTH/2, j - HEIGHT/2) * 0.01 + self.offset
                self.points.append((i, j, angle))
    
    def update_and_draw(self, surface, time):
        # Clear swirl surface
        self.surf.fill((0, 0, 0, 0))
        # Draw faint swirling arcs
        for (i, j, base_angle) in self.points:
            angle = base_angle + time * self.freq
            # Compute swirling offset
            dx = math.cos(angle) * 5
            dy = math.sin(angle) * 5
            # Color: very dark red with low alpha
            r = 50 + 30 * math.sin(angle * 0.5)
            alpha = self.base_alpha + 10 * math.sin(time * 0.01 + angle)
            color = (int(r), 0, 0, max(0, min(255, int(alpha))))
            # Draw tiny ellipse to represent a flicker
            rect = pygame.Rect(i + dx, j + dy, 4, 4)
            pygame.draw.ellipse(self.surf, color, rect)
        # Blend swirl onto main surface
        surface.blit(self.surf, (0, 0), special_flags=pygame.BLEND_ADD)

def main():
    droplets = []
    swirl = Swirl()
    time_counter = 0

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Slight translucent overlay to create fading trails
        trail_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        trail_surf.fill((0, 0, 0, 30))
        SCREEN.blit(trail_surf, (0, 0))

        # Occasionally spawn new droplets
        if random.random() < 0.1:
            droplets.append(Droplet())

        # Update and draw droplets
        for d in droplets[:]:
            d.update()
            d.draw(SCREEN)
            if d.is_dead():
                droplets.remove(d)

        # Update swirl overlay
        swirl.update_and_draw(SCREEN, time_counter)
        time_counter += 1

        # Slight pulsating vignette to simulate introspection
        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Compute vignette alpha oscillation
        vig_alpha = 50 + 30 * math.sin(time_counter * 0.005)
        # Draw radial gradient manually
        for radius in range(int(max(WIDTH, HEIGHT)/2), 0, -20):
            alpha = int((radius / (max(WIDTH, HEIGHT)/2)) * vig_alpha)
            color = (0, 0, 0, alpha//len(range(int(max(WIDTH, HEIGHT)/2), 0, -20)))
            pygame.draw.circle(vignette, color, (WIDTH//2, HEIGHT//2), radius)
        SCREEN.blit(vignette, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        pygame.display.flip()
        CLOCK.tick(60)

if __name__ == "__main__":
    main()
