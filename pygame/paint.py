import pygame

pygame.init()
Clock = pygame.time.Clock()
# colors
RED = (255,0,0)
BLACK = (0,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)

start_pos = None
temp_surface = None

current_tool = 'brush'
current_color = BLACK
eraser_color = WHITE


screen = pygame.display.set_mode((1000,700))
screen.fill((255,255,255))
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_color = RED
            if event.key == pygame.K_b:
                current_color = BLACK
            if event.key == pygame.K_g:
                current_color = GREEN

            if event.key == pygame.K_1:
                current_tool = 'brush'
            if event.key == pygame.K_2:
                current_tool = 'eraser'
            if event.key == pygame.K_3:
                current_tool = 'rectangle'
            if event.key == pygame.K_4:
                current_tool = 'circle'
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_tool == 'rectangle':
                start_pos = event.pos  
                temp_surface = screen.copy()
            if current_tool == 'circle':
                start_pos = event.pos
                temp_surface = screen.copy()

        if event.type == pygame.MOUSEBUTTONUP:
            if current_tool == 'rectangle':
                start_pos = None
                temp_surface = None
            if current_tool == 'circle':
                start_pos = None
                temp_surface = None

    mouse = pygame.mouse.get_pressed()

    if mouse[0]:
        x, y = pygame.mouse.get_pos()

        if current_tool == 'brush':
            pygame.draw.circle(screen, current_color, (x, y), 5)

        if current_tool == 'eraser':
            pygame.draw.circle(screen, eraser_color, (x, y), 5)
    

    if mouse[0] and current_tool == 'rectangle' and start_pos:
        screen.blit(temp_surface, (0, 0))

        x1, y1 = start_pos
        x2, y2 = pygame.mouse.get_pos()

        rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )

        pygame.draw.rect(screen, current_color, rect, 2)

    if mouse[0] and current_tool == 'circle' and start_pos:
        screen.blit(temp_surface, (0, 0))

        x1, y1 = start_pos
        x2, y2 = pygame.mouse.get_pos()

        radius = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5)

        pygame.draw.circle(screen, current_color, start_pos, radius, 2)

    pygame.display.update()
    pygame.time.Clock.tick(60)

pygame.quit()