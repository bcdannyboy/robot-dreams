import sys
import threading
import time
import math
import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Invigorated")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Particle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = random.randint(2, 6)
        self.color = [random.randint(128, 255) for _ in range(3)]
        self.speed = random.uniform(2, 6)
        self.angle = random.uniform(0, 2 * math.pi)
        self.life = random.uniform(2.5, 6.5)
        self.birth = time.time()
        self.offset = random.random() * 10

    def update(self):
        elapsed = time.time() - self.birth
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.radius = max(0.1, self.radius - 0.05)
        return elapsed < self.life

    def draw(self, surface):
        pulsate = abs(math.sin((time.time() - self.birth) * 5 + self.offset)) * 255
        color = tuple(min(255, int(c + pulsate / 3)) for c in self.color)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.radius))

particles = []

def energy_wave():
    frequency = 0.5
    amplitude = 100
    phase = 0
    color = [random.randint(150, 255) for _ in range(3)]
    while True:
        phase += 0.05
        for i in range(WIDTH):
            y = int(HEIGHT/2 + math.sin(i * frequency * 0.01 + phase) * amplitude)
            screen.set_at((i, y), color)
        time.sleep(0.01)

wave_thread = threading.Thread(target=energy_wave, daemon=True)
wave_thread.start()

invigorated_font = pygame.font.SysFont("arial", 64, bold=True)
sub_font = pygame.font.SysFont("arial", 24, italic=True)

def draw_text():
    t = time.time()
    text_color = (int(255 * abs(math.sin(t * 1.5))),
                  int(255 * abs(math.cos(t * 1.7))),
                  int(255 * abs(math.sin(t * 2.3))))
    text = invigorated_font.render("Invigorated", True, text_color)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 50))
    subtext = sub_font.render("↯ pulsing with chaos & potential ↯", True, WHITE)
    screen.blit(subtext, (WIDTH//2 - subtext.get_width()//2, HEIGHT - 80))

running = True
while running:
    screen.fill(BLACK)
    draw_text()

    if random.random() < 0.5:
        particles.append(Particle())

    for p in particles[:]:
        if not p.update():
            particles.remove(p)
        else:
            p.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
