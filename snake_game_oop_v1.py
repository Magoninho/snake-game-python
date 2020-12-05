import pygame
import random
from pygame.locals import *
import json


settings = None

with open('settings.json') as f:
    settings = json.load(f)

pygame.init()

pygame.mixer.init(44000, -16, 1, 1024)
pygame.mixer.music.load(settings['song_path'])
pygame.mixer.music.play(-1)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = settings['screen_size']
HEIGHT = int(WIDTH / 4 * 4)
SCALE = settings['scale']
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


class Game:
    def __init__(self, title):
        # this makes the aspect ratio of the window
        self.title = title
        self.frame_rate = settings['frame_rate']
        self.clock = pygame.time.Clock()
    # instances and things that are executed once

    def setup(self):

        pygame.display.set_caption(self.title)

        self.snake = Snake(WIDTH / 4 // SCALE * SCALE,
                           HEIGHT / 2 // SCALE * SCALE, 5, SCALE)
        self.snake.create_snake()
        self.fruit = Fruit()

    # the place to render objects
    def render(self):
        """
        Here goes all the drawinings
        """
        SCREEN.fill((0, 0, 0))
        self.snake.draw_snake(SCREEN, WHITE)
        self.fruit.draw_fruit(SCREEN)
        font = pygame.font.Font("./8-BIT.TTF", 24)
        text = font.render(
            str(self.snake.score), False, (255, 255, 255))
        SCREEN.blit(text, (0, 0))

    # here comes the update of the game
    def update(self, condition):

        while condition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            """------------ before render process ------------"""

            self.clock.tick(self.frame_rate)

            self.snake.move()
            self.snake.eat(self.fruit, self.fruit.fruit_pos)

            """---------------------render---------------------"""

            self.render()
            pygame.display.update()

            """------------------------------------------------"""


class Snake:
    def __init__(self, initialX, initialY, initial_size, scale):

        self.snake = []  # snake body list
        self.initialX = initialX
        self.initialY = initialY
        self.initial_size = settings['initial_snake_size']
        self.dead = False
        self.score = 0
        SCALE = scale

        # movement constants
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        self.moving_to = self.RIGHT

        # TODO: aplicar as configurações do json nessas definições

    def create_snake(self):
        for piece in range(self.initial_size):
            self.snake.append(
                [self.initialX - SCALE * piece, self.initialY])

    def draw_snake(self, screen, color):
        for body in range(len(self.snake)):
            pygame.draw.rect(
                screen, settings['snake_color'], (self.snake[body][0], self.snake[body][1], SCALE, SCALE))

    def move(self):
        # Grudador de corpo de cobra by magoninho gamer corporation enterteinement ltda
        for square in range(len(self.snake) - 1, 0, -1):
            self.snake[square] = [self.snake[square - 1]
                                  [0], self.snake[square - 1][1]]

        keys = pygame.key.get_pressed()

        """
        omg a lot of if statements :O
        """
        if keys[pygame.K_UP]:
            self.moving_to = self.UP
        if keys[pygame.K_DOWN]:
            self.moving_to = self.DOWN
        if keys[pygame.K_RIGHT]:
            self.moving_to = self.RIGHT
        if keys[pygame.K_LEFT]:
            self.moving_to = self.LEFT

        if self.moving_to == self.RIGHT:
            self.snake[0] = [self.snake[0][0] + SCALE, self.snake[0][1]]
        if self.moving_to == self.LEFT:
            self.snake[0] = [self.snake[0][0] - SCALE, self.snake[0][1]]
        if self.moving_to == self.UP:
            self.snake[0] = [self.snake[0][0], self.snake[0][1] - SCALE]
        if self.moving_to == self.DOWN:
            self.snake[0] = [self.snake[0][0], self.snake[0][1] + SCALE]

        if self.snake[0][0] > WIDTH - SCALE:
            self.snake[0][0] = 0

        if self.snake[0][0] < 0:
            self.snake[0][0] = WIDTH - SCALE

        if self.snake[0][1] > HEIGHT - SCALE:
            self.snake[0][1] = 0

        if self.snake[0][1] < 0:
            self.snake[0][1] = HEIGHT - SCALE

        for i in range(len(self.snake) - 1, 0, -1):
            # if the snake collides with itself
            if self.snake[0] == self.snake[i]:
                pygame.font.init()
                font = pygame.font.Font("8-BIT.TTF", 17)
                text = font.render(
                    "Press R to respawn", False, (0, 255, 255))
                self.dead = True
                while self.dead:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == K_r:
                                main()
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                exit()
                    SCREEN.blit(text, (5, HEIGHT-25))
                    pygame.display.update()

    def eat(self, fruit, fruit_pos):
        if self.snake[0][0] == fruit_pos[0] and self.snake[0][1] == fruit_pos[1]:
            self.snake.append(self.snake[0])
            fruit.fruit_pos = fruit.generate_new_fruit()
            self.score += 1


class Fruit:
    def __init__(self):
        self.color = settings['fruit_color']
        self.fruit_pos = self.generate_new_fruit()

    def generate_new_fruit(self):
        x = random.randint(0, WIDTH - SCALE)
        y = random.randint(0, HEIGHT - SCALE)
        return [x // SCALE * SCALE, y // SCALE * SCALE]

    def draw_fruit(self, screen):
        pygame.draw.rect(screen, self.color, (self.fruit_pos[0], self.fruit_pos[1],
                                              SCALE, SCALE))


#-------------- S T U F F --------------#
# variables
# game loop condition
def main():
    game = Game("The best game ever")
    game.setup()
    game.update(True)


main()
"""
TODO:
- aplicar as configurações do json
- comentar o codigo
"""
