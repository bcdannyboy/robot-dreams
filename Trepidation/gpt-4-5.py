import pygame
import random
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(" ")

clock = pygame.time.Clock()

def flicker():
    if random.random() > 0.9:
        return random.randint(-10, 10)
    return 0

def spiral_surface(time):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    cx, cy = width // 2, height // 2
    points = []
    for i in range(400):
        angle = i * 0.1 + time
        radius = i * 0.6
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius
        points.append((x + flicker(), y + flicker()))
    if points:
        pygame.draw.lines(surface, (255, random.randint(0, 40), random.randint(0, 40), 50), False, points, 4)
    return surface

def noise_overlay():
    noise = pygame.Surface((width, height), pygame.SRCALPHA)
    for _ in range(3000):
        x, y = random.randint(0, width), random.randint(0, height)
        alpha = random.randint(0, 40)
        noise.set_at((x, y), (255, 255, 255, alpha))
    return noise

running = True
time = 0

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    spiral = spiral_surface(time)
    noise = noise_overlay()

    screen.blit(spiral, (0, 0))
    screen.blit(noise, (0, 0))

    pygame.display.flip()
    clock.tick(60)
    time += 0.02

pygame.quit()
