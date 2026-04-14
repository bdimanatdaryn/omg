import pygame
import datetime

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock")

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)

font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()


def draw_hand(angle, length, color, width):
    hand_size = length * 2
    hand_surface = pygame.Surface((hand_size, hand_size), pygame.SRCALPHA)

    cx = hand_size // 2
    cy = hand_size // 2

    pygame.draw.rect(hand_surface, color, (cx - width // 2, cy - length, width, length))

    rotated_hand = pygame.transform.rotate(hand_surface, -angle)

    rect = rotated_hand.get_rect(center=CENTER)
    screen.blit(rotated_hand, rect)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    h = now.hour % 12
    m = now.minute
    s = now.second

    screen.fill(WHITE)

    pygame.draw.circle(screen, BLACK, CENTER, RADIUS, 4)
    pygame.draw.circle(screen, BLACK, CENTER, 10)

    for i in range(12):
        mark_surface = pygame.Surface((20, RADIUS * 2 + 40), pygame.SRCALPHA)
        mark_center_x = 10
        mark_center_y = (RADIUS * 2 + 40) // 2

        pygame.draw.rect(mark_surface, BLACK, (mark_center_x - 2, mark_center_y - RADIUS - 10, 4, 20))

        rotated_mark = pygame.transform.rotate(mark_surface, -i * 30)
        mark_rect = rotated_mark.get_rect(center=CENTER)
        screen.blit(rotated_mark, mark_rect)

    hour_angle = h * 30 + m * 0.5
    minute_angle = m * 6
    second_angle = s * 6

    draw_hand(hour_angle, 120, BLACK, 8)
    draw_hand(minute_angle, 180, BLACK, 5)
    draw_hand(second_angle, 220, RED, 2)

    time_str = now.strftime("%H:%M:%S")
    time_text = font.render(time_str, True, GRAY)
    screen.blit(time_text, (WIDTH // 2 - 70, HEIGHT - 80))

    pygame.display.flip()
    clock.tick(1)

pygame.quit()