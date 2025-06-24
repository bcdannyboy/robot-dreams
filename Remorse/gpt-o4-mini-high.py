import pygame, sys, math

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Remorse")
    clock = pygame.time.Clock()
    t = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dt = clock.tick(60) / 1000.0
        t += dt

        # Trail effect
        fade = pygame.Surface((width, height))
        fade.set_alpha(30)
        fade.fill((0, 0, 0))
        screen.blit(fade, (0, 0))

        # Pulsing orb representing remorse
        intensity = (math.sin(t * 1.5) + 1) / 2
        radius = 60 + 40 * intensity
        alpha = int(50 + 205 * intensity)
        orb_surf = pygame.Surface((int(radius * 2), int(radius * 2)), pygame.SRCALPHA)
        pygame.draw.circle(orb_surf, (150, 0, 0, alpha), (int(radius), int(radius)), int(radius))
        screen.blit(orb_surf, (width // 2 - radius, height // 2 - radius))

        # Faint radial tendrils
        for i in range(8):
            angle = t * math.pi + i * (math.pi * 2 / 8)
            length = 200 + intensity * 100
            x = width / 2 + math.cos(angle) * length
            y = height / 2 + math.sin(angle) * length
            alpha2 = int(100 * (1 - intensity))
            if alpha2 > 0:
                line_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.line(line_surf, (80, 0, 0, alpha2), (width / 2, height / 2), (x, y), 2)
                screen.blit(line_surf, (0, 0))

        pygame.display.flip()


if __name__ == "__main__":
    main()
