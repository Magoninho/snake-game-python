import pygame
import random
from pygame.locals import *
import json

# Oppening the settings json file
with open('./settings.json') as f:
    settings = json.load(f)

pygame.init()

# initializing the pygame mixer
pygame.mixer.init(44000, -16, 1, 1024)
pygame.mixer.music.load(settings['song_path'])
pygame.mixer.music.play(-1)

# some constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = settings['screen_size']
HEIGHT = int(WIDTH / 4 * 4)
SCALE = settings['scale']
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# The game class
class Game:
    def __init__(self, title):
        # this makes the aspect ratio of the window
        self.title = title
        self.frame_rate = settings['frame_rate'] # setting the framerate with the settings
        self.clock = pygame.time.Clock()

    # instances and things that are executed once
    def setup(self):

        pygame.display.set_caption(self.title) # setting the window title

        self.snake = Snake(WIDTH / 4 // SCALE * SCALE,
                           HEIGHT / 2 // SCALE * SCALE, 5, SCALE) # instanciating the snake
        self.snake.create_snake() # creating the snake wow
        self.fruit = Fruit() # creating the fruit

    # the place to render objects
    def render(self):
        """
        Here goes all the drawinings that need to be rendered
        """
        SCREEN.fill((0, 0, 0))
        self.snake.draw_snake(SCREEN, WHITE) # drawining the snake
        self.fruit.draw_fruit(SCREEN) # drawining the fruit
        font = pygame.font.Font("./8-BIT.TTF", 24) # initializing the font
        text = font.render(
            str(self.snake.score), False, (255, 255, 255)) # rendering the score text
        SCREEN.blit(text, (0, 0)) # bliting the score to the screen surface

    # here comes the update of the game
    def update(self, condition):

        while condition:
            """
            The event loop
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    # if you press ESC you quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            """------------ before render process ------------"""

            self.clock.tick(self.frame_rate) # setting the limit of framerate with the framerate specified

            self.snake.move() # starting the snake movement
            self.snake.eat(self.fruit, self.fruit.fruit_pos) # constantly checking if the snake ate the fruit

            """---------------------render---------------------"""

            self.render() # rendering the stuff :D
            pygame.display.update() # updating the display

            """------------------------------------------------"""

# THE SNAKE CLASS
class Snake:
    def __init__(self, initialX, initialY, initial_size, scale):

        self.snake = []  # snake body list
        # parameters
        self.initialX = initialX
        self.initialY = initialY
        self.initial_size = settings['initial_snake_size']
        self.dead = False
        self.score = 0
        SCALE = scale # idk

        # movement constants
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        self.moving_to = self.RIGHT

    def die(self):
        """
        The die function
        it initializes a new while loop asking to press r to restart
        if the user presses restart it will run the main function (the core function of the game)
        """
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

    # create the snake
    def create_snake(self):
        # goes through every piece of the initial body size and append to the snake body array
        # the snake has an array for each body piece. This array contains the X and the Y
        for piece in range(self.initial_size):
            self.snake.append(
                [self.initialX - SCALE * piece, self.initialY]) # and there is some calculations to make the body be side by side correctly

    # draw the snake
    def draw_snake(self, screen, color):
        # now it will pick all the pieces appended to the body array and draw it
        for body in range(len(self.snake)):
            pygame.draw.rect(
                screen, settings['snake_color'], (self.snake[body][0], self.snake[body][1], SCALE, SCALE))

    def move(self):
        # this will bind the snake body (if you remove this part of the code, only the head of the snake will go foward)
        for square in range(len(self.snake) - 1, 0, -1):
            self.snake[square] = [self.snake[square - 1]
                                  [0], self.snake[square - 1][1]]

        keys = pygame.key.get_pressed() # gets all the keys pressed by the user

        """
        A lot of if statements to change the direction and apply
        This needs to be like this because the snake moves by itself (you don't need to keep holding the key), so it will set the direction and
        make another set of conditions to move the snake according to the moving_to variable value
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

        """
        Checking if the collide_on_walls is activated
        """
        if not settings['collide_on_walls']:
            if self.snake[0][0] > WIDTH - SCALE:
                self.snake[0][0] = 0

            if self.snake[0][0] < 0:
                self.snake[0][0] = WIDTH - SCALE

            if self.snake[0][1] > HEIGHT - SCALE:
                self.snake[0][1] = 0

            if self.snake[0][1] < 0:
                self.snake[0][1] = HEIGHT - SCALE
        # if it is not activated, just die when colliding with the walls
        else:
            if self.snake[0][0] > WIDTH - SCALE or self.snake[0][0] < 0 or self.snake[0][1] > HEIGHT - SCALE or self.snake[0][1] < 0:
                self.die()
        # if the snake collides with itself
        for i in range(len(self.snake) - 1, 0, -1):
            if self.snake[0] == self.snake[i]:
                self.die()
    # checking if the snake ate
    def eat(self, fruit, fruit_pos):
        # if the X and Y coordinates of the snake's head is equal to the fruit's X coordinate
        if self.snake[0][0] == fruit_pos[0] and self.snake[0][1] == fruit_pos[1]:
            self.snake.append(self.snake[0]) # append one piece to the body (it will calculate automatically because the snake is constantly moving)
            fruit.fruit_pos = fruit.generate_new_fruit() # generate a new fruit
            self.score += 1 # add one score to the player

# The Fruit class
class Fruit:
    def __init__(self):
        self.color = settings['fruit_color'] # gets the fruit color in the settings.json
        self.fruit_pos = self.generate_new_fruit() # the position of the fruit is the value returned from the generate_new_fruit function

    def generate_new_fruit(self):

        # picks a random position between 0 and the window sizes minus the scale of the grid
        x = random.randint(0, WIDTH - SCALE)
        y = random.randint(0, HEIGHT - SCALE)
        return [x // SCALE * SCALE, y // SCALE * SCALE]

    def draw_fruit(self, screen):
        pygame.draw.rect(screen, self.color, (self.fruit_pos[0], self.fruit_pos[1],
                                              SCALE, SCALE))


#-------------- S T U F F --------------#
# game loop condition
def main():

    game = Game("The best game ever") # instanciates the game itself
    game.setup() # runs the setup function
    game.update(True) # updates the game given a condition for it


main()

"""
Feito com carinho,
por Magoninho :)

Made with love,
by Magoninho :)
"""
