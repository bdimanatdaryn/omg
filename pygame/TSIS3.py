import pygame
from pygame.locals import *
import random
import json
import os

pygame.init()

#  BASIC SETTINGS 

WIDTH, HEIGHT = 300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

clock = pygame.time.Clock()
FPS = 60

BASE_DIR = os.path.dirname(__file__)

LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

FINISH_DISTANCE = 2000

#  COLORS 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
DARK_GRAY = (80, 80, 80)
RED = (220, 40, 40)
GREEN = (40, 180, 40)
BLUE = (40, 80, 220)
YELLOW = (230, 190, 40)

font_small = pygame.font.SysFont(None, 24)
font_medium = pygame.font.SysFont(None, 32)
font_big = pygame.font.SysFont(None, 46)

#  GAME STATES 

MENU = "menu"
USERNAME = "username"
GAME = "game"
GAME_OVER = "game_over"
LEADERBOARD = "leaderboard"
SETTINGS = "settings"

state = MENU

#  DEFAULT SETTINGS 

default_settings = {
    "sound": True,
    "car_color": "default",
    "difficulty": "normal"
}

settings = default_settings.copy()


#  JSON FUNCTIONS 

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            for key in default_settings:
                if key not in data:
                    data[key] = default_settings[key]

            return data

        except:
            return default_settings.copy()

    return default_settings.copy()


def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []

    return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def add_to_leaderboard(name, score, distance, coins):
    data = load_leaderboard()

    entry = {
        "name": name,
        "score": score,
        "distance": int(distance),
        "coins": coins
    }

    data.append(entry)

    data.sort(key=lambda x: x["score"], reverse=True)
    data = data[:10]

    save_leaderboard(data)


settings = load_settings()


#  BUTTON FUNCTION 

def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, GRAY, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)

    label = font_medium.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

    return rect


def draw_text(text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


#  IMAGE COLOR FUNCTION 

def apply_car_color(image, color_name):
    if color_name == "default":
        return image.copy()

    colored = image.copy()

    if color_name == "red":
        color = (255, 80, 80, 255)
    elif color_name == "blue":
        color = (80, 120, 255, 255)
    elif color_name == "green":
        color = (80, 255, 120, 255)
    else:
        return image.copy()

    colored.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
    return colored


#  CLASSES 

class Nitro(pygame.sprite.Sprite):
    def __init__(self, path="nitro.png"):
        super().__init__()
        image = pygame.image.load(os.path.join(BASE_DIR, path)).convert_alpha()
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (150, -2000)
        self.speed = 5

    def move(self):
        self.rect.centery += self.speed


class Shield(pygame.sprite.Sprite):
    def __init__(self, path="shield.png"):
        super().__init__()
        image = pygame.image.load(os.path.join(BASE_DIR, path)).convert_alpha()
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (150, -2000)
        self.speed = 5

    def move(self):
        self.rect.centery += self.speed


class Repair(pygame.sprite.Sprite):
    def __init__(self, path="repair.png"):
        super().__init__()
        image = pygame.image.load(os.path.join(BASE_DIR, path)).convert_alpha()
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (150, -2000)
        self.speed = 5

    def move(self):
        self.rect.centery += self.speed


class Slow(pygame.sprite.Sprite):
    def __init__(self, path="slow.png"):
        super().__init__()
        image = pygame.image.load(os.path.join(BASE_DIR, path)).convert_alpha()
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (150, -2000)
        self.speed = 5

    def move(self):
        self.rect.centery += self.speed


class Coin(pygame.sprite.Sprite):
    def __init__(self, path="coin.png"):
        super().__init__()
        image = pygame.image.load(os.path.join(BASE_DIR, path)).convert_alpha()
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47, 253), -20)
        self.speed = 3

    def move(self):
        self.rect.centery += self.speed

        if self.rect.centery > 650:
            self.respawn()

    def respawn(self):
        self.rect.centery = -20
        self.rect.centerx = random.randint(47, 253)


class PlayerCar(pygame.sprite.Sprite):
    def __init__(self, path="Player.png"):
        super().__init__()
        image = pygame.image.load(os.path.join(BASE_DIR, path)).convert_alpha()
        image = pygame.transform.scale(image, (75, 150))

        self.original_image = image
        self.image = apply_car_color(self.original_image, settings["car_color"])

        self.rect = self.image.get_rect()
        self.rect.center = (150, 525)
        self.speed = 3

    def update_color(self):
        self.image = apply_car_color(self.original_image, settings["car_color"])

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.rect.centerx -= self.speed

        elif keys[K_RIGHT]:
            self.rect.centerx += self.speed

        if self.rect.centerx < 47:
            self.rect.centerx = 47

        if self.rect.centerx > 253:
            self.rect.centerx = 253


