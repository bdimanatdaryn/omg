import pygame

pygame.init()

screen = pygame.display.set_mode((600,400))

clock = pygame.time.Clock()
run = True
x=30
y=30
radius=25
speed=20
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP] and y-speed-radius>=0 :
        y -= speed
    if pressed[pygame.K_DOWN] and y+speed+radius<=400:
        y += speed
    if pressed[pygame.K_RIGHT] and x+speed+radius<=600:
        x += speed
    if pressed[pygame.K_LEFT] and x-speed-radius>=0:
        x -= speed

    screen.fill((200,200,200))
    pygame.draw.circle(screen,(200,0,0),(x,y),radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()