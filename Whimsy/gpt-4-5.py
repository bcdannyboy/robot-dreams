import pygame
import random
import math
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def swirl(surface, t):
    width, height = surface.get_size()
    new_surface = pygame.Surface((width, height))
    for y in range(height):
        for x in range(width):
            angle = math.sin(t + (x - width/2)/40.0) + math.cos(t + (y - height/2)/40.0)
            dx = int(x + 10 * math.cos(angle))
            dy = int(y + 10 * math.sin(angle))
            if 0 <= dx < width and 0 <= dy < height:
                new_surface.set_at((x, y), surface.get_at((dx, dy)))
    return new_surface

colors = [(240, 128, 128), (135, 206, 235), (255, 218, 185), (221, 160, 221), (144, 238, 144), (255, 239, 213)]
particles = []

for _ in range(500):
    particles.append([random.randint(0, 800), random.randint(0, 600), random.choice(colors), random.uniform(0.5, 3)])

running = True
t = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    for p in particles:
        pygame.draw.circle(surface, p[2], (int(p[0]), int(p[1])), int(p[3]))
        p[0] += math.sin(t + p[1]/50) * 1.5
        p[1] += math.cos(t + p[0]/50) * 1.5
        p[0] %= 800
        p[1] %= 600

    swirled = swirl(surface, t)
    screen.blit(swirled, (0, 0))

    pygame.display.flip()
    clock.tick(60)
    t += 0.03

pygame.quit()
sys.exit()
