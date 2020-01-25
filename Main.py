import pygame
import random
import math

# Initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.jpg')

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

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('tiger.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Fireball
fireballImg = pygame.image.load('hot.png')
fireballX = 0
fireballY = 480
fireballX_change = 0
fireballY_change = 4
fireball_state = "ready"

# score

score_value = 0
font = pygame.font.Font('FakeHope.ttf', 32)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


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
    screen.fill((110, 200, 100))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed check if it's right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5
        if event.key == pygame.K_UP:
            playerY_change = -5
        if event.key == pygame.K_DOWN:
            playerY_change = 5
        if event.key == pygame.K_SPACE:
            if fireball_state is "ready":
                fireballX = playerX
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
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], fireballX, fireballY)
        if collision:
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
