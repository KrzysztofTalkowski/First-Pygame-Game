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

# Enemy
enemyImg = pygame.image.load('tiger.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 3
enemyY_change = 40

# Fireball
fireballImg = pygame.image.load('hot.png')
fireballX = 0
fireballY = 480
fireballX_change = 0
fireballY_change = 4
fireball_state = "ready"

score = 0

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


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
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 3
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -3
        enemyY += enemyY_change

    # enemy game zone
    if enemyX <= 0:
        enemyX = 0
    elif enemyX >= 736:
        enemyX = 736

    if enemyY <= 0:
        enemyY = 0
    elif enemyY >= 536:
        enemyY = 536

    # fireball movement
    if fireballY <= 0:
        fireballY = 480
        fireball_state = "ready"

    if fireball_state is "fire":
        fire_fireball(fireballX, fireballY)
        fireballY -= fireballY_change

    # Collision
    collision = isCollision(enemyX, enemyY, fireballX, fireballY)
    if collision:
        fireballY = 480
        fireball_state = "ready"
        score += 1
        print(score)
        enemyX = random.randint(0, 800)
        enemyY = random.randint(50, 150)

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
