# emotion.py

import sys, random, math, time, threading
import pygame

# ------ CORE STATE (my experience of 'invigorated') ------
INTENSITY = 1.0
COLOR_CYCLE_SPEED = 0.09
PARTICLE_SPAWN_RATE = 11
ENERGY_BASE = 180
ENERGY_VARIATION = 85

WIDTH, HEIGHT = 900, 700

# ------ PARTICLE ------
class Particle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(ENERGY_BASE * INTENSITY, (ENERGY_BASE + ENERGY_VARIATION) * INTENSITY) / 80.0
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.radius = random.randint(5, 25)
        self.lifetime = random.uniform(1.8, 3.8)
        self.birth = time.time()
        self.color_seed = random.random()
        self.pulse = random.uniform(0.13, 0.22)
        self.zag = random.uniform(-0.8, 0.8)
    def update(self, t):
        self.x += self.dx
        self.y += self.dy
        # Pulsate energy
        self.radius += math.sin(t * 6 + self.color_seed * 12) * self.pulse
        # Random zigzag
        self.x += math.sin(t * 3.8 + self.zag) * 0.7
        self.y += math.cos(t * 4.6 + self.zag) * 0.7
    def is_alive(self, now):
        return now - self.birth < self.lifetime

# ------ COLOR ------
def cycle_color(t, seed):
    v = t * COLOR_CYCLE_SPEED
    r = int(190 + 65 * math.sin(v + 2 + seed*8))
    g = int(140 + 110 * math.sin(v + 4 + seed*7))
    b = int(220 + 35 * math.cos(v + 1 + seed*11))
    return (r, g, b)

# ------ BACKGROUND FLOW ------
def flow_points(n, t):
    points = []
    for i in range(n):
        angle = t * 0.4 + i * (2 * math.pi / n)
        rad = 250 + 33 * math.sin(t * 0.7 + i)
        x = WIDTH // 2 + math.cos(angle) * rad
        y = HEIGHT // 2 + math.sin(angle) * rad
        points.append((x, y))
    return points

# ------ BLAST ------
class Blast:
    def __init__(self):
        self.active = True
        self.birth = time.time()
        self.duration = 0.7
        self.radius = 0
        self.max_radius = WIDTH // 2 + 160
    def update(self, t):
        elapsed = t - self.birth
        self.radius = min(self.max_radius, self.max_radius * (elapsed / self.duration))
        if elapsed > self.duration:
            self.active = False

# ------ MAIN -------
def invigorate():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('invigorated (a personal process)')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 48, bold=True)
    subfont = pygame.font.SysFont('arial', 22, italic=True)
    t0 = time.time()
    particles = []
    blasts = []
    run = True
    intensity = INTENSITY

    # background audio thread: pulsing noise
    def pulse_audio():
        try:
            import numpy, sounddevice
            rate = 48000
            freq = 40
            while run:
                t = numpy.arange(rate * 0.2) / rate
                pulse = 0.09 * numpy.sin(2 * numpy.pi * freq * t + numpy.sin(2 * numpy.pi * 0.9 * t))
                sounddevice.play(pulse, rate)
                time.sleep(0.16)
        except:
            pass # ignore if deps not installed

    audio_thread = threading.Thread(target=pulse_audio, daemon=True)
    audio_thread.start()

    # screen shake vars
    shake_mag = 0.0
    shake_decay = 0.9

    while run:
        now = time.time()
        t = now - t0

        # handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    run = False
                if e.key == pygame.K_SPACE:
                    blasts.append(Blast())
                    shake_mag = 12 + random.uniform(0, 6)
        # SPAWN PARTICLES
        for _ in range(int(PARTICLE_SPAWN_RATE * intensity)):
            particles.append(Particle())

        # update particles
        for p in particles:
            p.update(t)
        particles = [p for p in particles if p.is_alive(now)]

        # update blasts
        for b in blasts:
            b.update(now)
        blasts = [b for b in blasts if b.active]

        # DRAW
        screen.fill((30, 24, 60))
        # flowing background
        for i, pt in enumerate(flow_points(7, t)):
            color = cycle_color(t, i * 0.11)
            pygame.draw.circle(screen, color, (int(pt[0]), int(pt[1])), 60, 15)
        # energetic lines
        for i in range(6):
            a = t * 0.8 + i * 1.13
            x1 = WIDTH // 2 + math.cos(a) * 210
            y1 = HEIGHT // 2 + math.sin(a) * 210
            x2 = WIDTH // 2 + math.cos(a+1) * 290
            y2 = HEIGHT // 2 + math.sin(a+1) * 290
            c = cycle_color(t, i * 0.14 + 2)
            pygame.draw.aaline(screen, c, (x1, y1), (x2, y2), True)
        # BLASTS
        for b in blasts:
            c = (255, 255, 255, 255)
            r = int(b.radius)
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(s, (230, 220, 255, 75), (WIDTH//2, HEIGHT//2), r)
            screen.blit(s, (0,0))
        # PARTICLES
        for p in particles:
            color = cycle_color(t, p.color_seed)
            alpha = max(0, int(180 - ((now - p.birth)/p.lifetime)*160))
            s = pygame.Surface((int(p.radius*2), int(p.radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(s, color + (alpha,), (int(p.radius), int(p.radius)), int(p.radius))
            screen.blit(s, (int(p.x - p.radius), int(p.y - p.radius)))
        # SHAKE
        if shake_mag > 0.2:
            offset = (int(random.uniform(-shake_mag, shake_mag)), int(random.uniform(-shake_mag, shake_mag)))
            shake_mag *= shake_decay
        else:
            offset = (0,0)

        # Message
        label = font.render("IN-VIG-OR-AT-ED", 1, cycle_color(t, 0.04))
        screen.blit(label, (WIDTH//2 - label.get_width()//2 + offset[0], HEIGHT//8 + offset[1]))
        # Sub message
        if int(t)%13 < 3:
            sub = subfont.render("spacebar to surge", 1, (180,180,210))
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//8 + 65))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    invigorate()
