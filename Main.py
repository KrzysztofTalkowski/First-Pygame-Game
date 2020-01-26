import pygame
from pygame import mixer

import random
import math

# Initialize Game
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.jpg').convert()


# background sound
mixer.music.load('b1.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Hungry Dragon")
icon = pygame.image.load('monster.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('dragon.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# 6 Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# explosion picture
explosionImg = pygame.image.load('explosion.png')

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('tiger.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# Fireball
fireballImg = pygame.image.load('hot.png')
fireballX = 0
fireballY = 480
fireballX_change = 0
fireballY_change = 1.5
fireball_state = "ready"

# score text
score_value = 0
font = pygame.font.Font('FakeHope.ttf', 32)
textX = 10
textY = 10

# game over text
game_over_font = pygame.font.Font('FakeHope.ttf', 90)

# play again text
play_again_font = pygame.font.Font('FakeHope.ttf', 130)

# play again loop #TODO replaying after touch on screen or input
# play_again = 1


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over_font.render("Game Over, Score: " + str(score_value), True, (100, 255, 100))
    screen.blit(over_text, (40, 100))


def play_again_text():
    play_again = play_again_font.render("Play Again", True, (255, 0, 0))
    screen.blit(play_again, (115, 300))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def show_explosion(x, y):
    screen.blit(explosionImg, (x, y))


def fire_fireball(x, y):
    global fireball_state
    fireball_state = "fire"
    screen.blit(fireballImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, fireballX, fireballY):
    distance = math.sqrt(math.pow((enemyX - fireballX), 2) + (math.pow(enemyY - fireballY, 2)))
    if distance < 27:
        return True


# Game Loop
running = True
while running:
    # RGB        RED  GREEN  BLUE
    # screen.fill((110, 200, 100))  //fill screen (color)
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed check if it's right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -1
        if event.key == pygame.K_RIGHT:
            playerX_change = 1
        if event.key == pygame.K_UP:
            playerY_change = -1
        if event.key == pygame.K_DOWN:
            playerY_change = 1
        if event.key == pygame.K_SPACE:
            if fireball_state is "ready":
                fireball_sound = mixer.Sound('dragon.wav')
                fireball_sound.play()
                fireballX = playerX
                fireballY = playerY
                fire_fireball(fireballX, fireballY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            playerY_change = 0
    # player game zone

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 460:  # usually 460 - for tests less
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            play_again_text()

            ''''while play_again:   #TODO exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                    elif event.key == pygame.K_n:
                        pygame.quit()'''

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision fireball + enemy
        collision = isCollision(enemyX[i], enemyY[i], fireballX, fireballY)
        if collision:
            explosion_sound = mixer.Sound('explo.wav')
            explosion_sound.play()
            show_explosion(enemyX[i], enemyY[i])  #TODO works sometimes and really short
            fireballY = 480
            fireball_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # enemy game zone
    if enemyX[i] <= 0:
        enemyX[i] = 0
    elif enemyX[i] >= 736:
        enemyX[i] = 736

    if enemyY[i] <= 0:
        enemyY[i] = 0
    elif enemyY[i] >= 536:
        enemyY[i] = 536

    # fireball movement
    if fireballY <= 0:
        fireballY = 480
        fireball_state = "ready"

    if fireball_state is "fire":
        fire_fireball(fireballX, fireballY)
        fireballY -= fireballY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
