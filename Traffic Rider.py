import random
import time
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Screen Parameters
screen_width = 800
screen_height = 600

# Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Traffic Rider')    # Name of Screen
clock = pygame.time.Clock()  # used to track amount of time

car_width = 50
car_Height = 50

# background
background = pygame.image.load('background.png')

# background music
mixer.music.load('Backgroundmusic.wav')
mixer.music.play(-1)  # "-1" plays music in a loop(music starts playing again)

# Car
cars = pygame.image.load('car.png')   # loads the image of car

# motorcycle
bikeImg = pygame.image.load('motorcycle.png')  # loads the image of motorcycle

# Counts no. of cars dodged (SCORE)
def cars_dodged(count):
    font = pygame.font.SysFont(None, 30)
    text = font.render("Dodged: " + str(count), True, (231, 76, 60))
    screen.blit(text, (0, 0))

# creates the image of the car on the screen
def cars1(x, y):
    screen.blit(cars, (x, y))  # blit function is used to draw the image on screen(x and y are position where image is to be drawn)

# creates the image of the bike on the screen
def bike(x, y):
    screen.blit(bikeImg, (x, y))  # blit function is used to draw the image on screen(x and y are position where image is to be drawn)


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((screen_width / 2), (screen_height / 2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

# Function to display CRASH message
def crash():
    message_display("You Crashed")

# Function for continuation of game after crash
def game_loop():
    x = (screen_width * 0.45)   # Starting position of bike(X)
    y = (screen_height * 0.8)   # Starting position of bike(Y)

    x_change = 0
    y_change = 0

    cars_startx = random.randrange(0, 750)  # Position from where cars appear
    cars_starty = -600
    cars_speed = 12      # the speed at which cars are comming(if increased, difficulty will also increase)
    cars_width = 50
    cars_height = 50

    dodged = 0  # Reset the value of score after crashing

    gameExit = False

    # loop to make the screen appear untill closed manually
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Assigning keys for movement of bike
            if event.type == pygame.KEYDOWN:    # if key pressed = "KEYDOWN"
                if event.key == pygame.K_LEFT:  # Left key is pressed
                    x_change = -10              # so decrease in X-axis(move towards 0)
                if event.key == pygame.K_RIGHT:  # Right key is pressed
                    x_change = 10                # so increase in X-axis(move towards 800)
                if event.key == pygame.K_UP:     # up key is pressed
                    y_change = -10                # so decrease in Y-axis(move towards 0, 0 is above on  Y-axis)
                if event.key == pygame.K_DOWN:     # down key is pressed
                    y_change = 10                  # so increase in Y-axis(move towards 600)

            if event.type == pygame.KEYUP:         # if key released = "KEYUP"
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN: # If any of either key is released
                    x_change = 0   # So stop movement of bike( no change)
                    y_change = 0   # So stop movement of bike( no change)

        x += x_change  # add the change into orignal value which occurs when left or right key is pressed
        y += y_change  # add the change into orignal value which occurs when up or down key is pressed

        # background image
        screen.blit(background, (0, 0))  # to draw background on the screen

        cars1(cars_startx, cars_starty)  # calling function "car1" and sending position of car where it has to be drawn(see the function above which uses blit command)

        cars_starty += cars_speed  # so the incomming cars can move
        bike(x, y)  # calling function "bike" and sending position of bike where it has to be drawn(see the function above which uses blit command)

        cars_dodged(dodged) # calling function so that the score can be drawn on the screen

        # collision with boundary
        if x > screen_width - car_width or x < 0:
            # crash sound
            crash_sound = mixer.Sound('crash.wav')
            crash_sound.play()
            crash()  # calling function so the crash message appears after crashing

        if cars_starty > screen_height:            # if one car leaves from the bottom so another comes from above
            cars_starty = 0 - cars_height
            cars_startx = random.randrange(0, 750)  # generates car from random position(different lanes)
            dodged += 1    # car passes without crashing so score is incremented
            cars_speed += 0.3  # increase in incomming cars at the rate of 0.3(increasing rate will also increase difficulty)

        # collision with car
        if y < cars_starty + cars_height:  # to detect head to head collisions
            if x > cars_startx and x < cars_startx + cars_width or x + car_width > cars_startx and x + car_width < cars_startx + cars_width:  #to detect sideways collision
                # crash sound
                crash_sound = mixer.Sound('crash.wav')
                crash_sound.play()
                crash()  # calling function so the crash message appears after crashing

        pygame.display.update() # updates the entire Screen.
        clock.tick(40)   # control the framerate. it tells how much time is passed since previous call


game_loop()  # calling game_loop functon
pygame.quit()  # to deactivate pygame library. opposite of "pygame.Init()" used in the begining.
quit()
