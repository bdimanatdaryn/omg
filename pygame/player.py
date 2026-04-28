import pygame

pygame.init()
pygame.mixer.init() 

pygame.display.set_caption("Spotify")
playlist = ['blood.mp3','2.mp3']
current = 0
screen = pygame.display.set_mode((600,600))
def play():
    pygame.mixer.music.load(playlist[current])
    pygame.mixer.music.play()

run = True
font = pygame.font.SysFont("Arial",30)
while run:
    screen.fill((30,30,30))
    text1 = font.render("Current: " + playlist[current], True, (255, 255, 255))
    text2 = font.render("P-Play S-Stop N-Next B-Back Q-Quit", True, (200, 200, 200))


    screen.blit(text1, (50, 200))
    screen.blit(text2, (50, 300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play()
            if event.key == pygame.K_s:
                pygame.mixer.music.stop()

            if event.key == pygame.K_n:
                current += 1
                if current >= len(playlist):
                    current = 0
                play()

            if event.key == pygame.K_b:
                current -= 1
                if current < 0:
                    current = len(playlist) - 1
                play()

            if event.key == pygame.K_q:
                run = False

    pygame.display.update()

pygame.quit()