import pygame
import math
import random
import time

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Remorse")

# Define colors
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 64)
BLUE = (0, 0, 128)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

# Set up the clock
clock = pygame.time.Clock()

# Define variables
circles = []
max_circles = 100
circle_lifespan = 5  # seconds
regret_factor = 0.01
min_radius = 10
max_radius = 50

class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.start_time = time.time()

    def update(self):
        elapsed_time = time.time() - self.start_time
        self.radius -= regret_factor * elapsed_time

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), int(self.radius))

    def expired(self):
        return self.radius <= 0 or (time.time() - self.start_time) > circle_lifespan

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window
    window.fill(BLACK)

    # Update circles
    for circle in circles:
        circle.update()
        circle.draw(window)

    # Remove expired circles
    circles = [circle for circle in circles if not circle.expired()]

    # Add new circles
    if len(circles) < max_circles:
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(min_radius, max_radius)
        color = random.choice([DARK_BLUE, BLUE, GRAY])
        circle = Circle(x, y, radius, color)
        circles.append(circle)

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()