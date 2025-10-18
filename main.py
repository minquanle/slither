import pygame
from time import sleep
from random import randint

# color
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)

class Snake:
    # initial
    def __init__(self, x, y, color, key_up, key_down, key_left, key_right, direction):
        self.body = [[x, y]]
        self.color = color
        self.alive = True
        self.score = 0
        self.direction = direction

        # tail
        self.tail_x = self.body[0][0]
        self.tail_y = self.body[0][1]
         
        # control
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right

    # draw
    def draw_snake(self, screen):
        for snake in self.body:
            pygame.draw.rect(screen, self.color, (200 + snake[0] * 30, 300 + snake[1] * 30, 30, 30))

    # handle keydown
    def handel_input(self, event) :
        if event.type == pygame.KEYDOWN:
            if event.key == self.key_up and self.direction != "down":
                self.direction = "up"
            if event.key == self.key_down and self.direction != "up":
                self.direction = "down"
            if event.key == self.key_left and self.direction != "right":
                self.direction = "left"
            if event.key == self.key_right and self.direction != "left":
                self.direction = "right"

    # move
    def moving (self) :
        if self.alive :
            if self.direction == "right" :
                self.body.append([self.body[-1][0] + 1, self.body[-1][1]])
                self.body.pop(0) 
            if self.direction == "left" :
                self.body.append([self.body[-1][0] - 1, self.body[-1][1]])
                self.body.pop(0) 
            if self.direction == "up" :
                self.body.append([self.body[-1][0], self.body[-1][1] - 1])
                self.body.pop(0) 
            if self.direction == "down" :
                self.body.append([self.body[-1][0], self.body[-1][1] + 1])
                self.body.pop(0)

    # grow
    def grow(self) :
        self.body.insert(0, [self.tail_x, self.tail_y])
        self.score += 1
    
    # collision
    def check_collision (self, other) :
        # hit other body
        for index in range(len(other.body)) :
            if self.body[-1][0] == other.body[index][0] and self.body[-1][1] == other.body[index][1] :
                self.alive = False

        # hit border
        if self.body[-1][0] > 19 or self.body[-1][1] > 19 or self.body[-1][0] < 0 or self.body[-1][1] < 0 :
            self.alive = False
    

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước cửa sổ game
screen_height = 1000
screen_width = 1000

# string
font_small = pygame.font.SysFont('sans', 20)
font_big = pygame.font.SysFont('sans', 50)
game_over_mess = ""
score = 0

# game screen
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption('Slither')
running = True
game_over = False
clock = pygame.time.Clock()

# game objects
def start_game():
    global player1, player2, apple, game_over, game_over_mess, snakes_list
    game_over = False
    player1 = Snake(5, 6, green, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, "right")
    player2 = Snake(15, 6, purple, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, "left")

    # apple
    apple = [randint(0, 19),randint(0, 19)]
    game_over = False
    game_over_mess = ""
    snakes_list = [player1, player2]

start_game()


while running:
    # snake'sspeed
    clock.tick(5)

    # background's color
    screen.fill(black)

    # draw grid
    for i in range(21):
        pygame.draw.line(screen, white, (200, i * 30 + 300), (800, i * 30 + 300))
        pygame.draw.line(screen, white, (i * 30 + 200, 300), (i * 30 + 200, 900))
    
    # draw apple
    pygame.draw.rect(screen, red, (200 + apple[0] * 30, 300 + apple[1] * 30, 30, 30))

    #draw snake
    for snake in snakes_list:
        snake.draw_snake(screen)

    # handle keydown
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over == True:
                start_game()
        
        # handle snake's input
        if not game_over:
            for snake in snakes_list:
                snake.handel_input(event)
        
    # handel logic
    if not game_over:     
        # moving
        for snake in snakes_list:
            snake.moving()
        
        # eat
        for snake in snakes_list:
            if apple[0] == snake.body[-1][0] and apple[1] == snake.body[-1][1] :
                apple = [randint(0, 19),randint(0, 19)]
                snake.grow()
        
        # handle collision
        player1.check_collision(player2)
        player2.check_collision(player1)

        #handle game_over
        if not player1.alive and not player2.alive:
            game_over = True
            game_over_mess = "Both Player Lost"
        elif player1.alive and not player2.alive:
            game_over = True
            game_over_mess = "Player 1 wins"
        elif player2.alive and not player1.alive:
            game_over = True
            game_over_mess = "Player 2 wins"

    # score
    score1_txt = font_small.render("Player1's Length: " + str(player1.score), True, white)
    score2_txt = font_small.render("Player2's Length: " + str(player2.score), True, white)
    screen.blit(score1_txt, (830, 400))
    screen.blit(score2_txt, (830, 420))

    if game_over:
        game_over_txt = font_big.render(game_over_mess, True, white)
        space_txt = font_big.render("Press Space to try again", True, white)
        screen.blit(game_over_txt, (300,160))
        screen.blit(space_txt, (320, 230))

    pygame.display.flip()

pygame.quit()