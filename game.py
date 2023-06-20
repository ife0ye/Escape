# necessary extensions
import pygame
import random
import sys

# game initialization 
pygame.init()

# Constant colors used
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)


# game setup
# font setup
font = pygame.font.SysFont(None, 36)

# screen setup
screenBreadth = 500
screenLength = 600
screen = pygame.display.set_mode((screenLength, screenBreadth))
pygame.display.set_caption("ESCAPE")

# user setup
userSize = 30
userSpeed = 3
userLives = 3 
userX = screenLength // 2
userY = screenBreadth // 2

# game clock set up
clock = pygame.time.Clock()

# timer setup
timeLeft = 300
timerStart = False

# trap setup
trapSize = 20
traps = []
numberOfTraps = 75

# randomizing the traps and adding them to array
for x in range(numberOfTraps):
    trapX = random.randint(0, screenLength - trapSize)
    trapY = random.randint(0, screenBreadth - trapSize)
    traps.append([trapX, trapY])

# randomizing the exit route
exitX = random.randint(0, screenLength - userSize)
exitY = random.randint(0, screenBreadth - userSize)

# game functions
# to draw user
def user(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, userSize, userSize))

# to check collisions
def collisionCheck(userX, userY, trapX, trapY):
    if userX + userSize > trapX and userX < trapX + trapSize:
        if userY + userSize > trapY and userY < trapY + trapSize:
            return True
    return False

# to check if player has exited 
def exitCheck(userX, userY, exitX, exitY):
    if userX + userSize > exitX and userX < exitX + userSize:
        if userY + userSize > exitY and userY < exitY + userSize:
            return True
    return False

# to draw timer
def drawTimer():
    timerText = font.render("Time: " + str(timeLeft), True, BLACK)
    screen.blit(timerText, (10, 10))

# to draw traps
def drawTrap(trap):
    pygame.draw.rect(screen, GREY, (trap[0], trap[1], trapSize, trapSize))

# to draw lives
def drawLives():
    livesText = font.render("Lives: " + str(userLives), True, BLACK)
    screen.blit(livesText, (screenLength - 120, 10))
    
# to draw exit sign
def drawExit():
    pygame.draw.rect(screen, GREEN, (exitX, exitY, userSize, userSize))

# The game
gameOn = True
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # to get direction user wants to move
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and userX > 0:
        userX -= userSpeed
    if keys[pygame.K_RIGHT] and userX < screenLength - userSize:
        userX += userSpeed
    if keys[pygame.K_UP] and userY > 0:
        userY -= userSpeed
    if keys[pygame.K_DOWN] and userY < screenBreadth - userSize:
        userY += userSpeed

    # check if user enters trap
    for trap in traps:
        if collisionCheck(userX, userY, trap[0], trap[1]):
            traps.remove(trap)
            userLives -= 1
            if userLives == 0:
                gameOn = False
                break

    # check if player has reached exit
    if exitCheck(userX, userY, exitX, exitY):
        gameOn = False
        break
    
    # refreshing game screen
    screen.fill(WHITE)
    user(userX, userY)
    for trap in traps:
        drawTrap(trap)
    drawTimer()
    drawLives()
    drawExit()
    pygame.display.update()

    # begin the timer
    if not timerStart:
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        timerStart = True

    # update game timer
    if event.type == pygame.USEREVENT:
        timeLeft -= 1
        if timeLeft == 0:
            running = False
            break

    # games frame rate
    clock.tick(60)

# end of game screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(WHITE)
    if timeLeft == 0:
        gameOverDisplay = font.render("Time Up", True, BLACK)
        screen.blit(gameOverDisplay, (screenLength // 2 - 50, screenBreadth // 2 - 50))
    elif userLives == 0:
        gameOverDisplay = font.render("Game Over", True, BLACK)
        screen.blit(gameOverDisplay, (screenLength // 2 - 50, screenBreadth // 2 - 50))
    elif userLives > 0 and userLives < 4:
        gameOverDisplay = font.render("CONGRATULATIONS!, You escaped", True, BLACK)
        screen.blit(gameOverDisplay, (screenLength-500, screenBreadth // 2 - 50))
    pygame.display.update()
