import pygame
from pygame.locals import *
import random


pygame.init()

pygame.mixer.init(44000, -16, 1, 1024)
pygame.mixer.music.load('./song2.wav')
pygame.mixer.music.play(-1)


WIDTH, HEIGHT = 300, 300
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snake game")

WHITE = (255, 255, 255)
head_color = (255, 255, 0)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# snake stuff
scale = 10
snk_x = WIDTH / 4 // scale * scale
snk_y = HEIGHT / 2 // scale * scale
tamanho_inicial = 5

moving_to = RIGHT

snake = []
morreu = False


def cria_snake():
    global tamanho_inicial, scale, snk_x, snk_y
    for piece in range(tamanho_inicial):
        snake.append([snk_x - scale * piece, snk_y])


cria_snake()


def frutinha():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    return (x//scale * scale, y//scale * scale)


def score():
    global posicao_f
    snake.append([snk_x, snk_y])
    posicao_f = frutinha()


posicao_f = frutinha()


def main():
    global snake, moving_to
    clock = pygame.time.Clock()
    while True:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        SCREEN.fill((0, 0, 0))

        for square in range(len(snake) - 1, 0, -1):  # fiquei preso aqui por um tempo k
            snake[square] = [snake[square-1][0], snake[square-1][1]]
        keys = pygame.key.get_pressed()

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

        # deixando o corpo da cobra grudado com a cabeça kkkkk
        for body in range(len(snake)):

            pygame.draw.rect(SCREEN, (WHITE),
                             (snake[body][0], snake[body][1], scale, scale))

        pygame.draw.rect(SCREEN, (255, 255, 0),
                         (posicao_f[0], posicao_f[1], scale, scale))

        if snake[0][0] == posicao_f[0] and snake[0][1] == posicao_f[1]:
            score()

        for i in range(len(snake) - 1, 0, -1):
            # se a cobra colide com ela mesma
            if snake[0] == snake[i]:
                pygame.font.init()
                font = pygame.font.SysFont("Arial", 24)
                text = font.render(
                    "Aperte R para recomeçar", False, (0, 255, 255))
                SCREEN.blit(text, (0, 0))
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
