import pygame
import random

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

# Enemy
enemyImg = pygame.image.load('tiger.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))

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

# TODO enemy moving
    '''# enemy moving 
    if enemyY == 64:
        smallOffset = not smallOffset
    if enemyX == 64:
        smallOffset = not smallOffset

    smallOffset = random.random()
    enemyX = enemyX - smallOffset
    enemyY = enemyY - smallOffset '''


    # if keystroke is pressed check if it's right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX -= 1.5
        if event.key == pygame.K_RIGHT:
            playerX += 1.5
        if event.key == pygame.K_UP:
            playerY -= 1.5
        if event.key == pygame.K_DOWN:
            playerY += 1.5

    # player game zone
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # enemy game zone

    if enemyX <= 0:
        enemyX = 0
    elif enemyX >= 736:
        enemyX = 736

    if enemyY <= 0:
        enemyY = 0
    elif enemyY >= 536:
        enemyY = 536

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
