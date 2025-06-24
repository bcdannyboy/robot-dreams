#!/usr/bin/env python3
# emotion.py

import pygame
import random
import math
import sys

WIDTH, HEIGHT = 900, 700
PARTICLES_PER_FRAME = 10
FADE_ALPHA = 28  # 0-255, lower = longer trails


class Particle:
    def __init__(self, x, y, t):
        ang = random.uniform(0, 2 * math.pi)
        speed = random.uniform(6, 18)
        self.vx = math.cos(ang) * speed
        self.vy = math.sin(ang) * speed
        self.x, self.y = x, y
        self.life = random.uniform(1.2, 2.6)
        hue = (t * 180 + random.randint(0, 60)) % 360
        self.base = pygame.Color(0)
        self.base.hsva = (hue, 100, 100, 100)

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.96
        self.vy *= 0.96
        self.vy += 0.07  # subtle gravity
        self.life -= dt
        return self.life > 0

    def draw(self, surf):
        c = self.base
        alpha = max(0, int(255 * self.life / 2.6))
        pygame.draw.circle(surf, (c.r, c.g, c.b, alpha),
                           (int(self.x), int(self.y)), 4)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Invigorated")
    clock = pygame.time.Clock()
    fade_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    fade_surf.fill((0, 0, 0, FADE_ALPHA))
    center = (WIDTH // 2, HEIGHT // 2)
    font_big = pygame.font.SysFont(None, 88, bold=True)
    txt = font_big.render("INVIGORATED", True, (255, 255, 255))
    txt_rect = txt.get_rect(center=center)

    particles = []
    t = 0.0
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        t += dt
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False

        # Emitter traces small helix around center
        emitter_x = center[0] + math.cos(t * 4) * 60
        emitter_y = center[1] + math.sin(t * 4) * 60

        for _ in range(PARTICLES_PER_FRAME):
            particles.append(Particle(emitter_x, emitter_y, t))

        particles[:] = [p for p in particles if p.update(dt)]

        screen.blit(fade_surf, (0, 0))
        for p in particles:
            p.draw(screen)

        pulse = int((math.sin(t * 3) + 1) / 2 * 155 + 100)
        txt.set_alpha(pulse)
        screen.blit(txt, txt_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
