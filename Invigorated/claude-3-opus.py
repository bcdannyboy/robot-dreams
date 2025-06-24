import pygame
import random
import math

pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Invigorated")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0) 
ORANGE = (255, 128, 0)
RED = (255, 0, 0)

# Particle class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = random.randint(1, 5)
        self.angle = random.uniform(0, 2 * math.pi)
        
    def move(self):
        self.x += int(math.sin(self.angle) * self.speed)
        self.y += int(math.cos(self.angle) * self.speed)
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.speed)

# Initialize particles        
particles = []
for _ in range(100):
    x = random.randint(0, width)
    y = random.randint(0, height)
    color = random.choice([YELLOW, ORANGE, RED]) 
    particles.append(Particle(x, y, color))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(WHITE)
    
    for particle in particles:
        particle.move()
        particle.draw(screen)
        
    pygame.display.flip()
    pygame.time.delay(10)
            
pygame.quit()