import pygame
import math
import random
import colorsys
import time
from threading import Thread
import numpy as np

pygame.init()

W, H = 1200, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("")
clock = pygame.time.Clock()

class Spark:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-8, -2)
        self.life = random.uniform(0.8, 1.2)
        self.max_life = self.life
        self.hue = random.uniform(0.05, 0.15)
        
    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += 15 * dt
        self.life -= dt
        
    def draw(self, surf):
        if self.life <= 0: return
        alpha = (self.life / self.max_life) ** 0.3
        sat = 0.9 + 0.1 * (self.life / self.max_life)
        val = 0.8 + 0.2 * (self.life / self.max_life)
        r, g, b = colorsys.hsv_to_rgb(self.hue, sat, val)
        color = (int(r * 255), int(g * 255), int(b * 255))
        
        size = int(3 * alpha + 1)
        if size > 0:
            pygame.draw.circle(surf, color, (int(self.x), int(self.y)), size)

class Wave:
    def __init__(self):
        self.t = 0
        self.amplitude = random.uniform(30, 80)
        self.frequency = random.uniform(0.008, 0.02)
        self.phase = random.uniform(0, math.pi * 2)
        self.y_offset = random.uniform(H * 0.3, H * 0.7)
        self.hue = random.uniform(0.45, 0.65)
        self.birth_time = time.time()
        
    def update(self, dt):
        self.t += dt
        
    def draw(self, surf):
        age = time.time() - self.birth_time
        if age > 8: return
        
        alpha = max(0, 1 - age / 8)
        points = []
        for x in range(0, W + 20, 8):
            y = self.y_offset + self.amplitude * math.sin(self.frequency * x + self.phase + self.t * 2)
            points.append((x, y))
            
        if len(points) > 1:
            r, g, b = colorsys.hsv_to_rgb(self.hue, 0.7, 0.9)
            color = (int(r * 255 * alpha), int(g * 255 * alpha), int(b * 255 * alpha))
            
            try:
                for i in range(len(points) - 1):
                    pygame.draw.line(surf, color, points[i], points[i + 1], 2)
            except:
                pass

class Pulse:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.radius = 0
        self.max_radius = random.uniform(100, 200)
        self.speed = random.uniform(150, 300)
        self.hue = random.uniform(0.8, 1.0)
        self.born = time.time()
        
    def update(self, dt):
        self.radius += self.speed * dt
        
    def draw(self, surf):
        age = time.time() - self.born
        if age > 2 or self.radius > self.max_radius: return
        
        alpha = max(0, 1 - self.radius / self.max_radius) * 0.3
        r, g, b = colorsys.hsv_to_rgb(self.hue, 0.8, 1.0)
        color = (int(r * 255 * alpha), int(g * 255 * alpha), int(b * 255 * alpha))
        
        if alpha > 0.01:
            pygame.draw.circle(surf, color, (int(self.x), int(self.y)), int(self.radius), 2)

sparks = []
waves = []
pulses = []
last_spark = 0
last_wave = 0
last_pulse = 0
mouse_trail = []

def background_thread():
    while True:
        time.sleep(random.uniform(0.1, 0.4))
        if len(waves) < 5:
            waves.append(Wave())
        time.sleep(random.uniform(0.5, 2.0))
        if len(pulses) < 3:
            pulses.append(Pulse(random.randint(100, W-100), random.randint(100, H-100)))

Thread(target=background_thread, daemon=True).start()

running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for _ in range(random.randint(15, 25)):
                sparks.append(Spark(mx + random.uniform(-20, 20), my + random.uniform(-20, 20)))
            pulses.append(Pulse(mx, my))
            waves.append(Wave())
        elif event.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            mouse_trail.append((mx, my, time.time()))
            if len(mouse_trail) > 20:
                mouse_trail.pop(0)
    
    now = time.time()
    if now - last_spark > random.uniform(0.05, 0.15):
        if mouse_trail:
            x, y, _ = random.choice(mouse_trail)
            sparks.append(Spark(x + random.uniform(-30, 30), y + random.uniform(-30, 30)))
        else:
            sparks.append(Spark(random.randint(50, W-50), random.randint(50, H-50)))
        last_spark = now
    
    screen.fill((5, 8, 15))
    
    # Update and draw mouse trail
    current_time = time.time()
    mouse_trail = [(x, y, t) for x, y, t in mouse_trail if current_time - t < 2]
    for i, (x, y, t) in enumerate(mouse_trail):
        age = current_time - t
        alpha = max(0, 1 - age / 2)
        size = int(8 * alpha) + 1
        hue = 0.1 + 0.05 * math.sin(t * 5)
        r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
        color = (int(r * 255 * alpha), int(g * 255 * alpha), int(b * 255 * alpha))
        if size > 0:
            pygame.draw.circle(screen, color, (int(x), int(y)), size)
    
    # Background energy field
    for i in range(0, W, 30):
        for j in range(0, H, 40):
            offset = math.sin(now * 2 + i * 0.01 + j * 0.01) * 0.3
            hue = 0.55 + offset * 0.1
            intensity = 0.1 + 0.05 * math.sin(now * 3 + i * 0.005 + j * 0.007)
            r, g, b = colorsys.hsv_to_rgb(hue, 0.4, intensity)
            color = (int(r * 255), int(g * 255), int(b * 255))
            pygame.draw.circle(screen, color, (i, j), 2)
    
    # Update and draw waves
    waves = [w for w in waves if time.time() - w.birth_time < 8]
    for wave in waves:
        wave.update(dt)
        wave.draw(screen)
    
    # Update and draw pulses
    pulses = [p for p in pulses if time.time() - p.born < 2 and p.radius < p.max_radius]
    for pulse in pulses:
        pulse.update(dt)
        pulse.draw(screen)
    
    # Update and draw sparks
    sparks = [s for s in sparks if s.life > 0]
    for spark in sparks:
        spark.update(dt)
        spark.draw(screen)
    
    # Central energy core
    core_x, core_y = W // 2, H // 2
    core_radius = 20 + 15 * math.sin(now * 4)
    for r in range(int(core_radius), 0, -3):
        alpha = (core_radius - r) / core_radius
        hue = 0.05 + 0.05 * math.sin(now * 6)
        color_r, color_g, color_b = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
        color = (int(color_r * 255 * alpha), int(color_g * 255 * alpha), int(color_b * 255 * alpha))
        pygame.draw.circle(screen, color, (core_x, core_y), r)
    
    pygame.display.flip()

pygame.quit()