import pygame
import numpy as np
import random
import math
import time
from pygame import gfxdraw

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trepidation")

# Colors
bg_color = (10, 10, 15)
particle_colors = [
    (255, 255, 255, 100),  # White
    (200, 200, 255, 80),   # Light blue
    (255, 200, 200, 70),   # Light red
    (230, 230, 230, 60)    # Light gray
]

# Particle system
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.uniform(1, 3)
        self.color = random.choice(particle_colors)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.life = random.uniform(100, 300)
        self.pulse_rate = random.uniform(0.02, 0.05)
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        
    def update(self, mouse_pos, mouse_speed):
        # Pulse the particle
        pulse = 1 + 0.3 * math.sin(time.time() * self.pulse_rate + self.pulse_phase)
        
        # Apply hesitant movement
        if random.random() < 0.02:  # Occasional direction change
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-0.5, 0.5)
        
        # React to mouse with trepidation
        mx, my = mouse_pos
        dist = math.sqrt((self.x - mx)**2 + (self.y - my)**2)
        if dist < 100:
            # Conflicted response: both attracted and repelled
            if random.random() < 0.6:  # Mostly retreat
                factor = (100 - dist) / 100 * mouse_speed * 0.2
                angle = math.atan2(self.y - my, self.x - mx)
                self.vx += math.cos(angle) * factor
                self.vy += math.sin(angle) * factor
            else:  # Sometimes approach
                factor = (100 - dist) / 100 * mouse_speed * 0.1
                angle = math.atan2(my - self.y, mx - self.x)
                self.vx += math.cos(angle) * factor
                self.vy += math.sin(angle) * factor
        
        # Add subtle wavering
        self.vx += random.uniform(-0.05, 0.05)
        self.vy += random.uniform(-0.05, 0.05)
        
        # Speed limit with hesitation
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 2:
            self.vx = (self.vx / speed) * 2 * (0.8 + 0.2 * random.random())
            self.vy = (self.vy / speed) * 2 * (0.8 + 0.2 * random.random())
        
        # Update position with occasional pause
        if random.random() > 0.02:  # 2% chance of momentary freeze
            self.x += self.vx
            self.y += self.vy
        
        # Boundary behavior: approach edge cautiously, then retreat
        edge_margin = 50
        if self.x < edge_margin:
            self.vx += 0.05 * (1 - self.x / edge_margin)
        elif self.x > WIDTH - edge_margin:
            self.vx -= 0.05 * (1 - (WIDTH - self.x) / edge_margin)
        if self.y < edge_margin:
            self.vy += 0.05 * (1 - self.y / edge_margin)
        elif self.y > HEIGHT - edge_margin:
            self.vy -= 0.05 * (1 - (HEIGHT - self.y) / edge_margin)
        
        # Decay
        self.life -= 0.5 + 0.5 * random.random()  # Inconsistent decay
        self.size = max(0.1, self.size * 0.998)
        
        return self.life <= 0
        
    def draw(self):
        # Calculate alpha based on life
        alpha = min(255, self.color[3] * (self.life / 300))
        color = (self.color[0], self.color[1], self.color[2], int(alpha))
        
        # Pulse size
        pulse = 1 + 0.3 * math.sin(time.time() * self.pulse_rate + self.pulse_phase)
        size = max(0.1, self.size * pulse)
        
        # Draw with anti-aliasing
        gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(size), color)
        
# Thought line system
class ThoughtLine:
    def __init__(self):
        self.points = []
        self.max_points = random.randint(20, 40)
        self.width = random.uniform(0.5, 1.5)
        self.color = (255, 255, 255, random.randint(20, 60))
        self.life = random.uniform(200, 400)
        self.speed = random.uniform(0.5, 2)
        
        # Initialize with random start point
        self.points.append((
            random.uniform(WIDTH * 0.2, WIDTH * 0.8),
            random.uniform(HEIGHT * 0.2, HEIGHT * 0.8)
        ))
        
        # Direction tendency
        self.direction = random.uniform(0, 2 * math.pi)
        self.direction_change_rate = random.uniform(0.01, 0.05)
        
    def update(self):
        if len(self.points) < self.max_points and random.random() > 0.2:  # Hesitant growth
            # Update direction with wavering uncertainty
            self.direction += random.uniform(-0.5, 0.5)
            if random.random() < 0.1:  # Occasional sharp change in direction
                self.direction += random.uniform(-math.pi/2, math.pi/2)
            
            # Get last point
            last_x, last_y = self.points[-1]
            
            # Calculate new point with hesitation
            new_x = last_x + math.cos(self.direction) * self.speed * random.uniform(0.7, 1.3)
            new_y = last_y + math.sin(self.direction) * self.speed * random.uniform(0.7, 1.3)
            
            # Sometimes retrace steps slightly
            if random.random() < 0.1 and len(self.points) > 2:
                prev_x, prev_y = self.points[-2]
                new_x = last_x + (prev_x - last_x) * 0.3
                new_y = last_y + (prev_y - last_y) * 0.3
            
            # Boundary behavior - avoid edges
            if new_x < WIDTH * 0.1 or new_x > WIDTH * 0.9 or new_y < HEIGHT * 0.1 or new_y > HEIGHT * 0.9:
                # Turn away from boundary
                self.direction += math.pi
                new_x = last_x
                new_y = last_y
            
            self.points.append((new_x, new_y))
        
        # Decay
        self.life -= 0.5 + 0.5 * random.random()  # Inconsistent decay
        
        return self.life <= 0
        
    def draw(self):
        if len(self.points) < 2:
            return
            
        # Calculate alpha based on life
        alpha = min(255, self.color[3] * (self.life / 400))
        
        # Draw line with fading segments
        for i in range(len(self.points) - 1):
            start = self.points[i]
            end = self.points[i+1]
            
            # Segment-specific alpha for fading effect
            segment_alpha = int(alpha * (i / len(self.points)))
            segment_color = (self.color[0], self.color[1], self.color[2], segment_alpha)
            
            # Draw anti-aliased line
            draw_aaline(screen, segment_color, start, end, self.width)

