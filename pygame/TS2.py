import pygame
import math
from datetime import datetime

pygame.init()

# COLORS
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (150, 150, 255)

# SCREEN
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Advanced")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# CANVAS
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# VARIABLES
current_color = BLACK
eraser_color = WHITE
current_tool = "pencil"
brush_size = 5

start_pos = None
prev_pos = None
drawing = False

# 🎨 COLOR BUTTONS
color_buttons = [
    (pygame.Rect(10, 10, 40, 40), RED),
    (pygame.Rect(60, 10, 40, 40), BLACK),
    (pygame.Rect(110, 10, 40, 40), GREEN),
    (pygame.Rect(160, 10, 40, 40), WHITE),
]

# 🧰 TOOL BUTTONS
tool_buttons = [
    (pygame.Rect(10, 60, 80, 30), "pencil"),
    (pygame.Rect(100, 60, 80, 30), "line"),
    (pygame.Rect(190, 60, 80, 30), "eraser"),
    (pygame.Rect(280, 60, 80, 30), "fill"),
    (pygame.Rect(370, 60, 80, 30), "rectangle"),
    (pygame.Rect(460, 60, 80, 30), "circle"),
]

# TEXT TOOL
text_mode = False
text_pos = None
typed_text = ""

# FILL
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

# SAVE
def save_canvas():
    time_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pygame.image.save(canvas, "paint_" + time_name + ".png")

# MAIN LOOP
running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))

    # 🎨 DRAW COLOR BUTTONS
    for rect, color in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # 🧰 DRAW TOOL BUTTONS
    for rect, tool in tool_buttons:
        color = BLUE if tool == current_tool else GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = font.render(tool, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 5))

    # TEXT PREVIEW
    if text_mode and text_pos:
        txt = font.render(typed_text, True, current_color)
        screen.blit(txt, text_pos)

    # DRAW PREVIEW
    if drawing and start_pos:
        x1, y1 = start_pos
        x2, y2 = pygame.mouse.get_pos()

        if current_tool == "line":
            pygame.draw.line(screen, current_color, start_pos, (x2, y2), brush_size)

        elif current_tool == "rectangle":
            rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
            pygame.draw.rect(screen, current_color, rect, brush_size)

        elif current_tool == "circle":
            r = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, r, brush_size)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # KEYBOARD
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            elif text_mode:
                if event.key == pygame.K_RETURN:
                    txt = font.render(typed_text, True, current_color)
                    canvas.blit(txt, text_pos)
                    text_mode = False
                    typed_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                else:
                    typed_text += event.unicode

        # MOUSE DOWN
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            clicked = False

            # COLOR BUTTONS
            for rect, color in color_buttons:
                if rect.collidepoint(event.pos):
                    current_color = color
                    clicked = True
                    break

            # TOOL BUTTONS
            for rect, tool in tool_buttons:
                if rect.collidepoint(event.pos):
                    current_tool = tool
                    clicked = True
                    break

            if not clicked:
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

        # MOUSE MOVE
        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == "pencil":
                pygame.draw.line(canvas, current_color, prev_pos, event.pos, brush_size)
                prev_pos = event.pos

            elif current_tool == "eraser":
                pygame.draw.line(canvas, eraser_color, prev_pos, event.pos, brush_size)
                prev_pos = event.pos

        # MOUSE UP
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            end = event.pos

            if current_tool == "line":
                pygame.draw.line(canvas, current_color, start_pos, end, brush_size)

            elif current_tool == "rectangle":
                rect = pygame.Rect(min(start_pos[0],end[0]), min(start_pos[1],end[1]),
                                   abs(end[0]-start_pos[0]), abs(end[1]-start_pos[1]))
                pygame.draw.rect(canvas, current_color, rect, brush_size)

            elif current_tool == "circle":
                r = int(((end[0]-start_pos[0])**2 + (end[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(canvas, current_color, start_pos, r, brush_size)

            drawing = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()