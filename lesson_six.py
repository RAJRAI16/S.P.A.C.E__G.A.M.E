import math
import random

from pygame.locals import *
import pygame
from pygame import mixer


pygame.init()


screen = pygame.display.set_mode((800, 600))


background = pygame.image.load('background.png')


mixer.music.load("background.wav")



pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10


playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))


enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))



bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def set_background():
    global background
    
    screen.fill((0, 0, 0))

    
    screen.blit(background, (0, 0))

def move_bullet():
    global bulletX, bulletY, bullet_state
    
    if bulletY <= 1:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change    

def game_input():
    global running, playerX_change, bulletX, playerX, bulletY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

def enemy_movement():
    global enemyX, enemyX_change, enemyY, enemyY_change
    
    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
 
        enemy(enemyX[i], enemyY[i], i)
 
def game_over():
    global running
    running = False  

    
    game_over_font = pygame.font.Font('freesansbold.ttf', 64)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (200, 250))

    # Display final score
    final_score_text = font.render(f"Final Score: {score_value}", True, (255, 255, 255))
    screen.blit(final_score_text, (280, 320))

    pygame.display.update()  

    
    pygame.time.delay(3000)  
    pygame.quit()  
    exit()  


def collision():
    global num_of_enemies, enemyX, enemyY, bulletX, bulletY, bullet_state, score_value

    for i in range(num_of_enemies):
        
        player_hit = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if player_hit:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            game_over()  
            return  

        
        bullet_hit = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if bullet_hit:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1  

            
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

running = True
while running:
    set_background()
    game_input() 
    enemy_movement()
    collision()
    move_bullet()
    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
