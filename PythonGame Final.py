from pygame.locals import *
import pygame
import time
import random

pygame.init()
display_width = 800
display_height = 600
snake_width = 10
snake_height= 10
snake_margin= 1
snake_length= 10
# define all the color that is used in the game
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 128, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

# define the crash state for the main function


block_color = (53, 115, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(" Snake Game made by Tung")
clock = pygame.time.Clock()


# Making a text object
def text_object(text, font, color):
    textsurface = font.render(text, True, color)
    return textsurface, textsurface.get_rect()


# Now we make the snake appearing on the main screen before choosing what to do next
def snakeBackGround(x, y):
    snakeImgMain =  pygame.image.load('snakebackground.png')
    gameDisplay.blit(snakeImgMain, (x, y))


# Then we create the button function to dynamically create button in the
def button(message, x, y, w, h, inactivecolor, activecolor, action=None):
    # get the mouse position
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print("click = {}".format(click))
    # if the mouse is in the button, change the color
    print(h)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        # create a rectangle in the display
        pygame.draw.rect(gameDisplay, activecolor, (x, y, w, h))

        # Check if there is a click and whether there is any action associated with the button
        if click[0] == 1 and action != None:
            action()
    else:  # otherwise just normal color should be fine
        pygame.draw.rect(gameDisplay, inactivecolor, (x, y, w, h))

    smalltext = pygame.font.SysFont("comicsansms", 18)
    textSurf, textRect = text_object(message, smalltext, black)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


# define quit game action
def quitgame():
    pygame.quit()
    quit()


# create an introduction page
def intro_page():
    intro = True
    x = display_width * 0.4
    y = display_height * 0.2

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        #create a snake background
        snakeBackGround(x, y)
        introtext = pygame.font.SysFont("comicsansms", 18)
        textSurf, textRect = text_object("Snakey Game", introtext, black)
        textRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(textSurf, textRect)

        # Proceed with creating the button
        button("Start Game", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit Game", 550, 450, 100, 50, red, bright_red, quitgame)

        # now update the display
        pygame.display.update()
        clock.tick(1)


# create class Apply
'''
class Apple(pygame.sprite.Sprite):
    def __init__(self,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        #create a block and fill it with color
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
'''


class Apple(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("apple.png").convert_alpha()

        self.rect_x = x
        self.rect_y = y
        # (20,20) is a good size for the snake

        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()# create a rectangle
        self.rect = self.rect.move((x, y))  # move the rectangle to a certain position in the screen

        gameDisplay.blit(self.image, self.rect)


# create the class snake
class Snakesegment(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('snake.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.step = 20



#Create a segment of the snake
class Snake():
    def __init__(self):
        self.allspriteslist = pygame.sprite.Group()
        self.snake_body =[]

        for i in range(snake_length):
            print ("this is i = {}".format(i))
            self.x = 500 - (snake_width + snake_margin) * i
            self.y = 500
            self.segment = Snakesegment(self.x, self.y)
            self.snake_body.append(self.segment)
            self.allspriteslist.add(self.segment)
    def moveLeft(self):
        print("RIGHT")
        self.x_change = (snake_width+snake_margin)*-1
        self.y_change = 0
        return self.x_change, self.y_change

    def moveRight(self):
        print("LEFT")
        self.x_change = (snake_width+snake_margin)
        self.y_change = 0
        return self.x_change, self.y_change


    def moveUp(self):
        print("UP")

        self.x_change = 0
        self.y_change = (snake_height + snake_margin)*-1
        return self.x_change, self.y_change



    def moveDown(self):
        print("DOWN")
        self.x_change = 0
        self.y_change = (snake_height + snake_margin)
        return self.x_change, self.y_change

    def update(self,x_change,y_change):
        #update the head position
        self.x_change = x_change
        self.y_change = y_change
        self.x = self.snake_body[0].rect.x + self.x_change
        self.y = self.snake_body[0].rect.y + self.y_change
        self.segment = Snakesegment(self.x,self.y)


        self.snake_body.insert(0,self.segment)
        self.allspriteslist.add(self.segment)
        print("new sprites list {}".format(self.allspriteslist))

    def delete_tail(self):
        #udate the tail
        self.old_segment = self.snake_body.pop()
        self.allspriteslist.remove(self.old_segment)




    def draw(self,gameDisplay):
        gameDisplay.blit(self.image, self.rect)


#Check for collision

# This is the main display of the game that ultilize all the function created

def game_loop():
    # initialise the player class
    # create the coordinate of the apple
    x_apple = random.randrange(0, display_width)
    y_apple = random.randrange(0, display_height)
    crashed = False
    snake = Snake()
    x_change =snake_margin+ snake_width
    y_change = 0

    while not crashed:
        gameDisplay.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x_change !=snake_width+snake_margin and y_change != 0: #check for opposite direction
                        x_change,y_change = snake.moveLeft()
                    # snake.draw()
                if event.key == pygame.K_RIGHT:
                    if x_change != (snake_width +snake_margin)*-1 and y_change != 0: #Check for opposite direction
                        x_change, y_change = snake.moveRight()
                    # snake.draw()
                if event.key == pygame.K_DOWN:
                    if x_change != 0 and y_change !=(snake_height + snake_margin)*-1: #Check for opposite direction
                        x_change, y_change = snake.moveDown()
                    # snake.draw()
                if event.key == pygame.K_UP:
                    if x_change != 0 and y_change !=(snake_height + snake_margin):
                        x_change, y_change = snake.moveUp()
                    # snake.draw()
        #update the last part of the snake
        apple = Apple(x_apple, y_apple)
        snake.update(x_change,y_change)

        eatapple = pygame.sprite.collide_rect(snake.snake_body[0],apple)
        if eatapple:
            print( "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            #Change the position of the apple --> create a new apple
            x_apple = random.randrange(0, display_width)
            y_apple = random.randrange(0, display_height)
        else: #normally, it will delete the tail, only when there is an overlap with the apple
            snake.delete_tail()

        #Check for collision with itself
        tung =  pygame.sprite.spritecollideany(snake.snake_body[0],snake.allspriteslist,collided=None)
        print ("this is tung {}".format(tung))
        if tung == None:
            crashed = True
        snake.allspriteslist.draw(gameDisplay)



        # Fill white background


        # tung = pygame.sprite.collide_rect(apple,snake.allspriteslist)
        pygame.display.flip()

        pygame.display.update()
        clock.tick(10)


# intro_page()
game_loop()
pygame.quit()
quit()