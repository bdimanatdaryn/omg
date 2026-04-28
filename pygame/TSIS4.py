import pygame
import random
import psycopg
import json
import os

pygame.init()


# DATABASE

DB_HOST = "localhost"
DB_NAME = "phonebook_db"
DB_USER = "postgres"
DB_PASSWORD = "2008"
DB_PORT = 5432


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


def create_table():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS snake_scores (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) NOT NULL,
                        score INTEGER NOT NULL,
                        level_reached INTEGER NOT NULL,
                        played_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            conn.commit()
    except Exception as e:
        print("DB create_table error:", e)


def save_result(username, score, level_reached):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO snake_scores (username, score, level_reached)
                    VALUES (%s, %s, %s)
                """, (username, score, level_reached))
            conn.commit()
    except Exception as e:
        print("DB save_result error:", e)


def get_top_10():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, score, level_reached, played_at
                    FROM snake_scores
                    ORDER BY score DESC, level_reached DESC, played_at ASC
                    LIMIT 10
                """)
                return cur.fetchall()
    except Exception as e:
        print("DB get_top_10 error:", e)
        return []


def get_personal_best(username):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT MAX(score)
                    FROM snake_scores
                    WHERE username = %s
                """, (username,))
                row = cur.fetchone()
                if row and row[0] is not None:
                    return row[0]
                return 0
    except Exception as e:
        print("DB get_personal_best error:", e)
        return 0



# SETTINGS JSON

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [220, 40, 40],
    "grid_overlay": True,
    "sound": True
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "snake_color" not in data:
            data["snake_color"] = DEFAULT_SETTINGS["snake_color"]
        if "grid_overlay" not in data:
            data["grid_overlay"] = DEFAULT_SETTINGS["grid_overlay"]
        if "sound" not in data:
            data["sound"] = DEFAULT_SETTINGS["sound"]

        return data
    except Exception:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


settings = load_settings()


# GAME SETTINGS

WIDTH = 600
HEIGHT = 700
TOP_AREA = 100
SIZE = 20

FIELD_WIDTH = 600
FIELD_HEIGHT = 600

COLS = FIELD_WIDTH // SIZE
ROWS = FIELD_HEIGHT // SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice Final")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
GREEN = (0, 200, 0)
BLUE = (40, 90, 255)
YELLOW = (255, 220, 0)
GRAY = (170, 170, 170)
DARK_RED = (120, 0, 0)
CYAN = (0, 220, 220)
PURPLE = (170, 80, 255)
ORANGE = (255, 160, 0)
WALL_COLOR = (110, 110, 110)

font_small = pygame.font.SysFont("Arial", 22)
font_medium = pygame.font.SysFont("Arial", 30)
font_big = pygame.font.SysFont("Arial", 40)

START_SPEED = 7
SUPER_FOOD_SCORE = 3
SUPER_FOOD_DURATION = 5000

POWERUP_FIELD_DURATION = 8000
POWERUP_EFFECT_DURATION = 5000

POWERUP_SPEED = "speed"
POWERUP_SLOW = "slow"
POWERUP_SHIELD = "shield"

COLOR_PRESETS = [
    (220, 40, 40),
    (0, 200, 0),
    (40, 90, 255),
    (255, 220, 0),
    (170, 80, 255),
    (255, 160, 0)
]


def draw_text(text, font, color, x, y):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))


def draw_centered_text(text, font, color, y):
    rendered = font.render(text, True, color)
    x = (WIDTH - rendered.get_width()) // 2
    screen.blit(rendered, (x, y))


def field_to_screen_x(grid_x):
    return grid_x * SIZE


def field_to_screen_y(grid_y):
    return TOP_AREA + grid_y * SIZE


def draw_grid():
    if not settings["grid_overlay"]:
        return

    for x in range(0, FIELD_WIDTH, SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, TOP_AREA), (x, TOP_AREA + FIELD_HEIGHT))

    for y in range(TOP_AREA, TOP_AREA + FIELD_HEIGHT, SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (FIELD_WIDTH, y))



# BUTTON

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        text_surface = font_medium.render(self.text, True, BLACK)
        text_x = self.rect.x + (self.rect.w - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.h - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)



# SPRITES

class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, color):
        super().__init__()
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = field_to_screen_x(grid_x)
        self.rect.y = field_to_screen_y(grid_y)

    @property
    def grid_x(self):
        return self.rect.x // SIZE

    @property
    def grid_y(self):
        return (self.rect.y - TOP_AREA) // SIZE


class Food(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def spawn(self, forbidden_positions):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) not in forbidden_positions:
                self.rect.x = field_to_screen_x(x)
                self.rect.y = field_to_screen_y(y)
                break

    @property
    def grid_x(self):
        return self.rect.x // SIZE

    @property
    def grid_y(self):
        return (self.rect.y - TOP_AREA) // SIZE


class SuperFood(Food):
    def __init__(self):
        super().__init__(BLUE)
        self.active = False
        self.spawn_time = 0

    def spawn(self, forbidden_positions):
        super().spawn(forbidden_positions)
        self.active = True
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if self.active and pygame.time.get_ticks() - self.spawn_time > SUPER_FOOD_DURATION:
            self.active = False


class PoisonFood(Food):
    def __init__(self):
        super().__init__(DARK_RED)
        self.active = False

    def spawn(self, forbidden_positions):
        super().spawn(forbidden_positions)
        self.active = True


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.active = False
        self.kind = None
        self.spawn_time = 0

    def set_kind_color(self):
        if self.kind == POWERUP_SPEED:
            self.image.fill(CYAN)
        elif self.kind == POWERUP_SLOW:
            self.image.fill(PURPLE)
        elif self.kind == POWERUP_SHIELD:
            self.image.fill(ORANGE)

    def spawn(self, forbidden_positions):
        self.kind = random.choice([POWERUP_SPEED, POWERUP_SLOW, POWERUP_SHIELD])
        self.set_kind_color()

        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) not in forbidden_positions:
                self.rect.x = field_to_screen_x(x)
                self.rect.y = field_to_screen_y(y)
                break

        self.active = True
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if self.active and pygame.time.get_ticks() - self.spawn_time > POWERUP_FIELD_DURATION:
            self.active = False
            self.kind = None

    @property
    def grid_x(self):
        return self.rect.x // SIZE

    @property
    def grid_y(self):
        return (self.rect.y - TOP_AREA) // SIZE


class ObstacleBlock(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = field_to_screen_x(grid_x)
        self.rect.y = field_to_screen_y(grid_y)

    @property
    def grid_x(self):
        return self.rect.x // SIZE

    @property
    def grid_y(self):
        return (self.rect.y - TOP_AREA) // SIZE



# HELPERS

def get_snake_positions(snake_list):
    positions = []
    for segment in snake_list:
        positions.append((segment.grid_x, segment.grid_y))
    return positions


def get_obstacle_positions(obstacles):
    positions = set()
    for block in obstacles:
        positions.add((block.grid_x, block.grid_y))
    return positions


def get_forbidden_positions(snake, obstacles, food, super_food, poison_food, powerup):
    positions = set(get_snake_positions(snake))
    positions.update(get_obstacle_positions(obstacles))

    positions.add((food.grid_x, food.grid_y))

    if super_food.active:
        positions.add((super_food.grid_x, super_food.grid_y))

    if poison_food.active:
        positions.add((poison_food.grid_x, poison_food.grid_y))

    if powerup.active:
        positions.add((powerup.grid_x, powerup.grid_y))

    return positions


def generate_obstacles(level, snake):
    obstacle_group = pygame.sprite.Group()

    if level < 3:
        return obstacle_group

    obstacle_count = min(4 + (level - 3) * 2, 20)
    snake_head = snake[0]
    snake_positions = set(get_snake_positions(snake))

    forbidden = set(snake_positions)

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx = snake_head.grid_x + dx
            ny = snake_head.grid_y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                forbidden.add((nx, ny))

    tries = 0
    while len(obstacle_group) < obstacle_count and tries < 2000:
        tries += 1
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)

        if (x, y) in forbidden:
            continue

        already = False
        for block in obstacle_group:
            if block.grid_x == x and block.grid_y == y:
                already = True
                break

        if already:
            continue

        obstacle_group.add(ObstacleBlock(x, y))

    return obstacle_group



# SETTINGS SCREEN

def settings_screen():
    global settings

    local_settings = {
        "snake_color": list(settings["snake_color"]),
        "grid_overlay": settings["grid_overlay"],
        "sound": settings["sound"]
    }

    btn_grid = Button(200, 180, 200, 50, "Toggle Grid")
    btn_sound = Button(200, 260, 200, 50, "Toggle Sound")
    btn_color_prev = Button(150, 360, 80, 50, "<")
    btn_color_next = Button(370, 360, 80, 50, ">")
    btn_save = Button(180, 500, 240, 60, "Save & Back")

    color_index = 0
    for i, c in enumerate(COLOR_PRESETS):
        if list(c) == local_settings["snake_color"]:
            color_index = i
            break

    while True:
        screen.fill(BLACK)

        draw_centered_text("SETTINGS", font_big, YELLOW, 60)

        draw_text(f"Grid Overlay: {'ON' if local_settings['grid_overlay'] else 'OFF'}", font_medium, WHITE, 140, 140)
        draw_text(f"Sound: {'ON' if local_settings['sound'] else 'OFF'}", font_medium, WHITE, 180, 220)
        draw_text("Snake Color:", font_medium, WHITE, 200, 320)

        pygame.draw.rect(screen, tuple(local_settings["snake_color"]), (260, 360, 80, 50))

        btn_grid.draw()
        btn_sound.draw()
        btn_color_prev.draw()
        btn_color_next.draw()
        btn_save.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if btn_grid.is_clicked(event):
                local_settings["grid_overlay"] = not local_settings["grid_overlay"]

            elif btn_sound.is_clicked(event):
                local_settings["sound"] = not local_settings["sound"]

            elif btn_color_prev.is_clicked(event):
                color_index = (color_index - 1) % len(COLOR_PRESETS)
                local_settings["snake_color"] = list(COLOR_PRESETS[color_index])

            elif btn_color_next.is_clicked(event):
                color_index = (color_index + 1) % len(COLOR_PRESETS)
                local_settings["snake_color"] = list(COLOR_PRESETS[color_index])

            elif btn_save.is_clicked(event):
                settings = local_settings
                save_settings(settings)
                return



# LEADERBOARD SCREEN

def leaderboard_screen():
    top_scores = get_top_10()
    btn_back = Button(220, 640, 160, 45, "Back")

    while True:
        screen.fill(BLACK)
        draw_centered_text("LEADERBOARD", font_big, YELLOW, 30)

        y = 100
        draw_text("Rank", font_small, WHITE, 20, y)
        draw_text("User", font_small, WHITE, 90, y)
        draw_text("Score", font_small, WHITE, 220, y)
        draw_text("Level", font_small, WHITE, 320, y)
        draw_text("Date", font_small, WHITE, 420, y)

        y += 40

        if len(top_scores) == 0:
            draw_centered_text("No records yet", font_medium, RED, 250)
        else:
            rank = 1
            for row in top_scores:
                username, score, level_reached, played_at = row
                date_str = played_at.strftime("%Y-%m-%d")

                draw_text(str(rank), font_small, WHITE, 20, y)
                draw_text(str(username), font_small, GREEN, 90, y)
                draw_text(str(score), font_small, WHITE, 235, y)
                draw_text(str(level_reached), font_small, WHITE, 335, y)
                draw_text(date_str, font_small, WHITE, 420, y)

                y += 35
                rank += 1

        btn_back.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if btn_back.is_clicked(event):
                return



# GAME OVER SCREEN

def game_over_screen(username, score, level, personal_best):
    btn_retry = Button(180, 460, 240, 60, "Retry")
    btn_menu = Button(180, 540, 240, 60, "Main Menu")

    while True:
        screen.fill(BLACK)

        draw_centered_text("GAME OVER", font_big, RED, 120)
        draw_centered_text(f"User: {username}", font_medium, WHITE, 220)
        draw_centered_text(f"Final Score: {score}", font_medium, WHITE, 270)
        draw_centered_text(f"Level Reached: {level}", font_medium, WHITE, 320)
        draw_centered_text(f"Personal Best: {personal_best}", font_medium, GREEN, 370)

        btn_retry.draw()
        btn_menu.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if btn_retry.is_clicked(event):
                return "retry"
            if btn_menu.is_clicked(event):
                return "menu"



# USERNAME SCREEN

def username_input_screen():
    username = ""
    pygame.key.start_text_input()

    btn_back = Button(220, 520, 160, 50, "Back")

    while True:
        screen.fill(BLACK)
        draw_centered_text("ENTER USERNAME", font_big, YELLOW, 100)

        box = pygame.Rect(150, 250, 300, 50)
        pygame.draw.rect(screen, WHITE, box, 2)
        draw_text(username, font_medium, GREEN, 160, 258)

        draw_centered_text("Press ENTER to start", font_small, GRAY, 340)

        btn_back.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.key.stop_text_input()
                return None

            if event.type == pygame.TEXTINPUT:
                if len(username) < 15 and event.text.isprintable():
                    username += event.text

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username.strip() != "":
                        pygame.key.stop_text_input()
                        return username.strip()

            if btn_back.is_clicked(event):
                pygame.key.stop_text_input()
                return None



# MAIN MENU

def main_menu():
    btn_play = Button(200, 180, 200, 60, "Play")
    btn_leaderboard = Button(200, 280, 200, 60, "Leaderboard")
    btn_settings = Button(200, 380, 200, 60, "Settings")
    btn_quit = Button(200, 480, 200, 60, "Quit")

    while True:
        screen.fill(BLACK)
        draw_centered_text("SNAKE GAME", font_big, YELLOW, 80)

        btn_play.draw()
        btn_leaderboard.draw()
        btn_settings.draw()
        btn_quit.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if btn_play.is_clicked(event):
                username = username_input_screen()
                if username is not None:
                    return username

            elif btn_leaderboard.is_clicked(event):
                leaderboard_screen()

            elif btn_settings.is_clicked(event):
                settings_screen()

            elif btn_quit.is_clicked(event):
                return "quit"



# GAME

def run_game(username):
    snake_color = tuple(settings["snake_color"])

    snake = [SnakeSegment(10, 10, snake_color)]
    snake_group = pygame.sprite.Group()
    snake_group.add(snake[0])

    food = Food(GREEN)
    food_group = pygame.sprite.Group(food)

    super_food = SuperFood()
    super_food_group = pygame.sprite.Group(super_food)

    poison_food = PoisonFood()
    poison_food_group = pygame.sprite.Group(poison_food)

    powerup = PowerUp()
    powerup_group = pygame.sprite.Group(powerup)

    obstacles = pygame.sprite.Group()

    food.spawn(get_snake_positions(snake))

    dx = 1
    dy = 0

    score = 0
    level = 1
    normal_food_eaten = 0
    personal_best = get_personal_best(username)

    shield_active = False
    speed_boost_active = False
    speed_boost_start = 0
    slow_motion_active = False
    slow_motion_start = 0

    while True:
        screen.fill(BLACK)
        dead = False
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_result(username, score, level)
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if dy == 1 and len(snake) > 1:
                        dead = True
                    else:
                        dx, dy = 0, -1

                elif event.key == pygame.K_DOWN:
                    if dy == -1 and len(snake) > 1:
                        dead = True
                    else:
                        dx, dy = 0, 1

                elif event.key == pygame.K_LEFT:
                    if dx == 1 and len(snake) > 1:
                        dead = True
                    else:
                        dx, dy = -1, 0

                elif event.key == pygame.K_RIGHT:
                    if dx == -1 and len(snake) > 1:
                        dead = True
                    else:
                        dx, dy = 1, 0

        if dead:
            save_result(username, score, level)
            if score > personal_best:
                personal_best = score
            return game_over_screen(username, score, level, personal_best)

        if speed_boost_active and now - speed_boost_start > POWERUP_EFFECT_DURATION:
            speed_boost_active = False

        if slow_motion_active and now - slow_motion_start > POWERUP_EFFECT_DURATION:
            slow_motion_active = False

        super_food.update()
        powerup.update()

        if not poison_food.active and random.randint(1, 250) == 1:
            forbidden = get_forbidden_positions(snake, obstacles, food, super_food, poison_food, powerup)
            poison_food.spawn(forbidden)

        if not powerup.active and random.randint(1, 300) == 1:
            forbidden = get_forbidden_positions(snake, obstacles, food, super_food, poison_food, powerup)
            powerup.spawn(forbidden)

        head = snake[0]
        new_x = head.grid_x + dx
        new_y = head.grid_y + dy

        # border collision
        if new_x < 0 or new_x >= COLS or new_y < 0 or new_y >= ROWS:
            if shield_active:
                shield_active = False
                new_x = head.grid_x
                new_y = head.grid_y
            else:
                save_result(username, score, level)
                if score > personal_best:
                    personal_best = score
                return game_over_screen(username, score, level, personal_best)

        # obstacle collision
        hit_obstacle = False
        for block in obstacles:
            if block.grid_x == new_x and block.grid_y == new_y:
                hit_obstacle = True
                break

        if hit_obstacle:
            if shield_active:
                shield_active = False
                new_x = head.grid_x
                new_y = head.grid_y
            else:
                save_result(username, score, level)
                if score > personal_best:
                    personal_best = score
                return game_over_screen(username, score, level, personal_best)

        new_head = SnakeSegment(new_x, new_y, snake_color)
        snake.insert(0, new_head)
        snake_group.add(new_head)

        ate_something = False

        if new_head.grid_x == food.grid_x and new_head.grid_y == food.grid_y:
            ate_something = True
            score += 1
            normal_food_eaten += 1

            forbidden = get_forbidden_positions(snake, obstacles, food, super_food, poison_food, powerup)
            food.spawn(forbidden)

            if normal_food_eaten % 4 == 0:
                level += 1

                if level >= 3:
                    obstacles = generate_obstacles(level, snake)

                forbidden = get_forbidden_positions(snake, obstacles, food, super_food, poison_food, powerup)
                food.spawn(forbidden)

                forbidden = get_forbidden_positions(snake, obstacles, food, super_food, poison_food, powerup)
                super_food.spawn(forbidden)

        elif super_food.active and new_head.grid_x == super_food.grid_x and new_head.grid_y == super_food.grid_y:
            ate_something = True
            score += SUPER_FOOD_SCORE
            super_food.active = False

        elif poison_food.active and new_head.grid_x == poison_food.grid_x and new_head.grid_y == poison_food.grid_y:
            ate_something = True
            poison_food.active = False

            for _ in range(2):
                if len(snake) > 1:
                    tail = snake.pop()
                    snake_group.remove(tail)

            if len(snake) <= 1:
                save_result(username, score, level)
                if score > personal_best:
                    personal_best = score
                return game_over_screen(username, score, level, personal_best)

        elif powerup.active and new_head.grid_x == powerup.grid_x and new_head.grid_y == powerup.grid_y:
            ate_something = True

            if powerup.kind == POWERUP_SPEED:
                speed_boost_active = True
                speed_boost_start = now
                slow_motion_active = False

            elif powerup.kind == POWERUP_SLOW:
                slow_motion_active = True
                slow_motion_start = now
                speed_boost_active = False

            elif powerup.kind == POWERUP_SHIELD:
                shield_active = True

            powerup.active = False
            powerup.kind = None

        if not ate_something:
            tail = snake.pop()
            snake_group.remove(tail)

        # self collision
        hit_self = False
        for part in snake[1:]:
            if new_head.grid_x == part.grid_x and new_head.grid_y == part.grid_y:
                hit_self = True
                break

        if hit_self:
            if shield_active:
                shield_active = False
                snake_group.remove(new_head)
                snake.pop(0)
            else:
                save_result(username, score, level)
                if score > personal_best:
                    personal_best = score
                return game_over_screen(username, score, level, personal_best)

        if score > personal_best:
            personal_best = score

        current_speed = START_SPEED + (level - 1)
        if speed_boost_active:
            current_speed += 4
        if slow_motion_active:
            current_speed -= 3
        if current_speed < 3:
            current_speed = 3

        snake_group.draw(screen)
        food_group.draw(screen)

        if super_food.active:
            super_food_group.draw(screen)

        if poison_food.active:
            poison_food_group.draw(screen)

        if powerup.active:
            powerup_group.draw(screen)

        obstacles.draw(screen)

        draw_grid()

        draw_text(f"User: {username}", font_small, YELLOW, 10, 8)
        draw_text(f"Score: {score}", font_small, WHITE, 10, 35)
        draw_text(f"Level: {level}", font_small, WHITE, 120, 35)
        draw_text(f"Best: {personal_best}", font_small, GREEN, 230, 35)

        if shield_active:
            draw_text("Shield: ON", font_small, ORANGE, 360, 8)

        if speed_boost_active:
            remain = max(0, (POWERUP_EFFECT_DURATION - (now - speed_boost_start)) // 1000)
            draw_text(f"Speed: {remain}s", font_small, CYAN, 360, 35)

        if slow_motion_active:
            remain = max(0, (POWERUP_EFFECT_DURATION - (now - slow_motion_start)) // 1000)
            draw_text(f"Slow: {remain}s", font_small, PURPLE, 360, 62)

        pygame.display.flip()
        clock.tick(current_speed)



# MAIN

def main():
    create_table()

    while True:
        menu_result = main_menu()

        if menu_result == "quit":
            break

        username = menu_result

        while True:
            result = run_game(username)

            if result == "retry":
                continue
            elif result == "menu":
                break
            elif result == "quit":
                pygame.quit()
                return

    pygame.quit()


if __name__ == "__main__":
    main()