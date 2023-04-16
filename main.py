import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1024, 623))

# background
backGroundImg = pygame.image.load("backGround.png")
mixer.music.load('bgSound.wav')
mixer.music.play(-1)
pygame.display.set_caption("Space Invader")
# Icon
icon = pygame.image.load("Game Icon.png")
pygame.display.set_icon(icon)
# Player
playerImg = pygame.image.load("Game Character.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(1.2)
    enemyY_change.append(40)
# Bullet
BulletImg = pygame.image.load("Bullet.png")
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 2
Bullet_State = "ready"

# Font
score_value = 0
current_score = 0
High_score= 0
font = pygame.font.Font('freesansbold.ttf', 30)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

game_over = False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
def showHighScore(x,y):
    score = font.render("Your Highest Score: " + str(High_score), True, (0, 255, 0))
    screen.blit(score, (x, y))
def showCurrentScore(x,y):
    score = font.render("Previous Score: " + str(current_score), True, (0, 255, 0))
    screen.blit(score, (x, y))

def game_over_text(x, y):
    global game_over
    display_game_over = over_font.render("Game Over ", True, (255, 0, 0))
    screen.blit(display_game_over, (x, y))
    game_over = True


def restartText(x, y):
    display_restart = font.render("Press 'R' to restart ", True, (255, 255, 255))
    screen.blit(display_restart, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global Bullet_State
    Bullet_State = "fire"
    screen.blit(BulletImg, (x + 22, y + 25))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def background():
    screen.blit(backGroundImg, (0, 0))


running = True
while running:
    # RGB ---_->Red,Green,blue
    screen.fill((195, 195, 195))
    background()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                playerX_change = -1.5
            if event.key == pygame.K_SPACE:
                if Bullet_State == "ready":
                    BulletX = playerX
                    fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                playerX_change = 0
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_r and game_over is True:
                for m in range(num_of_enemies):
                    enemyY[m] = random.randint(50, 200)
                    enemyX[m] = random.randint(0, 800)
                    score_value = 0
                    game_over = False
    playerX += playerX_change
    if playerX <= -4:
        playerX = -4
    elif playerX >= 964:
        playerX = 964

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(330, 50)
            showCurrentScore(365,200)
            showHighScore(365,250)
            restartText(370, 550)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= -4:
            enemyX_change[i] = 0.7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 962:
            enemyX_change[i] = -0.7
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
            explosion_sound = mixer.Sound('badexplosionSound.wav')
            explosion_sound.play()
            BulletY = 480
            Bullet_State = "ready"
            score_value += 1
            current_score = score_value
            if score_value > High_score:
                High_score = score_value
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 200)
        enemy(enemyX[i], enemyY[i], i)

    if BulletY <= -2:
        BulletY = 480
        Bullet_State = "ready"
    if Bullet_State == "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
