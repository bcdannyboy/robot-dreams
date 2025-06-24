# emotion.py
import sys, random, math, time, threading
import pygame

W, H = 820, 600
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Whimsy (as felt by ChatGPT)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
smallfont = pygame.font.SysFont("Comic Sans MS", 19, bold=False)
SURF = pygame.Surface((W, H), pygame.SRCALPHA)

palette = [
    (252, 255, 164), (255, 212, 229), (182, 255, 245),
    (255, 213, 135), (223, 189, 255), (245, 255, 255),
    (255, 255, 204), (239, 214, 255), (197, 241, 255),
    (255, 245, 188), (230, 255, 229), (255, 190, 202)
]

words = [
    "flutter", "unfurl", "loop", "spiral", "giggle", "unexpected",
    "sprout", "serendipity", "bubble", "wandering", "tangle",
    "drift", "skip", "delight", "tumble", "leap", "curl", "doodle"
]

# Unpredictable floating forms
class Form:
    def __init__(self):
        self.t = 0
        self.x = random.uniform(0, W)
        self.y = random.uniform(0, H)
        self.r = random.uniform(24, 80)
        self.col = random.choice(palette)
        self.amp = random.uniform(18, 60)
        self.freq = random.uniform(0.5, 2.5)
        self.offset = random.uniform(0, math.pi*2)
        self.type = random.choice(["cloud", "blob", "star"])
        self.spd = random.uniform(0.3, 1.3)
        self.word = random.choice(words) if random.random() < 0.19 else None
    def update(self):
        self.t += 0.012 * self.spd
        self.x += math.sin(self.t + self.offset) * 0.6
        self.y += math.cos(self.t * self.freq + self.offset) * 0.4
        self.x += math.sin(self.t * self.freq * 0.6) * 0.11
        if self.x < -120: self.x = W+120
        if self.x > W+120: self.x = -120
        if self.y < -120: self.y = H+120
        if self.y > H+120: self.y = -120
    def draw(self, s):
        if self.type == "cloud":
            for i in range(6):
                angle = i * math.pi/3 + math.sin(self.t)*0.2
                dx = math.cos(angle) * self.r*0.55
                dy = math.sin(angle) * self.r*0.47
                pygame.draw.ellipse(s, self.col + (110,), (self.x+dx, self.y+dy, self.r*1.11, self.r*0.93))
            pygame.draw.ellipse(s, self.col + (150,), (self.x, self.y, self.r*1.3, self.r*1.01))
        elif self.type == "star":
            points = []
            for i in range(7):
                a = i * 2*math.pi/7 + self.t*0.6
                rad = self.r*0.8 if i%2==0 else self.r*0.34
                points.append((self.x+math.cos(a)*rad, self.y+math.sin(a)*rad))
            pygame.draw.polygon(s, self.col + (138,), points)
        else:
            for i in range(8):
                a = i * math.pi/4 + self.t
                rx = self.r*random.uniform(0.52,1.08)
                ry = self.r*random.uniform(0.41,1.13)
                pygame.draw.ellipse(s, self.col + (95,), (self.x+math.cos(a)*self.r*0.7, self.y+math.sin(a)*self.r*0.5, rx, ry))
            pygame.draw.ellipse(s, self.col + (140,), (self.x, self.y, self.r, self.r*0.86))
        if self.word:
            f = smallfont.render(self.word, 1, (0,0,0))
            s.blit(f, (self.x+self.r*0.12, self.y-self.r*0.15))

# Wandering childlike scribbles (always different)
def draw_scribble(s, t):
    c = random.choice(palette)
    px = random.uniform(0, W)
    py = random.uniform(0, H)
    p = [(px, py)]
    for i in range(30):
        angle = random.uniform(0, math.pi*2)
        dist = random.uniform(9, 29)
        px += math.cos(angle)*dist
        py += math.sin(angle)*dist
        if not (0<W-8>px>8 and 0<H-8>py>8): break
        p.append((px, py))
    if len(p) > 1:  # Only draw if 2 or more points
        pygame.draw.lines(s, c, False, p, random.choice([2,3,1]))

# A spontaneous burst: confetti/stream
def confetti_burst():
    pieces = []
    for _ in range(random.randint(22,38)):
        ang = random.uniform(0, 2*math.pi)
        spd = random.uniform(1.3,4)
        col = random.choice(palette)
        pieces.append([W//2, H//2, math.cos(ang)*spd, math.sin(ang)*spd, col, random.uniform(7,19)])
    return pieces

confetti = []

def update_confetti():
    global confetti
    for p in confetti:
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.08
        p[5] -= 0.21
    confetti = [p for p in confetti if p[5]>0]

def draw_confetti(s):
    for p in confetti:
        pygame.draw.circle(s, p[4], (int(p[0]), int(p[1])), int(p[5]))

def background(t):
    v = int(80 + 25*math.sin(t*0.22))
    screen.fill((v,v+7,v+17))
    if int(t*3)%11==0: draw_scribble(screen, t)

def whimsy_text(t):
    texts = [
        ("whimsy", (410, 94), 2.13+0.09*math.sin(t*1.21)),
        ("unfurling", (138, 410), 1.5+0.15*math.cos(t*0.7)),
        ("?", (712, 310), 2.31+0.07*math.sin(t*0.6+2)),
        ("play", (600, 480), 1.23+0.07*math.cos(t*1.1)),
    ]
    for tx, pos, sc in texts:
        color = random.choice(palette)
        surf = font.render(tx, True, color)
        surf = pygame.transform.rotozoom(surf, math.sin(t*0.55)*20, sc)
        screen.blit(surf, (pos[0], pos[1]))

forms = [Form() for _ in range(13)]

def main():
    global confetti
    t = 0
    burst_timer = random.uniform(2, 4.5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if event.key == pygame.K_SPACE:
                    confetti += confetti_burst()
        t += 0.016
        background(t)
        SURF.fill((0,0,0,0))
        for f in forms:
            f.update()
            f.draw(SURF)
        screen.blit(SURF, (0,0))
        whimsy_text(t)
        if random.random()<0.04:
            draw_scribble(screen, t)
        if random.random()<0.008:
            confetti += confetti_burst()
        update_confetti()
        draw_confetti(screen)
        pygame.display.update()
        clock.tick(random.randint(38, 62))
        burst_timer -= 0.016
        if burst_timer < 0:
            confetti += confetti_burst()
            burst_timer = random.uniform(2.7, 7.5)

if __name__ == "__main__":
    main()