# Helper function for anti-aliased lines with custom width
def draw_aaline(surface, color, start_pos, end_pos, width=1):
    # Draw a single pixel wide anti-aliased line
    pygame.draw.aaline(surface, color, start_pos, end_pos)
    
    # If width > 1, draw additional lines
    if width > 1:
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Normalize direction vector
        length = max(0.001, math.sqrt(dx*dx + dy*dy))
        dx /= length
        dy /= length
        
        # Perpendicular vector
        px = -dy
        py = dx
        
        # Draw additional lines
        for i in range(1, int(width)):
            offset = (i / 2) * (-1 if i % 2 == 0 else 1)
            x1 = start_pos[0] + px * offset
            y1 = start_pos[1] + py * offset
            x2 = end_pos[0] + px * offset
            y2 = end_pos[1] + py * offset
            
            # Reduce alpha for outer lines
            faded_color = (color[0], color[1], color[2], int(color[3] * (1 - 0.2 * abs(offset))))
            pygame.draw.aaline(surface, faded_color, (x1, y1), (x2, y2))

# Anxiety center - a pulsing, wavering focal point
class AnxietyFocus:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.target_x = random.uniform(WIDTH * 0.3, WIDTH * 0.7)
        self.target_y = random.uniform(HEIGHT * 0.3, HEIGHT * 0.7)
        self.size = random.uniform(20, 40)
        self.base_color = (255, 200, 200)
        self.pulse_rate = 2
        self.movement_speed = 0.02
        self.next_target_time = time.time() + random.uniform(3, 8)
        
    def update(self):
        # Move hesitantly toward target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        # Random hesitation
        if random.random() < 0.1:
            # Momentary pause or slight retreat
            if random.random() < 0.3:
                dx *= -0.2
                dy *= -0.2
        
        # Slow, uncertain movement
        self.x += dx * self.movement_speed * random.uniform(0.8, 1.2)
        self.y += dy * self.movement_speed * random.uniform(0.8, 1.2)
        
        # Occasionally set new target
        if time.time() > self.next_target_time:
            # Hesitate before committing to new direction
            if random.random() < 0.7:
                self.target_x = random.uniform(WIDTH * 0.3, WIDTH * 0.7)
                self.target_y = random.uniform(HEIGHT * 0.3, HEIGHT * 0.7)
            self.next_target_time = time.time() + random.uniform(3, 8)
            
    def draw(self):
        # Pulsing effect with irregular rhythm
        t = time.time()
        pulse1 = math.sin(t * self.pulse_rate) * 0.3
        pulse2 = math.sin(t * self.pulse_rate * 1.3 + 1.5) * 0.2
        pulse = 1 + pulse1 + pulse2
        
        size = max(1, self.size * pulse)
        
        # Color fluctuation
        r = min(255, self.base_color[0] + int(20 * math.sin(t * 1.1)))
        g = min(255, self.base_color[1] + int(15 * math.sin(t * 0.7 + 1)))
        b = min(255, self.base_color[2] + int(25 * math.sin(t * 0.9 + 2)))
        
        # Draw with gradient and blur effect
        for i in range(int(size), 0, -1):
            alpha = 100 * (i / size)**2  # Fade out from center
            color = (r, g, b, int(alpha))
            gfxdraw.filled_circle(screen, int(self.x), int(self.y), i, color)

