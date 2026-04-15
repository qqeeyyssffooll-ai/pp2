import pygame
from clock import angles

pygame.init()
pygame.display.set_caption("Mickeys Clock")
screen = pygame.display.set_mode((600, 600))

pygame.display.set_icon(pygame.image.load("images/icon.png"))
bg = pygame.image.load("images/clock_face.png")
right = pygame.image.load("images/right_hand.png")
left = pygame.image.load("images/left_hand.png")

pivot = (300, 300) 
offset_r = pygame.math.Vector2(0, -75)
offset_l = pygame.math.Vector2(0, -137)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    m_angle, s_angle = angles()

    m_hand = pygame.transform.rotate(right, -m_angle)
    m_rotate = offset_r.rotate(m_angle)
    m_pos = m_hand.get_rect(center = pivot + m_rotate)

    s_hand = pygame.transform.rotate(left, -s_angle)
    s_rotate = offset_l.rotate(s_angle)
    s_pos = s_hand.get_rect(center = pivot + s_rotate)

    screen.blit(bg, (0, 0))
    screen.blit(m_hand, m_pos)
    screen.blit(s_hand, s_pos)
    pygame.display.update()

pygame.quit()