class OpposingCar(pygame.sprite.Sprite):
    def __init__(self, path="Enemy.png"):
        super().__init__()
        image = pygame.image.load(os.path.join(BASE_DIR, path)).convert_alpha()
        self.image = pygame.transform.scale(image, (70, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47, 253), 75)

        self.speed = 4

    def move(self):
        self.rect.centery += self.speed

        if self.rect.centery > 675:
            self.respawn()

    def respawn(self):
        self.rect.centery = -75
        self.rect.centerx = random.randint(47, 253)

        while abs(self.rect.centerx - player.rect.centerx) < 60:
            self.rect.centerx = random.randint(47, 253)


class BackgroundLoading:
    def __init__(self, path="road.png"):
        self.image = pygame.image.load(os.path.join(BASE_DIR, path)).convert()
        self.image = pygame.transform.scale(self.image, (300, 300))

        rect1 = self.image.get_rect()
        rect2 = self.image.get_rect()
        rect3 = self.image.get_rect()

        rect2.centery += 300
        rect3.centery += 600

        self.rectangles = []
        self.rectangles.append(rect1)
        self.rectangles.append(rect2)
        self.rectangles.append(rect3)

    def draw(self):
        for rectangle in self.rectangles:
            screen.blit(self.image, rectangle)

    def move(self):
        for rectangle in self.rectangles:
            rectangle.centery += 2

            if rectangle.centery > 750:
                rectangle.centery = -150


#  GAME VARIABLES 

username = ""
score = 0
coins_collected = 0
distance = 0
bonus_score = 0

game_saved = False

player = None
opponent = None
coin = None
nitro = None
shield = None
repair = None
slow = None
background = None

cars = None
opponents = None
coins = None
nitos = None
shields = None
repairs = None
slows = None

honk_sound = None

POWERUP_SPAWN_DELAY = 12000
POWERUP_TIMEOUT = 7000
NITRO_DURATION = 5000

SLOW_SPAWN_DELAY = 18000
SLOW_EFFECT_DURATION = 3000

powerup_visible = False
powerup_spawn_time = 0
last_powerup_time = 0

current_powerup = None
active_powerup = None
active_powerup_end_time = 0

slow_show = False
slow_active = False
last_slow_time = 0
slow_start_time = 0


#  DIFFICULTY 

def get_difficulty_values():
    if settings["difficulty"] == "easy":
        return 3, 22000, 16000

    if settings["difficulty"] == "hard":
        return 6, 13000, 9000

    return 4, 18000, 12000


#  GAME RESET 

def reset_game():
    global score, coins_collected, distance, bonus_score, game_saved
    global player, opponent, coin, nitro, shield, repair, slow, background
    global cars, opponents, coins, nitos, shields, repairs, slows
    global powerup_visible, powerup_spawn_time, last_powerup_time
    global current_powerup, active_powerup, active_powerup_end_time
    global slow_show, slow_active, last_slow_time, slow_start_time
    global honk_sound
    global SLOW_SPAWN_DELAY, POWERUP_SPAWN_DELAY

    score = 0
    coins_collected = 0
    distance = 0
    bonus_score = 0
    game_saved = False

    enemy_speed, slow_delay, powerup_delay = get_difficulty_values()

    SLOW_SPAWN_DELAY = slow_delay
    POWERUP_SPAWN_DELAY = powerup_delay

    player = PlayerCar()
    opponent = OpposingCar()
    opponent.speed = enemy_speed

    coin = Coin()

    nitro = Nitro()
    shield = Shield()
    repair = Repair()
    slow = Slow()

    background = BackgroundLoading()

    cars = pygame.sprite.Group()
    cars.add(player)
    cars.add(opponent)

    opponents = pygame.sprite.Group()
    opponents.add(opponent)

    coins = pygame.sprite.Group()
    coins.add(coin)

    nitos = pygame.sprite.Group()
    nitos.add(nitro)

    shields = pygame.sprite.Group()
    shields.add(shield)

    repairs = pygame.sprite.Group()
    repairs.add(repair)

    slows = pygame.sprite.Group()
    slows.add(slow)

    powerup_visible = False
    powerup_spawn_time = 0
    last_powerup_time = pygame.time.get_ticks()

    current_powerup = None
    active_powerup = None
    active_powerup_end_time = 0

    slow_show = False
    slow_active = False
    last_slow_time = pygame.time.get_ticks()
    slow_start_time = 0

    honk_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "crash.wav"))


