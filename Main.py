import pygame
from pygame import mixer

import random
import math

# TODO
# [X]  1. Different music on game over
# [X] 2. Explosion image is not always working correctly
# [ ] 3. Change movements of enemies (to make it random) added ghosts, but they aren't moving randomly..
# [ ] 4. Enemies should 'drop' candies(?)
# [ ] 5. Upgrade of dragon after x score
# [X] 6. Upgrade of enemies after x (speed increased with score)
# [ ] 7. Replay button or y/n
# [X] 8. Mute music Keys  P/O
# [ ] 9. High scores (would be awesome)
# [X] 10. Accuracy of shooting on screen.   # just have to repair %
# [ ] 11. Game over when enemy touches player (only when player can walk freely)
# [ ] 12. Number of enemies should increase with time or score
# [ ] 13. Convert everything into OOP


# Initialize Game
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.jpg').convert()

# background sound
mixer.music.load('b1.mp3')
mixer.music.play(-1)

# Sound Button
sound_on = pygame.image.load('ON.png')
sound_off = pygame.image.load('OFF.png')
soundX = 760
soundY = 10
pause = False

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

# score text
score_value = 0
font = pygame.font.Font('FakeHope.ttf', 32)
textX = 10
textY = 10

# 6 Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 1

# Ghost
'''ghostImg = pygame.image.load('ghost.png')
ghostX = 200
ghostY = 200
ghostX_change = 1
ghostY_change = 1
ghost_num = 1
'''

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('tiger.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(20)

# explosion picture
explosionImg = pygame.image.load('explosion.png')

# Fireball
fireballImg = pygame.image.load('hot.png')
fireballX = 0
fireballY = 480
fireballX_change = 0
fireballY_change = 1.5
fireball_state = "ready"

# game over text
game_over_font = pygame.font.Font('FakeHope.ttf', 90)

# play again text
play_again_font = pygame.font.Font('FakeHope.ttf', 130)

# run once
run_once = 0

# Accuracy of shooting
kills = 0
shoots = 0
targetImg = pygame.image.load('target.png')
targetImgX = 615
targetImgY = 8
targetX = 660
targetY = 10
percentX = 705
percentY = 10


def show_target_img(x, y):
    screen.blit(targetImg, (x, y))


def show_target(x, y, x1, y1):
    if kills == 0:
        val = 0
    else:
        val = (kills / (shoots + kills)) * 100
    target = font.render(str(round(val)), True, (255, 255, 255))
    percent = font.render(str('%'), True, (255, 255, 255))  # repair %
    screen.blit(target, (x, y))
    screen.blit(percent, (x1, y1))


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


def enemy(x, y, num):
    screen.blit(enemyImg[num], (x, y))


'''def ghost(x, y):
    screen.blit(ghostImg, (x, y))'''


def show_explosion(x, y):
    screen.blit(explosionImg, (x, y))


def fire_fireball(x, y):
    global fireball_state
    fireball_state = "fire"
    screen.blit(fireballImg, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, fireball_x, fireball_y):
    distance = math.sqrt(math.pow((enemy_x - fireball_x), 2) + (math.pow(enemy_y - fireball_y, 2)))
    if distance < 27:
        return True


def sound_off_button(x, y):
    screen.blit(sound_off, (x, y))


def sound_on_button(x, y):
    screen.blit(sound_on, (x, y))


def paused():
    pygame.mixer.music.pause()


def stop_music():
    pygame.mixer.music.stop()


def un_pause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


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

        # music pause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = True
                paused()
            if event.key == pygame.K_o:
                pause = False
                un_pause()

        # Moving player Left/Right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            '''if event.key == pygame.K_UP:    # Moving up and down
                playerY_change = -1
            if event.key == pygame.K_DOWN:
                playerY_change = 1'''
            # Shooting with space bar
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

    '''playerY += playerY_change  # unnecessary without moving up/down
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536'''

    # Enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 450:  # usually 460 - for tests les
            while run_once == 0:
                stop_music()
                run_once = 1
                mixer.music.load('ENDGAME.mp3')
                mixer.music.play(-1)
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
        if score_value <= 1:
            if enemyX[i] <= 0:
                enemyX_change[i] = 1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1
                enemyY[i] += enemyY_change[i]
        if score_value <= 2:
            if enemyX[i] <= 0:
                enemyX_change[i] = 1.05
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1.05
                enemyY[i] += enemyY_change[i]
        elif score_value <= 3:
            if enemyX[i] <= 0:
                enemyX_change[i] = 1.1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1.1
                enemyY[i] += enemyY_change[i]
        elif score_value <= 4:
            if enemyX[i] <= 0:
                enemyX_change[i] = 1.15
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1.15
                enemyY[i] += enemyY_change[i]
        elif score_value >= 5:
            if enemyX[i] <= 0:
                enemyX_change[i] = 1.20
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1.20
                enemyY[i] += enemyY_change[i]

        # Collision fireball + enemy
        collision = is_collision(enemyX[i], enemyY[i], fireballX, fireballY)
        if collision:
            show_explosion(enemyX[i], enemyY[i])  # TODO too short
            explosion_sound = mixer.Sound('explo.wav')
            explosion_sound.play()
            fireballY = 480
            fireball_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            kills += 1

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

    '''ghost(ghostX, ghostY)
    # GHOST GAME ZONE
    if ghostX <= 0:
        ghostX = 0
    elif ghostX >= 736:
        ghostX = 736

    if ghostY <= 0:
        ghostY = 0
    elif ghostY >= 536:
        ghostY = 536

    # GHOST MOVEMENT
    if score_value <= 1:
        if ghostX <= 0:
            ghostX_change = random.randint(0.2, 0.2)
            enemyY += ghostY_change
        elif ghostX >= 736:
            ghostX_change = random.randint(0.2, 0.2)
            ghostY += ghostY_change

    ghostX += ghostX_change
    ghostY += ghostY_change'''

    # fireball movement
    if fireballY <= 0:
        fireballY = 480
        fireball_state = "ready"
        shoots += 1

    if fireball_state is "fire":
        fire_fireball(fireballX, fireballY)
        fireballY -= fireballY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_target(targetX, targetY, percentX, percentY)
    show_target_img(targetImgX, targetImgY)
    '''ghost(200, 200)'''

    # music buttons on screen
    if pause is False:
        sound_on_button(soundX, soundY)
    elif pause is True:
        sound_off_button(soundX, soundY)

    pygame.display.update()
