import pygame
import player

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

player.load_track()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_s:
                player.play()

            if event.key == pygame.K_p:
                player.pause()

            if event.key == pygame.K_n:
                player.next_track()

            if event.key == pygame.K_b:
                player.prev_track()

    screen.fill((0, 0, 0))

    text = font.render(player.get_name(), True, (255, 255, 255))
    rect = text.get_rect(center=(300, 250))
    screen.blit(text, rect)

    controls = [
        "S = Start",
        "P = Pause",
        "N = Next",
        "B = Back",
        "Q = Quit"
    ]

    y = 350
    for line in controls:
        surf = font.render(line, True, (255, 255, 255))
        r = surf.get_rect(center=(300, y))
        screen.blit(surf, r)
        y += 35

    progress = player.get_progress()

    pygame.draw.rect(screen, (100, 100, 100), (100, 550, 400, 10))
    pygame.draw.rect(screen, (0, 255, 0), (100, 550, 400 * progress, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()