#  SPAWN FUNCTIONS 

def hide_all_powerups():
    nitro.rect.centery = -2000
    shield.rect.centery = -2000
    repair.rect.centery = -2000


def hide_slow():
    slow.rect.centery = -2000


def respawn_opponent():
    opponent.rect.centery = -75
    opponent.rect.centerx = random.randint(47, 253)

    while abs(opponent.rect.centerx - player.rect.centerx) < 60:
        opponent.rect.centerx = random.randint(47, 253)


def spawn_powerup():
    global current_powerup, powerup_visible, powerup_spawn_time

    hide_all_powerups()

    current_powerup = random.choice(["nitro", "shield", "repair"])

    if current_powerup == "nitro":
        obj = nitro

    elif current_powerup == "shield":
        obj = shield

    else:
        obj = repair

    obj.rect.centery = -20
    obj.rect.centerx = random.randint(47, 253)

    while obj.rect.colliderect(opponent.rect):
        obj.rect.centerx = random.randint(47, 253)

    while abs(obj.rect.centerx - player.rect.centerx) < 60:
        obj.rect.centerx = random.randint(47, 253)

    powerup_visible = True
    powerup_spawn_time = pygame.time.get_ticks()


def spawn_slow():
    global slow_show

    slow.rect.centery = -20
    slow.rect.centerx = random.randint(47, 253)

    while slow.rect.colliderect(opponent.rect):
        slow.rect.centerx = random.randint(47, 253)

    while abs(slow.rect.centerx - player.rect.centerx) < 60:
        slow.rect.centerx = random.randint(47, 253)

    slow_show = True


#  SCORE FUNCTION 

def calculate_score():
    return int(distance) + coins_collected * 10 + bonus_score


#  SCREENS 

def draw_main_menu():
    screen.fill((210, 210, 210))

    title = font_big.render("RACER GAME", True, BLACK)
    screen.blit(title, title.get_rect(center=(150, 90)))

    play_btn = draw_button("Play", 75, 170, 150, 45)
    leaderboard_btn = draw_button("Leaderboard", 50, 235, 200, 45)
    settings_btn = draw_button("Settings", 65, 300, 170, 45)
    quit_btn = draw_button("Quit", 75, 365, 150, 45)

    return play_btn, leaderboard_btn, settings_btn, quit_btn


def draw_username_screen():
    screen.fill((220, 220, 220))

    title = font_big.render("Enter Name", True, BLACK)
    screen.blit(title, title.get_rect(center=(150, 120)))

    box = pygame.Rect(45, 220, 210, 45)
    pygame.draw.rect(screen, WHITE, box, border_radius=8)
    pygame.draw.rect(screen, BLACK, box, 2, border_radius=8)

    name_text = font_medium.render(username, True, BLACK)
    screen.blit(name_text, (box.x + 10, box.y + 12))

    info = font_small.render("Press ENTER to start", True, BLACK)
    screen.blit(info, info.get_rect(center=(150, 300)))


def draw_leaderboard_screen():
    screen.fill((230, 230, 230))

    title = font_big.render("TOP 10", True, BLACK)
    screen.blit(title, title.get_rect(center=(150, 45)))

    data = load_leaderboard()

    y = 95
    for i in range(len(data)):
        entry = data[i]

        line = str(i + 1) + ". " + entry["name"] + " | " + str(entry["score"]) + " | " + str(entry["distance"]) + "m"
        text = font_small.render(line, True, BLACK)
        screen.blit(text, (20, y))

        y += 35

    back_btn = draw_button("Back", 90, 525, 120, 45)

    return back_btn


def draw_settings_screen():
    screen.fill((220, 220, 220))

    title = font_big.render("SETTINGS", True, BLACK)
    screen.blit(title, title.get_rect(center=(150, 50)))

    sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
    sound_btn = draw_button(sound_text, 55, 110, 190, 40)

    color_text = "Car: " + settings["car_color"]
    color_btn = draw_button(color_text, 55, 175, 190, 40)

    difficulty_text = "Difficulty: " + settings["difficulty"]
    difficulty_btn = draw_button(difficulty_text, 45, 240, 210, 40)

    back_btn = draw_button("Back", 90, 520, 120, 45)

    return sound_btn, color_btn, difficulty_btn, back_btn


