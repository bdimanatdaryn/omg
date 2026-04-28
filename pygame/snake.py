import pygame
import psycopg2
import random
from datetime import datetime

pygame.init()

conn=psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008"
)

cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS snake_scores (id SERIAL PRIMARY KEY,username VARCHAR(50) NOT NULL,score INTEGER NOT NULL,level_reached INTEGER NOT NULL,played_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
conn.commit()



# атрибуты
screen = pygame.display.set_mode((600,600)) 
SIZE_BLOCK =20
SUPER_FOOD_COLOR = (0, 0, 255)
super_food_active = False
super_food_timer = 0
SUPER_FOOD_DURATION = 5  # секунд
SUPER_FOOD_SCORE = 3
score = 0
level = 1
super_food_x = 0
super_food_y = 0
normal_food_eaten = 0

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
# spawning super food 
def super_food_spawn():
    global super_food_x, super_food_y, super_food_active, super_food_timer

    while True:
        super_food_x = random.randint(0, COUNT_BLOCKS - 1)
        super_food_y = random.randint(0, COUNT_BLOCKS - 1)

        is_on_snake = False
        for block in snake_block:
            if block.x == super_food_x and block.y == super_food_y:
                is_on_snake = True

        if not is_on_snake:
            break

    super_food_active = True
    super_food_timer = pygame.time.get_ticks()

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
        normal_food_eaten += 1



        if normal_food_eaten % 4 == 0 and normal_food_eaten != 0:
            game_speed += 1
            level += 1
            super_food_spawn()
    if super_food_active:
        draw_block(SUPER_FOOD_COLOR, super_food_y, super_food_x)

    if super_food_active and snake_block[0].x == super_food_x and snake_block[0].y == super_food_y:
        snake_block.append(SnakeBlock(prev_x, prev_y))
        score += SUPER_FOOD_SCORE
        super_food_active = False

    if super_food_active:
        current_time = pygame.time.get_ticks()
        if (current_time - super_food_timer) > SUPER_FOOD_DURATION * 1000:
            super_food_active = False
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