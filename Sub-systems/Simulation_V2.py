import pygame
import random

# initialize Pygame
pygame.init()

# define window size
window_width = 1250
window_height = 750

# Define the color of the road
white = (215, 205, 205) #255
black = (0, 0, 0)
red = (255, 0, 0)

# Create the game's window
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Car Simulation")

# Define the car's width and height
car_width = 15     
car_height = 20     
player_car = pygame.image.load("main\AV\Images\car.png")
player_car = pygame.transform.scale(player_car, (car_width, car_height))

# Define obstacle car
obstacle_width = 15
obstacle_height = 20
obstacle_car = pygame.image.load("main\AV\Images\car1.png")
obstacle_car = pygame.transform.scale(obstacle_car, (obstacle_width, obstacle_height))

# Set up clock
clock = pygame.time.Clock()

# Set up font color
font = pygame.font.SysFont(None, 30)
color_font = (255,0,0)

def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color_font)
    game_window.blit(screen_text, [window_width/3, window_height/3])


def game_loop():
    # define starting position of player's car
    x = window_width * 0.5
    y = window_height * 0.8

    # define starting position of obstacle car
    obstacle_x = random.randrange(0, window_width - obstacle_width)
    obstacle_y = -obstacle_height

    # define speed of cars
    car_speed_y = -5
    car_speed = 0
    obstacle_speed = 5

    # set up game over flag
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            # move car left and right with arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_speed = -5
                elif event.key == pygame.K_RIGHT:
                    car_speed = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_speed = 0
                    
        # move player's car
        x += car_speed
        y += car_speed_y
        # draw road
        game_window.fill(black)
        pygame.draw.rect(game_window, white, [100, 0, 600, window_height])
        # draw player's car
        game_window.blit(player_car, (x, y))
        # draw obstacle car and move it down the screen
        game_window.blit(obstacle_car, (obstacle_x, obstacle_y))
        obstacle_y += obstacle_speed
        # check if obstacle car goes off the screen and reset it
        if obstacle_y > window_height:
            obstacle_y = -obstacle_height
            obstacle_x = random.randrange(0, window_width - obstacle_width)
        # check for collision with obstacle car
        if y < obstacle_y + obstacle_height:
            if x > obstacle_x and x < obstacle_x + obstacle_width or x + car_width > obstacle_x and x + car_width < obstacle_x + obstacle_width:
                game_over = True
        # update display and set frames per second
        pygame.display.update()
        clock.tick(60)

    message_to_screen("Game over. Press Q to quit or R to restart.", red)
    pygame.display.update()

    # wait for player to quit or restart game
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_exit = True
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    game_loop()

game_loop()
pygame.quit()
quit()