def draw_game_over_screen():
    screen.fill((180, 80, 80))

    title = font_big.render("GAME OVER", True, WHITE)
    screen.blit(title, title.get_rect(center=(150, 90)))

    draw_text("Name: " + username, font_medium, WHITE, 60, 150)
    draw_text("Score: " + str(score), font_medium, WHITE, 60, 190)
    draw_text("Distance: " + str(int(distance)) + "m", font_medium, WHITE, 60, 230)
    draw_text("Coins: " + str(coins_collected), font_medium, WHITE, 60, 270)

    retry_btn = draw_button("Retry", 75, 360, 150, 45)
    menu_btn = draw_button("Main Menu", 55, 425, 190, 45)

    return retry_btn, menu_btn


#  GAME DRAW AND UPDATE 

def update_game():
    global score, coins_collected, distance, bonus_score
    global powerup_visible, last_powerup_time, active_powerup, active_powerup_end_time
    global current_powerup
    global slow_show, slow_active, last_slow_time, slow_start_time
    global state, game_saved

    now = pygame.time.get_ticks()

    # Distance
    distance += opponent.speed * 0.08
    score = calculate_score()

    # Background
    background.move()
    background.draw()

    # Coin
    coin.move()
    screen.blit(coin.image, coin.rect)

    # Power-up spawn
    if powerup_visible == False and active_powerup is None:
        if now - last_powerup_time >= POWERUP_SPAWN_DELAY:
            spawn_powerup()

    # Power-up move and draw
    if powerup_visible == True:
        if current_powerup == "nitro":
            obj = nitro
        elif current_powerup == "shield":
            obj = shield
        else:
            obj = repair

        obj.move()
        screen.blit(obj.image, obj.rect)

        if obj.rect.centery > 650:
            powerup_visible = False
            last_powerup_time = pygame.time.get_ticks()
            hide_all_powerups()

        if now - powerup_spawn_time >= POWERUP_TIMEOUT:
            powerup_visible = False
            last_powerup_time = pygame.time.get_ticks()
            hide_all_powerups()

    # Slow spawn
    if slow_show == False:
        if now - last_slow_time >= SLOW_SPAWN_DELAY:
            spawn_slow()

    # Slow move and draw
    if slow_show == True:
        slow.move()
        screen.blit(slow.image, slow.rect)

        if slow.rect.centery > 650:
            slow_show = False
            last_slow_time = pygame.time.get_ticks()
            hide_slow()

    # Cars
    screen.blit(player.image, player.rect)
    screen.blit(opponent.image, opponent.rect)

    player.move()
    opponent.move()

    # Collision with enemy
    if pygame.sprite.spritecollideany(player, opponents):
        if active_powerup == "shield":
            active_powerup = None
            bonus_score += 30
            respawn_opponent()

        else:
            if settings["sound"]:
                honk_sound.play()

            if game_saved == False:
                add_to_leaderboard(username, score, distance, coins_collected)
                game_saved = True

            state = GAME_OVER

    # Collision with coin
    if pygame.sprite.spritecollideany(player, coins):
        coins_collected += 1
        bonus_score += 2

        if coins_collected % 10 == 0:
            opponent.speed += 1

        coin.respawn()

    # Collision with slow obstacle
    if slow_show == True and pygame.sprite.spritecollideany(player, slows):
        if active_powerup == "shield":
            active_powerup = None
            bonus_score += 20

        else:
            slow_active = True
            slow_start_time = pygame.time.get_ticks()

        slow_show = False
        last_slow_time = pygame.time.get_ticks()
        hide_slow()

    # Collision with nitro
    if powerup_visible == True and current_powerup == "nitro":
        if pygame.sprite.spritecollideany(player, nitos):
            active_powerup = "nitro"
            active_powerup_end_time = pygame.time.get_ticks() + NITRO_DURATION
            slow_active = False
            bonus_score += 20

            powerup_visible = False
            last_powerup_time = pygame.time.get_ticks()
            hide_all_powerups()

    # Collision with shield
    if powerup_visible == True and current_powerup == "shield":
        if pygame.sprite.spritecollideany(player, shields):
            active_powerup = "shield"
            bonus_score += 30

            powerup_visible = False
            last_powerup_time = pygame.time.get_ticks()
            hide_all_powerups()

    # Collision with repair
    if powerup_visible == True and current_powerup == "repair":
        if pygame.sprite.spritecollideany(player, repairs):
            bonus_score += 50
            respawn_opponent()

            powerup_visible = False
            last_powerup_time = pygame.time.get_ticks()
            hide_all_powerups()

    # Nitro timer
    if active_powerup == "nitro":
        if pygame.time.get_ticks() >= active_powerup_end_time:
            active_powerup = None

    # Slow timer
    if slow_active == True:
        if pygame.time.get_ticks() - slow_start_time >= SLOW_EFFECT_DURATION:
            slow_active = False

    # Speed control
    if active_powerup == "nitro":
        player.speed = 6

    elif slow_active == True:
        player.speed = 1

    else:
        player.speed = 3

    # Finish
    if distance >= FINISH_DISTANCE:
        if game_saved == False:
            add_to_leaderboard(username, score, distance, coins_collected)
            game_saved = True

        state = GAME_OVER

    # UI
    remaining_distance = FINISH_DISTANCE - int(distance)

    if remaining_distance < 0:
        remaining_distance = 0

    draw_text("Score: " + str(score), font_small, BLACK, 10, 10)
    draw_text("Coins: " + str(coins_collected), font_small, BLACK, 10, 35)
    draw_text("Dist: " + str(int(distance)) + "m", font_small, BLACK, 10, 60)
    draw_text("Left: " + str(remaining_distance) + "m", font_small, BLACK, 10, 85)

    if active_powerup == "nitro":
        remaining = (active_powerup_end_time - pygame.time.get_ticks()) // 1000

        if remaining < 0:
            remaining = 0

        draw_text("Nitro: " + str(remaining), font_small, BLUE, 180, 10)

    elif active_powerup == "shield":
        draw_text("Shield: ON", font_small, BLUE, 180, 10)

    elif slow_active == True:
        remaining = (SLOW_EFFECT_DURATION - (pygame.time.get_ticks() - slow_start_time)) // 1000

        if remaining < 0:
            remaining = 0

        draw_text("Slow: " + str(remaining), font_small, RED, 180, 10)


