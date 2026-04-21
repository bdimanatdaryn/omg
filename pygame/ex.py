import pygame
from pygame.locals import *
import random

pygame.init()

screen = pygame.display.set_mode((300,600))
clock = pygame.time.Clock()
# Class of coin
class Coin(pygame.sprite.Sprite):
    def __init__(self, path="coin.png"):
        super().__init__()
        imported_image = pygame.image.load(path)
        self.image = pygame.transform.scale(imported_image,(40,40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47,253), -20)
        self.speed = 3

    def move(self):
        self.rect.centery += self.speed

        if self.rect.centery > 650:
            self.rect.centery = -20
            self.rect.centerx = random.randint(47,253)
# Class of Player car
class player_car(pygame.sprite.Sprite):
    def __init__(self,path="Player.png"):
        super().__init__()
        imported_image = pygame.image.load(path)
        self.image = pygame.transform.scale(imported_image,(75,150))
        self.rect = self.image.get_rect()
        self.rect.center = (47,525)

    def move(self):
        button = pygame.key.get_pressed()

        if button[K_LEFT]:
            self.rect.centerx -= 3
        elif button[K_RIGHT]:
            self.rect.centerx += 3
        # boundary condition for the position of the car
        if self.rect.centerx < 47:
            self.rect.centerx = 47
        if self.rect.centerx > 253:
            self.rect.centerx = 253

    
# Class of opposing car

class opposing_car(pygame.sprite.Sprite):
    def __init__(self,path = "Enemy.png"):
        super().__init__()
        imported_image = pygame.image.load(path)
        self.image = pygame.transform.scale(imported_image,(70,150))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(47,253),75)
        self.speed = 5
        self.score = 0
    
    def move(self):
        self.rect.centery += self.speed

        if self.rect.centery > 675:
            self.rect.centery = -75
            self.rect.centerx = random.randint(47,253)
            self.score += 10
# background
class background_loading:
    def __init__(self, path = "road.png"):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image,(300,300))
        rect1 = self.image.get_rect()
        rect2 = self.image.get_rect()
        rect2.centery += 300
        rect3 = self.image.get_rect()
        rect3.centery += 600
        self.rectangles = []
        self.rectangles.append(rect1)
        self.rectangles.append(rect2)
        self.rectangles.append(rect3)
        
    
    def draw(self):
        for rectangle in self.rectangles:
            screen.blit(self.image,rectangle)
    
    def move(self):
        for rectangle in self.rectangles:
            rectangle.centery+=2
            if rectangle.centery>750:
                rectangle.centery = -150


score = 0

player = player_car() # creating player
opponent = opposing_car() # creating enemy
coin = Coin() # creating coins

# groups of sprites 

cars = pygame.sprite.Group()
cars.add(player)
cars.add(opponent)

opponents = pygame.sprite.Group()
opponents.add(opponent)


coins = pygame.sprite.Group() 
coins.add(coin)

# sound for crash

honk_sound = pygame.mixer.Sound("crash.wav")

running = True



background = background_loading()

# the main Loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    background.move()
    background.draw()
    coin.move()
    screen.blit(coin.image, coin.rect)
    

    for car in cars:
        screen.blit(car.image,car.rect)
        car.move()

    # COLLISION WITH ENEMY (GAME OVER)
    if pygame.sprite.spritecollideany(player,opponents):
        screen.fill((125,50,50))
        font = pygame.font.SysFont("open dyslexic",18)
        text = font.render("Your final score is: " + str(opponent.score),True,(0,255,255))
        rect = text.get_rect()
        rect.center = (150,300)
        honk_sound.play()
        screen.blit(text,rect)
        pygame.display.update()
        pygame.time.delay(2000)
        running = False
    # COLLISION WITH COIN 
    if pygame.sprite.spritecollideany(player,coins):
        score += 1
        coin.rect.centery = -20
        coin.rect.centerx = random.randint(47,253)
    # the text for Coins
    font = pygame.font.SysFont(None, 30)
    text = font.render("Coins: " + str(score), True, (0,0,0))
    screen.blit(text, (200,10))

    clock.tick(60)
    pygame.display.flip()
 