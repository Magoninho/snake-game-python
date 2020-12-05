import pygame
import json
from pygame.locals import *
import random

settings = None
"""
OPENING THE SETTINGS FILE
"""
with open('./settings.json') as f:
    settings = json.load(f)

pygame.init()

pygame.mixer.init(44000, -16, 1, 1024)
pygame.mixer.music.load(settings['song_path'])
pygame.mixer.music.play(-1)


WIDTH = settings['screen_size']
HEIGHT = int(WIDTH / 4 * 4)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snake game")

WHITE = (255, 255, 255)
fruit_color = settings['fruit_color']


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# snake stuff
scale = settings['scale']
snk_x = WIDTH / 4 // scale * scale
snk_y = HEIGHT / 2 // scale * scale
initial_snake_size = settings['initial_snake_size']

moving_to = RIGHT

snake = []
morreu = False


def cria_snake():
    global initial_snake_size, scale, snk_x, snk_y
    for piece in range(initial_snake_size):
        snake.append([snk_x - scale * piece, snk_y])


cria_snake()


def frutinha():
    x = random.randint(0, WIDTH-scale)
    y = random.randint(0, HEIGHT-scale)
    return (x//scale * scale, y//scale * scale)


def score():
    global posicao_f
    snake.append([snk_x, snk_y])
    posicao_f = frutinha()


posicao_f = frutinha()


def main():
    global snake, moving_to

    scr = 0

    clock = pygame.time.Clock()

    # the main game loop
    while True:
        clock.tick(settings['frame_rate'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        SCREEN.fill((0, 0, 0))

        font = pygame.font.Font("./8-BIT.TTF", 24)
        text = font.render(
            str(scr), False, (255, 255, 255))
        SCREEN.blit(text, (0, 0))

        for square in range(len(snake) - 1, 0, -1):  # got stuck here a little bit
            snake[square] = [snake[square-1][0], snake[square-1][1]]
        keys = pygame.key.get_pressed()

        """
        omg a lot of if statements :O
        """
        if keys[pygame.K_UP]:
            moving_to = UP
        if keys[pygame.K_DOWN]:
            moving_to = DOWN
        if keys[pygame.K_RIGHT]:
            moving_to = RIGHT
        if keys[pygame.K_LEFT]:
            moving_to = LEFT
        if moving_to == RIGHT:
            snake[0] = [snake[0][0] + scale, snake[0][1]]
        if moving_to == LEFT:
            snake[0] = [snake[0][0] - scale, snake[0][1]]
        if moving_to == UP:
            snake[0] = [snake[0][0], snake[0][1] - scale]
        if moving_to == DOWN:
            snake[0] = [snake[0][0], snake[0][1] + scale]

        # making the head stay with the body
        for body in range(len(snake)):

            pygame.draw.rect(SCREEN, settings['snake_color'],
                             (snake[body][0], snake[body][1], scale, scale))

        pygame.draw.rect(SCREEN, fruit_color,
                         (posicao_f[0], posicao_f[1], scale, scale))

        if snake[0][0] == posicao_f[0] and snake[0][1] == posicao_f[1]:
            scr += 1
            score()

        """
        MAKE THE SNAKE COMEBACK WHEN GOING THROUGH THE WALL
        """
        if snake[0][0] > WIDTH - scale:
            snake[0][0] = 0

        if snake[0][0] < 0:
            snake[0][0] = WIDTH - scale

        if snake[0][1] > HEIGHT - scale:
            snake[0][1] = 0

        if snake[0][1] < 0:
            snake[0][1] = HEIGHT - scale

        for i in range(len(snake) - 1, 0, -1):
            # if the snake collides with itself
            if snake[0] == snake[i]:
                pygame.font.init()
                font = pygame.font.Font("8-BIT.TTF", 17)
                text = font.render(
                    "Press R to respawn", False, (0, 255, 255))
                SCREEN.blit(text, (5, HEIGHT-25))
                morreu = True
                while morreu:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == K_r:
                                snake = []
                                cria_snake()
                                moving_to = RIGHT
                                main()
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                exit()
                    pygame.display.update()

        pygame.display.update()


main()
