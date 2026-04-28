import pygame
from pygame.locals import *
import random

pygame.init()

screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Racer Game")

clock = pygame.time.Clock()

# ---------------- POWER-UP SETTINGS ----------------

POWERUP_SPAWN_DELAY = 12000   # every 12 seconds new power-up can appear
POWERUP_TIMEOUT = 7000        # power-up disappears after 7 seconds
NITRO_DURATION = 5000         # nitro works for 5 seconds

powerup_visible = False
powerup_spawn_time = 0
last_powerup_time = pygame.time.get_ticks()

current_powerup = None        # "nitro", "shield", "repair"
active_powerup = None         # None, "nitro", "shield"
active_powerup_end_time = 0

# ---------------- SLOW OBSTACLE SETTINGS ----------------

SLOW_SPAWN_DELAY = 18000      # slow appears every 18 seconds
SLOW_EFFECT_DURATION = 3000   # slow effect works 3 seconds

slow_show = False
slow_active = False

last_slow_time = pygame.time.get_ticks()
slow_start_time = 0


# ---------------- CLASS OF NITRO ----------------

class Nitro(pygame.sprite.Sprite):
    def __init__(self, path="nitro.png"):
        super().__init__()
        imported_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(imported_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47, 253), -2000)
        self.speed = 5

    def move(self):
        self.rect.centery += self.speed


# ---------------- CLASS OF SHIELD ----------------

class Shield(pygame.sprite.Sprite):
    def __init__(self, path="shield.png"):
        super().__init__()
        imported_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(imported_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47, 253), -2000)
        self.speed = 5

    def move(self):
        self.rect.centery += self.speed


# ---------------- CLASS OF REPAIR ----------------

class Repair(pygame.sprite.Sprite):
    def __init__(self, path="repair.png"):
        super().__init__()
        imported_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(imported_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47, 253), -2000)
        self.speed = 5

    def move(self):
        self.rect.centery += self.speed


# ---------------- CLASS OF SLOW OBSTACLE ----------------

class Slow(pygame.sprite.Sprite):
    def __init__(self, path="slow.png"):
        super().__init__()
        imported_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(imported_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47, 253), -2000)
        self.speed = 5

    def move(self):
        self.rect.centery += self.speed


# ---------------- CLASS OF COIN ----------------

class Coin(pygame.sprite.Sprite):
    def __init__(self, path="coin.png"):
        super().__init__()
        imported_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(imported_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47, 253), -20)
        self.speed = 3

    def move(self):
        self.rect.centery += self.speed

        if self.rect.centery > 650:
            self.rect.centery = -20
            self.rect.centerx = random.randint(47, 253)


# ---------------- CLASS OF PLAYER CAR ----------------

