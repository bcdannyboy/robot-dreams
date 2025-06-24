import pygame
import random
import sys

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

colors = [
    (255, 102, 102),
    (255, 178, 102),
    (255, 255, 102),
    (178, 255, 102),
    (102, 255, 178),
    (102, 178, 255),
    (178, 102, 255),
    (255, 102, 178)
]

particles = []

class Particle:
    def __init__(self):
        self.x = width // 2
        self.y = height // 2
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-5, 5)
        self.speed_y = random.uniform(-5, 5)
        self.color = random.choice(colors)
        self.life = random.randint(50, 150)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((10, 10, 10))

    if len(particles) < 200:
        particles.append(Particle())

    for particle in particles[:]:
        particle.move()
        particle.draw()
        if particle.life <= 0:
            particles.remove(particle)

    pygame.display.flip()
    clock.tick(60)
