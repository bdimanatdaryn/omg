import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

image = pygame.image.load("ball.png")

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((255,255,255))
    screen.blit(image, (50,50))

    pygame.display.flip()
    clock.tick(60)