class player_car(pygame.sprite.Sprite):
    def __init__(self, path="Player.png"):
        super().__init__()
        imported_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(imported_image, (75, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (150, 525)
        self.speed = 3

    def move(self):
        button = pygame.key.get_pressed()

        if button[K_LEFT]:
            self.rect.centerx -= self.speed

        elif button[K_RIGHT]:
            self.rect.centerx += self.speed

        if self.rect.centerx < 47:
            self.rect.centerx = 47

        if self.rect.centerx > 253:
            self.rect.centerx = 253


# ---------------- CLASS OF OPPOSING CAR ----------------

class opposing_car(pygame.sprite.Sprite):
    def __init__(self, path="Enemy.png"):
        super().__init__()
        imported_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(imported_image, (70, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47, 253), 75)
        self.speed = 4
        self.score = 0

    def move(self):
        self.rect.centery += self.speed

        if self.rect.centery > 675:
            self.rect.centery = -75
            self.rect.centerx = random.randint(47, 253)
            self.score += 10


# ---------------- BACKGROUND ----------------

class background_loading:
    def __init__(self, path="road.png"):
        self.image = pygame.image.load(path).convert()
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


# ---------------- CREATE OBJECTS ----------------

score = 0

player = player_car()
opponent = opposing_car()
coin = Coin()

nitro = Nitro()
shield = Shield()
repair = Repair()
slow = Slow()

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

background = background_loading()

honk_sound = pygame.mixer.Sound("crash.wav")


# ---------------- FUNCTIONS ----------------

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
    global current_powerup
    global powerup_visible
    global powerup_spawn_time

    hide_all_powerups()

    current_powerup = random.choice(["nitro", "shield", "repair"])

    if current_powerup == "nitro":
        nitro.rect.centery = -20
        nitro.rect.centerx = random.randint(47, 253)

        while nitro.rect.colliderect(opponent.rect):
            nitro.rect.centerx = random.randint(47, 253)

    elif current_powerup == "shield":
        shield.rect.centery = -20
        shield.rect.centerx = random.randint(47, 253)

        while shield.rect.colliderect(opponent.rect):
            shield.rect.centerx = random.randint(47, 253)

    elif current_powerup == "repair":
        repair.rect.centery = -20
        repair.rect.centerx = random.randint(47, 253)

        while repair.rect.colliderect(opponent.rect):
            repair.rect.centerx = random.randint(47, 253)

    powerup_visible = True
    powerup_spawn_time = pygame.time.get_ticks()


def spawn_slow():
    global slow_show

    slow.rect.centery = -20
    slow.rect.centerx = random.randint(47, 253)

    # Slow should not spawn inside enemy car
    while slow.rect.colliderect(opponent.rect):
        slow.rect.centerx = random.randint(47, 253)

    # Slow should not spawn directly above player
    while abs(slow.rect.centerx - player.rect.centerx) < 60:
        slow.rect.centerx = random.randint(47, 253)

    slow_show = True


# ---------------- MAIN LOOP ----------------

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks()

    # ---------------- BACKGROUND ----------------

    background.move()
    background.draw()

    # ---------------- COIN ----------------

    coin.move()
    screen.blit(coin.image, coin.rect)

    # ---------------- POWER-UP SPAWN ----------------

    if powerup_visible == False and active_powerup is None:
        if now - last_powerup_time >= POWERUP_SPAWN_DELAY:
            spawn_powerup()

    # ---------------- POWER-UP MOVE AND DRAW ----------------

    if powerup_visible == True:

        if current_powerup == "nitro":
            nitro.move()
            screen.blit(nitro.image, nitro.rect)

            if nitro.rect.centery > 650:
                powerup_visible = False
                last_powerup_time = pygame.time.get_ticks()
                hide_all_powerups()

        elif current_powerup == "shield":
            shield.move()
            screen.blit(shield.image, shield.rect)

            if shield.rect.centery > 650:
                powerup_visible = False
                last_powerup_time = pygame.time.get_ticks()
                hide_all_powerups()

        elif current_powerup == "repair":
            repair.move()
            screen.blit(repair.image, repair.rect)

            if repair.rect.centery > 650:
                powerup_visible = False
                last_powerup_time = pygame.time.get_ticks()
                hide_all_powerups()

        # Power-up disappears if player does not collect it in time
        if now - powerup_spawn_time >= POWERUP_TIMEOUT:
            powerup_visible = False
            last_powerup_time = pygame.time.get_ticks()
            hide_all_powerups()

    # ---------------- SLOW OBSTACLE SPAWN ----------------

    if slow_show == False:
        if now - last_slow_time >= SLOW_SPAWN_DELAY:
            spawn_slow()

    # ---------------- SLOW OBSTACLE MOVE AND DRAW ----------------

    if slow_show == True:
        slow.move()
        screen.blit(slow.image, slow.rect)

        if slow.rect.centery > 650:
            slow_show = False
            last_slow_time = pygame.time.get_ticks()
            hide_slow()

    # ---------------- CARS ----------------

    for car in cars:
        screen.blit(car.image, car.rect)
        car.move()

    # ---------------- COLLISION WITH ENEMY ----------------

    if pygame.sprite.spritecollideany(player, opponents):

        # Shield protects from one collision
        if active_powerup == "shield":
            active_powerup = None
            respawn_opponent()

        else:
            screen.fill((125, 50, 50))

            font = pygame.font.SysFont("open dyslexic", 18)
            text = font.render("Your final score is: " + str(opponent.score), True, (0, 255, 255))
            rect = text.get_rect()
            rect.center = (150, 300)

            honk_sound.play()
            screen.blit(text, rect)

            pygame.display.update()
            pygame.time.delay(2000)

            running = False

    # ---------------- COLLISION WITH COIN ----------------

    if pygame.sprite.spritecollideany(player, coins):
        score += 1

        if score % 10 == 0:
            opponent.speed += 1

        coin.rect.centery = -20
        coin.rect.centerx = random.randint(47, 253)

    # ---------------- COLLISION WITH SLOW OBSTACLE ----------------

    if slow_show == True and pygame.sprite.spritecollideany(player, slows):

        # Shield protects from slow obstacle
        if active_powerup == "shield":
            active_powerup = None

        else:
            slow_active = True
            slow_start_time = pygame.time.get_ticks()

        slow_show = False
        last_slow_time = pygame.time.get_ticks()
        hide_slow()

    # ---------------- COLLISION WITH NITRO ----------------

    if powerup_visible == True and current_powerup == "nitro":
        if pygame.sprite.spritecollideany(player, nitos):
            active_powerup = "nitro"
            active_powerup_end_time = pygame.time.get_ticks() + NITRO_DURATION

            slow_active = False

            powerup_visible = False
            last_powerup_time = pygame.time.get_ticks()
            hide_all_powerups()

    # ---------------- COLLISION WITH SHIELD ----------------

    if powerup_visible == True and current_powerup == "shield":
        if pygame.sprite.spritecollideany(player, shields):
            active_powerup = "shield"

            powerup_visible = False
            last_powerup_time = pygame.time.get_ticks()
            hide_all_powerups()

    # ---------------- COLLISION WITH REPAIR ----------------

    if powerup_visible == True and current_powerup == "repair":
        if pygame.sprite.spritecollideany(player, repairs):

            # Repair works instantly: clears enemy from road
            respawn_opponent()

            powerup_visible = False
            last_powerup_time = pygame.time.get_ticks()
            hide_all_powerups()

    # ---------------- ACTIVE POWER-UP TIMER ----------------

    if active_powerup == "nitro":
        if pygame.time.get_ticks() >= active_powerup_end_time:
            active_powerup = None

    # ---------------- SLOW EFFECT TIMER ----------------

    if slow_active == True:
        if pygame.time.get_ticks() - slow_start_time >= SLOW_EFFECT_DURATION:
            slow_active = False

    # ---------------- SPEED CONTROL ----------------

    if active_powerup == "nitro":
        player.speed = 6

    elif slow_active == True:
        player.speed = 1

    else:
        player.speed = 3

    # ---------------- TEXT ----------------

    font = pygame.font.SysFont(None, 30)

    text = font.render("Coins: " + str(score), True, (0, 0, 0))
    screen.blit(text, (190, 10))

    if active_powerup == "nitro":
        remaining = (active_powerup_end_time - pygame.time.get_ticks()) // 1000

        if remaining < 0:
            remaining = 0

        power_text = font.render("Nitro: " + str(remaining), True, (0, 0, 255))
        screen.blit(power_text, (10, 10))

    elif active_powerup == "shield":
        power_text = font.render("Shield: ON", True, (0, 150, 255))
        screen.blit(power_text, (10, 10))

    elif slow_active == True:
        remaining = (SLOW_EFFECT_DURATION - (pygame.time.get_ticks() - slow_start_time)) // 1000

        if remaining < 0:
            remaining = 0

        power_text = font.render("Slow: " + str(remaining), True, (255, 0, 0))
        screen.blit(power_text, (10, 10))

    else:
        power_text = font.render("Power: None", True, (0, 0, 0))
        screen.blit(power_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()