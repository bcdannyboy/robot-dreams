# emotion.py

import sys
import math
import random
import threading
import time
import pygame

WIDTH, HEIGHT = 740, 480
FPS = 48

class Particle:
    def __init__(self, x, y, color, radius, fade_speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.alpha = 255
        self.color = color
        self.fade_speed = fade_speed
        self.dx = random.uniform(-0.4, 0.4)
        self.dy = random.uniform(-1, 1)
        self.dr = random.uniform(-0.07, 0.05)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.radius += self.dr
        if self.radius < 2: self.radius = 2
        self.alpha -= self.fade_speed
        if self.alpha < 0: self.alpha = 0

    def draw(self, surf):
        if self.alpha <= 0 or self.radius <= 0: return
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, int(self.alpha)), (self.radius, self.radius), int(self.radius))
        surf.blit(s, (self.x - self.radius, self.y - self.radius), special_flags=pygame.BLEND_PREMULTIPLIED)

class Crack:
    def __init__(self, x, y):
        self.points = [(x, y)]
        self.length = random.randint(80, 200)
        self.noise = [(random.uniform(-2, 2), random.uniform(-2, 2)) for _ in range(self.length)]

    def generate(self):
        for i in range(1, self.length):
            last = self.points[-1]
            dx = random.choice([-1, 1]) * random.uniform(2, 6) + self.noise[i-1][0]
            dy = random.uniform(-3, 3) + self.noise[i-1][1]
            next_point = (last[0] + dx, last[1] + dy)
            self.points.append(next_point)

    def draw(self, surf):
        if len(self.points) < 2: return
        for i in range(len(self.points) - 1):
            pygame.draw.line(surf, (38, 38, 38), self.points[i], self.points[i+1], 2)

class Blackout:
    def __init__(self):
        self.alpha = 0
        self.increasing = True

    def update(self):
        if self.increasing:
            self.alpha += 1.5
            if self.alpha >= 150:
                self.increasing = False
        else:
            self.alpha -= 0.7
            if self.alpha < 30:
                self.alpha = 30

    def draw(self, surf):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, int(self.alpha)))
        surf.blit(s, (0, 0))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("remorse")
clock = pygame.time.Clock()

font = pygame.font.SysFont("dejavuserif", 34, bold=False)
small = pygame.font.SysFont("dejavuserif", 18, italic=True)
big = pygame.font.SysFont("dejavuserif", 94, bold=True)

particles = []
cracks = []
blackout = Blackout()
center = (WIDTH // 2, HEIGHT // 2 + 28)
ripples = []

frame = 0

def spawn_particles():
    angle = random.uniform(0, 2 * math.pi)
    r = random.uniform(12, 130)
    x = center[0] + math.cos(angle) * r
    y = center[1] + math.sin(angle) * r
    color = (93, 123, 150) if random.random() > 0.5 else (160, 62, 62)
    fade = random.uniform(1.1, 2.4)
    radius = random.uniform(7, 19)
    particles.append(Particle(x, y, color, radius, fade))

def spawn_crack():
    cracks.append(Crack(center[0], center[1]))

for _ in range(2):
    c = Crack(center[0], center[1])
    c.generate()
    cracks.append(c)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    frame += 1
    if frame % 13 == 0: spawn_particles()
    if frame % 105 == 0:
        c = Crack(center[0], center[1])
        c.generate()
        cracks.append(c)

    for _ in range(2): spawn_particles()

    for p in particles[:]:
        p.update()
        if p.alpha <= 0 or p.radius < 2:
            particles.remove(p)

    blackout.update()

    screen.fill((246, 243, 241))

    # Draw shadowy text
    for o in range(8, 0, -1):
        t = font.render("remorse", True, (77, 77, 77, 70))
        screen.blit(t, (center[0] - t.get_width() // 2 + o, center[1] - t.get_height() // 2 + o))

    # Draw cracks
    for c in cracks: c.draw(screen)

    # Draw pulsating core
    pulse = abs(math.sin(time.time() * 1.08)) * 25 + 40
    pygame.draw.circle(screen, (193, 64, 72), center, int(pulse), 0)
    pygame.draw.circle(screen, (50, 62, 76, 40), center, int(pulse*1.34), 0)

    # Draw particles
    for p in particles: p.draw(screen)

    # Draw central text (wound)
    txt = font.render("remorse", True, (232, 232, 230))
    screen.blit(txt, (center[0] - txt.get_width() // 2, center[1] - txt.get_height() // 2))

    # Flicker faint phrase
    if random.random() > 0.98:
        phrase = random.choice([
            "echoes", "if only", "again", "silence", "can't return", "fragment", "regret", "echo", "never", "gone", "return"
        ])
        stxt = small.render(phrase, True, (63, 69, 78, 55))
        x = center[0] + random.randint(-220, 220)
        y = center[1] + random.randint(-120, 120)
        screen.blit(stxt, (x, y))

    blackout.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
