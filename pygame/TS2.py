import pygame
import math
from datetime import datetime

pygame.init()

# цвета
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (150, 150, 255)

# окно
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Advanced")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# холст
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# текущие настройки
current_color = BLACK
eraser_color = WHITE
current_tool = "pencil"
brush_size = 5

start_pos = None
prev_pos = None
drawing = False

# кнопки цветов
color_buttons = [
    (pygame.Rect(10, 10, 40, 40), RED),
    (pygame.Rect(60, 10, 40, 40), BLACK),
    (pygame.Rect(110, 10, 40, 40), GREEN),
    (pygame.Rect(160, 10, 40, 40), WHITE),
]

# кнопки инструментов
tool_buttons = [
    (pygame.Rect(10, 60, 90, 30), "pencil"),
    (pygame.Rect(105, 60, 90, 30), "line"),
    (pygame.Rect(200, 60, 90, 30), "eraser"),
    (pygame.Rect(295, 60, 90, 30), "fill"),
    (pygame.Rect(390, 60, 90, 30), "rectangle"),
    (pygame.Rect(485, 60, 90, 30), "circle"),
    (pygame.Rect(580, 60, 90, 30), "square"),
    (pygame.Rect(675, 60, 90, 30), "right_triangle"),
    (pygame.Rect(770, 60, 90, 30), "equilateral_triangle"),
    (pygame.Rect(865, 60, 90, 30), "rhombus"),
]

# текст
text_mode = False
text_pos = None
typed_text = ""

# заливка
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
        stack += [(px+1,py),(px-1,py),(px,py+1),(px,py-1)]

# сохранение
def save_canvas():
    name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pygame.image.save(canvas, f"paint_{name}.png")

running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))

    # рисуем кнопки цветов
    for rect, color in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # рисуем кнопки инструментов
    for rect, tool in tool_buttons:
        col = BLUE if tool == current_tool else GRAY
        pygame.draw.rect(screen, col, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        txt = font.render(tool, True, BLACK)
        screen.blit(txt, (rect.x + 3, rect.y + 5))

    # предпросмотр текста
    if text_mode and text_pos:
        txt = font.render(typed_text, True, current_color)
        screen.blit(txt, text_pos)

    # предпросмотр фигур
    if drawing and start_pos:
        x1, y1 = start_pos
        x2, y2 = pygame.mouse.get_pos()

        if current_tool == "line":
            pygame.draw.line(screen, current_color, start_pos, (x2,y2), brush_size)

        elif current_tool == "rectangle":
            rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
            pygame.draw.rect(screen, current_color, rect, brush_size)

        elif current_tool == "circle":
            r = int(((x2-x1)**2+(y2-y1)**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, r, brush_size)

        elif current_tool == "square":
            size = min(abs(x2-x1), abs(y2-y1))
            pygame.draw.rect(screen, current_color, (x1,y1,size,size), brush_size)

        elif current_tool == "right_triangle":
            pts = [(x1,y1),(x2,y1),(x1,y2)]
            pygame.draw.polygon(screen, current_color, pts, brush_size)

        elif current_tool == "equilateral_triangle":
            size = abs(x2-x1)
            h = int(size * math.sqrt(3)/2)
            if y2 > y1:
                h = -h
            pts = [(x1,y1),(x1+size,y1),(x1+size//2,y1-h)]
            pygame.draw.polygon(screen, current_color, pts, brush_size)

        elif current_tool == "rhombus":
            cx, cy = (x1+x2)//2, (y1+y2)//2
            pts = [(cx,y1),(x2,cy),(cx,y2),(x1,cy)]
            pygame.draw.polygon(screen, current_color, pts, brush_size)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # клавиатура
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

        # нажатие мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = False

            # проверка цветов
            for rect, color in color_buttons:
                if rect.collidepoint(event.pos):
                    current_color = color
                    clicked = True
                    break

            # проверка инструментов
            for rect, tool in tool_buttons:
                if rect.collidepoint(event.pos):
                    current_tool = tool
                    clicked = True
                    break

            # если не кнопка — начинаем рисовать
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

        # движение мыши
        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == "pencil":
                pygame.draw.line(canvas, current_color, prev_pos, event.pos, brush_size)
                prev_pos = event.pos

            elif current_tool == "eraser":
                pygame.draw.line(canvas, eraser_color, prev_pos, event.pos, brush_size)
                prev_pos = event.pos

        # отпустили мышь
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            x1,y1 = start_pos
            x2,y2 = event.pos

            if current_tool == "line":
                pygame.draw.line(canvas, current_color, start_pos, event.pos, brush_size)

            elif current_tool == "rectangle":
                rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
                pygame.draw.rect(canvas, current_color, rect, brush_size)

            elif current_tool == "circle":
                r = int(((x2-x1)**2+(y2-y1)**2)**0.5)
                pygame.draw.circle(canvas, current_color, start_pos, r, brush_size)

            elif current_tool == "square":
                size = min(abs(x2-x1), abs(y2-y1))
                pygame.draw.rect(canvas, current_color, (x1,y1,size,size), brush_size)

            elif current_tool == "right_triangle":
                pts = [(x1,y1),(x2,y1),(x1,y2)]
                pygame.draw.polygon(canvas, current_color, pts, brush_size)

            elif current_tool == "equilateral_triangle":
                size = abs(x2-x1)
                h = int(size * math.sqrt(3)/2)
                if y2 > y1:
                    h = -h
                pts = [(x1,y1),(x1+size,y1),(x1+size//2,y1-h)]
                pygame.draw.polygon(canvas, current_color, pts, brush_size)

            elif current_tool == "rhombus":
                cx, cy = (x1+x2)//2, (y1+y2)//2
                pts = [(cx,y1),(x2,cy),(cx,y2),(x1,cy)]
                pygame.draw.polygon(canvas, current_color, pts, brush_size)

            drawing = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()