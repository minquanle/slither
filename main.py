import pygame
from time import sleep
from random import randint

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước cửa sổ game
screen_height = 1000
screen_width = 1000

# color
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# string
font_small = pygame.font.SysFont('sans', 20)
font_big = pygame.font.SysFont('sans', 50)
score = 0

pausing = False

# game screen
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption('Snake')
running = True

# snake
snakes = [[5, 6]]

# direction
direction = "right"

# apple
apple = [randint(0, 19),randint(0, 19)]


clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.fill(black)
    def game_over_scene() :
        game_over_txt = font_big.render("Game Over, Your Score: " + str(score), True, white)
        space_txt = font_big.render("Press Space to try again", True, white)
        screen.blit(game_over_txt, (300,160))
        screen.blit(space_txt, (320, 230))

    # tail
    tail_x = snakes[0][0]
    tail_y = snakes[0][1]

    # draw grid
    for i in range(21):
        pygame.draw.line(screen, white, (200, i * 30 + 300), (800, i * 30 + 300))
        pygame.draw.line(screen, white, (i * 30 + 200, 300), (i * 30 + 200, 900))
    
    # draw snake
    for snake in snakes:
        pygame.draw.rect(screen, green, (200 + snake[0] * 30, 300 + snake[1] * 30, 30, 30))

    # draw apple
    pygame.draw.rect(screen, red, (200 + apple[0] * 30, 300 + apple[1] * 30, 30, 30))

    # moving
    if pausing == False:
        if direction == "right" :
            snakes.append([snakes[-1][0] + 1, snakes[-1][1]])
            snakes.pop(0) 
        if direction == "left" :
            snakes.append([snakes[-1][0] - 1, snakes[-1][1]])
            snakes.pop(0) 
        if direction == "up" :
            snakes.append([snakes[-1][0], snakes[-1][1] - 1])
            snakes.pop(0) 
        if direction == "down" :
            snakes.append([snakes[-1][0], snakes[-1][1] + 1])
            snakes.pop(0) 
    
    sleep(0.07)

    # eat
    if apple[0] == snakes[-1][0] and apple[1] == snakes[-1][1] :
        apple = [randint(0, 19),randint(0, 19)]
        snakes.insert(0, [tail_x, tail_y])
        score += 1
    
    # handle hit the boarder
    if snakes[-1][0] > 19 or snakes[-1][1] > 19 or snakes[-1][0] < 0 or snakes[-1][1] < 0 :
        pausing = True
        game_over_scene()
    
    #handle hit body
    for index in range(len(snakes) - 1) :
        if snakes[-1][0] == snakes[index][0] and snakes[-1][1] == snakes[index][1] :
            pausing = True
            game_over_scene()

    # score
    score_txt = font_small.render("Your Score: " + str(score), True, white)
    screen.blit(score_txt, (830, 400))

    # handle keydown
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "down":
                direction = "up"
            if event.key == pygame.K_DOWN and direction != "up":
                direction = "down"
            if event.key == pygame.K_LEFT and direction != "right":
                direction = "left"
            if event.key == pygame.K_RIGHT and direction != "left":
                direction = "right"
            if event.key == pygame.K_SPACE and pausing == True:
                pausing = False
                snakes = [[5, 6]]
                apple = [randint(0, 19),randint(0, 19)]
                score = 0
                direction = "right"

    pygame.display.flip()

pygame.quit()