#  MAIN LOOP 

running = True

while running:
    mouse_clicked = False
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True

        if state == USERNAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip() == "":
                        username = "Player"

                    reset_game()
                    state = GAME

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    if len(username) < 12:
                        username += event.unicode

    #  MENU 

    if state == MENU:
        play_btn, leaderboard_btn, settings_btn, quit_btn = draw_main_menu()

        if mouse_clicked:
            if play_btn.collidepoint(mouse_pos):
                username = ""
                state = USERNAME

            elif leaderboard_btn.collidepoint(mouse_pos):
                state = LEADERBOARD

            elif settings_btn.collidepoint(mouse_pos):
                state = SETTINGS

            elif quit_btn.collidepoint(mouse_pos):
                running = False

    #  USERNAME 

    elif state == USERNAME:
        draw_username_screen()

    #  GAME 

    elif state == GAME:
        update_game()

    #  GAME OVER 

    elif state == GAME_OVER:
        retry_btn, menu_btn = draw_game_over_screen()

        if mouse_clicked:
            if retry_btn.collidepoint(mouse_pos):
                reset_game()
                state = GAME

            elif menu_btn.collidepoint(mouse_pos):
                state = MENU

    #  LEADERBOARD 

    elif state == LEADERBOARD:
        back_btn = draw_leaderboard_screen()

        if mouse_clicked:
            if back_btn.collidepoint(mouse_pos):
                state = MENU

    #  SETTINGS 

    elif state == SETTINGS:
        sound_btn, color_btn, difficulty_btn, back_btn = draw_settings_screen()

        if mouse_clicked:
            if sound_btn.collidepoint(mouse_pos):
                settings["sound"] = not settings["sound"]
                save_settings()

            elif color_btn.collidepoint(mouse_pos):
                if settings["car_color"] == "default":
                    settings["car_color"] = "red"

                elif settings["car_color"] == "red":
                    settings["car_color"] = "blue"

                elif settings["car_color"] == "blue":
                    settings["car_color"] = "green"

                else:
                    settings["car_color"] = "default"

                save_settings()

            elif difficulty_btn.collidepoint(mouse_pos):
                if settings["difficulty"] == "easy":
                    settings["difficulty"] = "normal"

                elif settings["difficulty"] == "normal":
                    settings["difficulty"] = "hard"

                else:
                    settings["difficulty"] = "easy"

                save_settings()

            elif back_btn.collidepoint(mouse_pos):
                state = MENU

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()