import pygame
import math
from datetime import datetime

pygame.init()

#  COLORS 
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

#  SCREEN 
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Advanced")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

#  CANVAS 
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

#  VARIABLES 
current_color = BLACK
eraser_color = WHITE

current_tool = "pencil"
brush_size = 5

start_pos = None
prev_pos = None

drawing = False

# Text tool variables
text_mode = False
text_pos = None
typed_text = ""

#  FLOOD FILL FUNCTION 
def flood_fill(surface, start_pos, fill_color):
    x, y = start_pos

    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or px >= WIDTH or py < 0 or py >= HEIGHT:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))


#  SAVE FUNCTION 
def save_canvas():
    time_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = "paint_save_" + time_name + ".png"
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


#  MAIN LOOP 
running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))

    # Live preview for text
    if text_mode and text_pos is not None:
        text_surface = font.render(typed_text, True, current_color)
        screen.blit(text_surface, text_pos)

    # Live preview for shapes
    mouse_pos = pygame.mouse.get_pos()

    if drawing and start_pos is not None:
        x1, y1 = start_pos
        x2, y2 = mouse_pos

        if current_tool == "line":
            pygame.draw.line(screen, current_color, start_pos, mouse_pos, brush_size)

        elif current_tool == "rectangle":
            rect = pygame.Rect(
                min(x1, x2),
                min(y1, y2),
                abs(x2 - x1),
                abs(y2 - y1)
            )
            pygame.draw.rect(screen, current_color, rect, brush_size)

        elif current_tool == "circle":
            radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            pygame.draw.circle(screen, current_color, start_pos, radius, brush_size)

        elif current_tool == "square":
            size = min(abs(x2 - x1), abs(y2 - y1))

            if x2 < x1:
                draw_x = x1 - size
            else:
                draw_x = x1

            if y2 < y1:
                draw_y = y1 - size
            else:
                draw_y = y1

            rect = pygame.Rect(draw_x, draw_y, size, size)
            pygame.draw.rect(screen, current_color, rect, brush_size)

        elif current_tool == "right_triangle":
            points = [
                (x1, y1),
                (x2, y1),
                (x1, y2)
            ]
            pygame.draw.polygon(screen, current_color, points, brush_size)

        elif current_tool == "equilateral_triangle":
            size = abs(x2 - x1)
            h = int(size * math.sqrt(3) / 2)

            if y2 > y1:
                h = -h

            points = [
                (x1, y1),
                (x1 + size, y1),
                (x1 + size // 2, y1 - h)
            ]
            pygame.draw.polygon(screen, current_color, points, brush_size)

        elif current_tool == "rhombus":
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            points = [
                (cx, y1),
                (x2, cy),
                (cx, y2),
                (x1, cy)
            ]
            pygame.draw.polygon(screen, current_color, points, brush_size)

    #  EVENTS 
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        #  KEYBOARD 
        if event.type == pygame.KEYDOWN:

            # Ctrl + S save
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            # Text typing
            elif text_mode:
                if event.key == pygame.K_RETURN:
                    text_surface = font.render(typed_text, True, current_color)
                    canvas.blit(text_surface, text_pos)

                    text_mode = False
                    typed_text = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    typed_text = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                else:
                    typed_text += event.unicode

            else:
                # Colors
                if event.key == pygame.K_r:
                    current_color = RED
                elif event.key == pygame.K_b:
                    current_color = BLACK
                elif event.key == pygame.K_g:
                    current_color = GREEN
                elif event.key == pygame.K_w:
                    current_color = WHITE

                # Brush size
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

                # Tools
                elif event.key == pygame.K_p:
                    current_tool = "pencil"
                elif event.key == pygame.K_l:
                    current_tool = "line"
                elif event.key == pygame.K_e:
                    current_tool = "eraser"
                elif event.key == pygame.K_f:
                    current_tool = "fill"
                elif event.key == pygame.K_t:
                    current_tool = "text"
                elif event.key == pygame.K_q:
                    current_tool = "rectangle"
                elif event.key == pygame.K_c:
                    current_tool = "circle"
                elif event.key == pygame.K_s:
                    current_tool = "square"
                elif event.key == pygame.K_a:
                    current_tool = "right_triangle"
                elif event.key == pygame.K_z:
                    current_tool = "equilateral_triangle"
                elif event.key == pygame.K_x:
                    current_tool = "rhombus"

        #  MOUSE DOWN 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                start_pos = event.pos
                prev_pos = event.pos
                drawing = True

                if current_tool == "fill":
                    flood_fill(canvas, event.pos, current_color)
                    drawing = False

                elif current_tool == "text":
                    text_mode = True
                    text_pos = event.pos
                    typed_text = ""
                    drawing = False

        #  MOUSE MOTION 
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == "pencil":
                    pygame.draw.line(canvas, current_color, prev_pos, event.pos, brush_size)
                    prev_pos = event.pos

                elif current_tool == "eraser":
                    pygame.draw.line(canvas, eraser_color, prev_pos, event.pos, brush_size)
                    prev_pos = event.pos

        #  MOUSE UP 
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos

                if current_tool == "line":
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)

                elif current_tool == "rectangle":
                    rect = pygame.Rect(
                        min(x1, x2),
                        min(y1, y2),
                        abs(x2 - x1),
                        abs(y2 - y1)
                    )
                    pygame.draw.rect(canvas, current_color, rect, brush_size)

                elif current_tool == "circle":
                    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)

                elif current_tool == "square":
                    size = min(abs(x2 - x1), abs(y2 - y1))

                    if x2 < x1:
                        draw_x = x1 - size
                    else:
                        draw_x = x1

                    if y2 < y1:
                        draw_y = y1 - size
                    else:
                        draw_y = y1

                    rect = pygame.Rect(draw_x, draw_y, size, size)
                    pygame.draw.rect(canvas, current_color, rect, brush_size)

                elif current_tool == "right_triangle":
                    points = [
                        (x1, y1),
                        (x2, y1),
                        (x1, y2)
                    ]
                    pygame.draw.polygon(canvas, current_color, points, brush_size)

                elif current_tool == "equilateral_triangle":
                    size = abs(x2 - x1)
                    h = int(size * math.sqrt(3) / 2)

                    if y2 > y1:
                        h = -h

                    points = [
                        (x1, y1),
                        (x1 + size, y1),
                        (x1 + size // 2, y1 - h)
                    ]
                    pygame.draw.polygon(canvas, current_color, points, brush_size)

                elif current_tool == "rhombus":
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    points = [
                        (cx, y1),
                        (x2, cy),
                        (cx, y2),
                        (x1, cy)
                    ]
                    pygame.draw.polygon(canvas, current_color, points, brush_size)

                drawing = False
                start_pos = None
                prev_pos = None

    pygame.display.update()
    clock.tick(60)

pygame.quit()