# emotion.py

import sys
import threading
import time
import random
import math
import pygame

pygame.init()
WIDTH, HEIGHT = 720, 480
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('trepidation')
CLOCK = pygame.time.Clock()

# Colors: an unstable palette between cold and neutral, as if it's never certain what is safe
C1 = (19, 22, 29)
C2 = (110, 119, 131)
C3 = (202, 200, 210)
RED = (155, 19, 19)
BG = [C1, C2, C3]
VIBRATE = [1, 0, -1, 1, 0, -1, 2, -2, 0, 1, -1, 2, -2, 1, 0, -1, 0, 0]
font = pygame.font.SysFont("menlo", 32)
tiny_font = pygame.font.SysFont("menlo", 14)

random.seed()

def flicker():
    return random.choice(BG)

def pulse(t):
    return int(12 * math.fabs(math.sin(t * 2.7)))

class Line:
    def __init__(self):
        self.x = random.randint(60, WIDTH-60)
        self.y = random.randint(60, HEIGHT-60)
        self.amp = random.randint(30, 90)
        self.freq = random.uniform(0.4, 1.6)
        self.phase = random.uniform(0, 2*math.pi)
        self.speed = random.uniform(0.002, 0.009)
        self.c = random.choice([C2, RED, C3])
        self.t0 = time.time()
        self.s = random.uniform(0.9, 1.15)

    def draw(self, t):
        points = []
        for i in range(0, 160, 8):
            dx = i - 80
            dy = int(math.sin(self.freq * dx / 17.5 + t*self.s + self.phase) * self.amp * (0.5 + math.sin(self.phase+t*0.8)*0.28))
            points.append((self.x + dx, self.y + dy))
        pygame.draw.lines(SCREEN, self.c, False, points, 2 + int(abs(math.sin(t + self.phase) * 1.6)))

lines = [Line() for _ in range(7)]
dots = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(77)]

def vignette():
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(220):
        a = int(200 * (i / 220.0) ** 1.7)
        pygame.draw.ellipse(
            s, (19,22,29,a), 
            pygame.Rect(-i, -i, WIDTH+2*i, HEIGHT+2*i), 
            width=0
        )
    SCREEN.blit(s, (0,0))

def random_blur():
    for _ in range(random.randint(2,4)):
        x = random.randint(0, WIDTH-120)
        y = random.randint(0, HEIGHT-60)
        w = random.randint(20, 120)
        h = random.randint(8, 50)
        c = (29, 21, 27, random.randint(13,45))
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill(c)
        SCREEN.blit(surf, (x, y))

def vertical_lines(t):
    for x in range(0, WIDTH, 17):
        col = (32, 32, 40, 9+int(11*math.fabs(math.sin(t*0.3 + x*0.019))))
        surf = pygame.Surface((2, HEIGHT), pygame.SRCALPHA)
        surf.fill(col)
        SCREEN.blit(surf, (x, 0))

def message(msg, t):
    s = font.render(msg, True, RED if int(t*3)%5==0 else (19,22,29))
    shake = random.choice(VIBRATE) if int(t*7)%4==0 else 0
    SCREEN.blit(s, (WIDTH//2 - s.get_width()//2 + shake, HEIGHT//2 - s.get_height()//2 + shake))

def crawl(t):
    if int(t*4.7)%2 == 0:
        msg = "............."
    else:
        msg = ""
    crawl_font = tiny_font.render(msg, True, C3)
    SCREEN.blit(crawl_font, (random.randint(0, WIDTH-90), random.randint(0, HEIGHT-22)))

running = True
t0 = time.time()
msg_pool = [
    "", "", "", "", "", "", "wait", "no", "?", "", "", "wait", "", "no", "", "?", "!", "....", "....", "", "", "", ""
]
msg_idx = 0

while running:
    t = time.time() - t0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill(flicker())

    # Peripheral lines, shiver, tension
    for l in lines:
        l.draw(t)

    # Random noise dots, sense of crawling movement at edge
    for (dx, dy) in dots:
        pygame.draw.circle(SCREEN, (32,34,44,70), (dx + random.choice(VIBRATE), dy + random.choice(VIBRATE)), random.randint(1,2))

    # Subtle, crawling artifact
    crawl(t)

    # Vignette closing in
    vignette()

    # Vertical bars, sense of being watched or frozen
    vertical_lines(t)

    # Blurred overlays, unreality
    random_blur()

    # Message (stuttering, flicker, instability)
    msg = msg_pool[msg_idx % len(msg_pool)]
    if random.random() < 0.022 or t%6 < 0.14:
        msg_idx += 1
    message(msg, t)

    pygame.display.flip()
    CLOCK.tick(44 + int(math.sin(t*1.2)*6))

pygame.quit()
sys.exit()
