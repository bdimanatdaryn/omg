import pygame
import random

pygame.init()

# атрибуты
screen = pygame.display.set_mode((600,600))
SIZE_BLOCK =20
score = 0
level = 1
color = (255,255,255)
COUNT_BLOCKS = 20
MARGIN = 1
SNAKE_COLOR = (255,0,0)
FOOD_COLOR = (0,255,0)
SNAKE_SPEED = 1
clock = pygame.time.Clock()
game_speed = 5
running = True
dx = 0
dy = 0
food_x = random.randint(0,COUNT_BLOCKS-1)
food_y = random.randint(0,COUNT_BLOCKS-1)

font = pygame.font.SysFont(None,20)

# swapning food 
def food_spawn():
    global food_x, food_y

    while True:
        food_x = random.randint(0, COUNT_BLOCKS - 1)
        food_y = random.randint(0, COUNT_BLOCKS - 1)

        # проверяем чтобы еда не появилась в змейке
        is_on_snake = False
        for block in snake_block:
            if block.x == food_x and block.y == food_y:
                is_on_snake = True

        if not is_on_snake:
            break
class SnakeBlock:
    def __init__(self,x,y):
        self.x = x
        self.y = y

# drawing all rect in a game
def draw_block(color,row,column):
    pygame.draw.rect(screen,color,(90+column*SIZE_BLOCK+MARGIN*(column+1),80+row*SIZE_BLOCK+MARGIN*(row+1),SIZE_BLOCK,SIZE_BLOCK))


snake_block = [SnakeBlock(9,9)]

# starting a game
while running:
    screen.fill((0,0,0))
    # stoping a game and different keys for snake movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dx = SNAKE_SPEED
                dy = 0
            if event.key == pygame.K_LEFT:
                dx = -SNAKE_SPEED
                dy = 0
            if event.key == pygame.K_UP:
                dx = 0
                dy = -SNAKE_SPEED
            if event.key == pygame.K_DOWN:
                dx = 0
                dy = SNAKE_SPEED
    prev_x = snake_block[0].x
    prev_y = snake_block[0].y

    snake_block[0].x += dx
    snake_block[0].y += dy

# control of different parts of body of a snake
    for i in range(1,len(snake_block)):
        current_x = snake_block[i].x
        current_y = snake_block[i].y

        snake_block[i].x = prev_x
        snake_block[i].y = prev_y

        prev_x = current_x
        prev_y = current_y
# draw play field
    for row in range(COUNT_BLOCKS):
        for column in range(COUNT_BLOCKS):    
            draw_block(color,row,column)
#draw snake
    for block in snake_block:
        draw_block(SNAKE_COLOR,block.y,block.x)
    
    for block in snake_block[1:]:
        if snake_block[0].x == block.x and snake_block[0].y == block.y:
            running = False
    if snake_block[0].x < 0 or snake_block[0].x >= COUNT_BLOCKS or \
        snake_block[0].y <0 or snake_block[0].y >= COUNT_BLOCKS:
        running = False
# score food level
    draw_block(FOOD_COLOR, food_y, food_x)
    if snake_block[0].x == food_x and snake_block[0].y == food_y:
        snake_block.append(SnakeBlock(prev_x, prev_y))
        food_spawn()
        score += 1

        if score % 4 == 0:
            game_speed += 1
            level += 1

# text in a game 
    score_text = font.render(f"Score: {score}", True, (255,0,0))
    screen.blit(score_text, (10,5))
    level_text = font.render(f"Level: {level}", True, (255,0,0))
    screen.blit(level_text, (80,5))
# Game over text
    if not running:
        font = pygame.font.SysFont("Arial",30)
        text = font.render("GAME OVER", True, (255,0,0))
        screen.blit(text, (200,250))
    
    pygame.display.flip()
    clock.tick(game_speed)
pygame.quit()