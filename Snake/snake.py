import pygame, sys
from pygame.locals import *
import pygame.freetype
import time
import random

resX = 400
resY = 400


def draw_grid(screen_width, screen_height):
    pygame.draw.lines(screen, BLACK, False, [[0, 0], [screen_width-1, 0], [screen_width-1, screen_height-1],  #границы
                                             [0, screen_height-1], [0, 0]], 3)
    for i in range(0, 400, 20):
        pygame.draw.lines(screen, BLACK, False, [[i, 0], [i, screen_height]], 1)
        pygame.draw.lines(screen, BLACK, False, [[0, i], [screen_width, i]], 1)


def text_blit_on_surf(text, font_size, text_color, back_color, center_x, center_y, surface):
    font = pygame.font.Font("Times.ttf", font_size)
    textSurfaceObj = font.render(text, True, text_color, back_color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (center_x, center_y)
    surface.blit(textSurfaceObj, textRectObj)
    pygame.display.update()


class Snake:
    def __init__(self):
        self.score = 0
        self.size = 0
        self.snake_ded = False
        self.X = 1
        self.Y = 1
        self.tail = [[1, 1], [0, 0]]
        self.direction = str

    def checkup(self):
        if self.X < 0 or self.Y < 0 or self.X > resX or self.Y > resY or [self.X, self.Y] in self.tail[1:]:
            text_blit_on_surf('Lol u died', 40, GREEN, BLUE, resX/2, resY/2, screen)
            pygame.time.wait(700)
            pygame.quit()
            sys.exit()

    def turn(self):
        if self.direction == 'Left':
            self.X -= 20
        if self.direction == 'Right':
            self.X += 20
        if self.direction == 'Up':
            self.Y -= 20
        if self.direction == 'Down':
            self.Y += 20

    def ate(self):
        self.size += 1

    def render(self):
        self.tail.insert(0, [self.X, self.Y])
        del self.tail[self.size+1:]
        for i in range(self.size + 1):
            pygame.draw.rect(screen, GREEN, [self.tail[i][0], self.tail[i][1], 19, 19])
        pygame.draw.rect(screen, RED, [self.X + 2, self.Y + 2, 2, 2])
        pygame.draw.rect(screen, RED, [self.X + 15, self.Y + 2, 2, 2])


class Apple:
    def __init__(self):
        self.apple_random = [[1 + n, 1 + j] for n in range(0, 400, 20) for j in range(0, 400, 20)]
        self.X, self.Y = random.choice(self.apple_random)

    def newapple(self):
        self.X, self.Y = random.choice(self.apple_random)

    def render(self):
        pygame.draw.rect(screen, RED, [self.X, self.Y, 19, 19])


pygame.init()

apple = Apple()
snake = Snake()

screen = pygame.display.set_mode((resX, resY), 0, 32)  # отрисовка окна
pygame.display.set_caption('BEST SNAEK IN DA WORLD')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FPS = 15

fpsClock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.direction = 'Left'
            elif event.key == pygame.K_RIGHT:
                snake.direction = 'Right'
            elif event.key == pygame.K_UP:
                snake.direction = 'Up'
            elif event.key == pygame.K_DOWN:
                snake.direction = 'Down'

    screen.fill(WHITE)
    draw_grid(resX, resY)
    apple.render()
    snake.turn()
    snake.checkup()
    snake.render()

    if (snake.X == apple.X) and (snake.Y == apple.Y):
        snake.ate()
        apple.newapple()

    pygame.display.update()
    fpsClock.tick(FPS)

