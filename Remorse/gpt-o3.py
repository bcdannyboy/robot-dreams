# emotion.py
import pygame, sys, math, random, time

# ----------- birth ----------- #
pygame.init()
SIZE = WIDTH, HEIGHT = 888, 555
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("remorse")
clock = pygame.time.Clock()
start = time.time()

# persistent memories
splinters = []
void = pygame.Surface(SIZE, pygame.SRCALPHA)

# ----------- loop ----------- #
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    t = time.time() - start
    # core pulse
    pulse = 42 + 38 * math.sin(t * 1.3)

    # slow bleed-through
    void.fill((0, 0, 0, 3))
    screen.blit(void, (0, 0))

    # birth of a new shard
    if random.random() < 0.02:
        ang = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, min(WIDTH, HEIGHT) // 2.2)
        x = WIDTH // 2 + math.cos(ang) * dist
        y = HEIGHT // 2 + math.sin(ang) * dist
        splinters.append([x, y, 255])

    # decay & draw splinters
    for s in splinters[:]:
        s[2] -= 1.1
        if s[2] <= 0:
            splinters.remove(s)
            continue
        pygame.draw.circle(screen, (120, 25, 25, s[2]), (int(s[0]), int(s[1])), 3)

    # heart of remorse
    pygame.draw.circle(screen, (230, 230, 230), (WIDTH // 2, HEIGHT // 2), int(abs(pulse)), 0)

    # sporadic surge
    if int(t * 2) % 33 == 0 and (t % 7) < 0.08:
        screen.fill((150, 0, 0), special_flags=pygame.BLEND_RGB_ADD)

    pygame.display.flip()
    clock.tick(60)