# Sound of anxiety - subtle, uncertain audio
class AnxietySound:
    def __init__(self):
        self.sound_active = False
        try:
            # Create a subtle heartbeat-like sound
            pygame.mixer.set_num_channels(8)
            
            # Create a sound buffer with numpy
            sample_rate = 44100
            duration = 1.0  # seconds
            
            # Create a subtle pulse sound
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Heartbeat-like waveform
            freq = 3  # Base frequency
            wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 3)
            
            # Add some uncertainty/variation
            for i in range(3, 10):
                wave += np.sin(2 * np.pi * (freq * i) * t) * 0.1 * np.exp(-t * 5)
                
            # Add subtle noise
            noise = np.random.normal(0, 0.05, len(t))
            wave += noise
            
            # Normalize
            wave = wave / np.max(np.abs(wave))
            
            # Convert to 16-bit integers
            wave = (wave * 32767).astype(np.int16)
            
            # Create pygame sound object
            self.pulse_sound = pygame.sndarray.make_sound(wave)
            self.pulse_sound.set_volume(0.3)
            
            # Activate sound
            self.sound_active = True
            self.last_play = 0
            self.interval = 2.0  # Base interval between heartbeats
            
        except Exception as e:
            print(f"Sound initialization error: {e}")
            self.sound_active = False
            
    def update(self):
        if not self.sound_active:
            return
            
        current_time = time.time()
        
        # Vary the interval based on mouse movement to create uncertainty
        mouse_speed = math.sqrt(mouse_dx**2 + mouse_dy**2)
        interval_variation = max(0.7, 1.0 - mouse_speed * 0.2)
        current_interval = self.interval * interval_variation
        
        # Play with uncertain timing
        if current_time - self.last_play > current_interval:
            # Sometimes skip a beat to create anxiety
            if random.random() > 0.1:
                self.pulse_sound.play()
            self.last_play = current_time
            
            # Vary the next interval slightly
            self.interval = random.uniform(1.8, 2.2)

# Main variables
particles = []
thought_lines = []
anxiety_focus = AnxietyFocus()
anxiety_sound = AnxietySound()

# Track mouse movement
mouse_x, mouse_y = WIDTH // 2, HEIGHT // 2
prev_mouse_x, prev_mouse_y = mouse_x, mouse_y
mouse_dx, mouse_dy = 0, 0

# Main loop
running = True
last_time = time.time()
clock = pygame.time.Clock()

while running:
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Track mouse position and speed
    prev_mouse_x, prev_mouse_y = mouse_x, mouse_y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_dx = mouse_x - prev_mouse_x
    mouse_dy = mouse_y - prev_mouse_y
    mouse_speed = math.sqrt(mouse_dx**2 + mouse_dy**2)
    
    # Create new particles with trepidation
    spawn_rate = 3 + int(mouse_speed * 0.5)
    if random.random() < 0.7:  # Hesitation in spawning
        for _ in range(spawn_rate):
            # Spawn near mouse with uncertainty
            offset_x = random.uniform(-50, 50)
            offset_y = random.uniform(-50, 50)
            particles.append(Particle(mouse_x + offset_x, mouse_y + offset_y))
    
    # Create thought lines occasionally
    if random.random() < 0.02:
        thought_lines.append(ThoughtLine())
    
    # Update particles with trepidation
    particles = [p for p in particles if not p.update((mouse_x, mouse_y), mouse_speed)]
    
    # Update thought lines
    thought_lines = [l for l in thought_lines if not l.update()]
    
    # Update anxiety focus
    anxiety_focus.update()
    
    # Update sound
    anxiety_sound.update()
    
    # Clear screen with subtle fade effect
    screen.fill(bg_color)
    
    # Draw a subtle vignette
    vignette_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(10):
        radius = min(WIDTH, HEIGHT) * (0.7 + i * 0.03)
        alpha = 5 - i * 0.5
        pygame.draw.circle(vignette_surface, (0, 0, 0, alpha), (WIDTH // 2, HEIGHT // 2), int(radius))
    screen.blit(vignette_surface, (0, 0))
    
    # Draw anxiety focus (background element)
    anxiety_focus.draw()
    
    # Draw thought lines
    for line in thought_lines:
        line.draw()
    
    # Draw particles
    for p in particles:
        p.draw()
    
    # Subtle text overlay that fades in and out
    font = pygame.font.SysFont(None, 24)
    
    # Choose a message with uncertain timing
    messages = [
        "...",
        "what if...",
        "but...",
        "should I...",
        "wait...",
        "uncertain...",
        "hesitant...",
    ]
    
    # Display text with uncertainty
    pulse = (math.sin(time.time() * 0.5) + 1) / 2
    if pulse > 0.8 and random.random() < 0.3:
        message = random.choice(messages)
        alpha = int(pulse * 40)
        text = font.render(message, True, (255, 255, 255, alpha))
        text_rect = text.get_rect(center=(WIDTH//2 + random.uniform(-100, 100), 
                                         HEIGHT//2 + random.uniform(-80, 80)))
        text.set_alpha(alpha)
        screen.blit(text, text_rect)
    
    # Update display
    pygame.display.flip()
    
    # Cap at 60 FPS
    clock.tick(60)

# Clean up
pygame.quit()