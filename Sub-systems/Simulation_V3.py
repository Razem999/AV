import pygame
import random

# initialize pygame
pygame.init()

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# set screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulation Game")

# set game clock
clock = pygame.time.Clock()

# define font
font = pygame.font.SysFont(None, 40)

# load images
car_img = pygame.image.load("main\AV\Images\car.png")
car_rect = car_img.get_rect()

# define car speed and position
car_speed = 5
car_x = SCREEN_WIDTH // 2 - car_rect.width // 2
car_y = SCREEN_HEIGHT - car_rect.height

# define obstacle properties
obstacle_speed = 5
obstacle_min_width = 30
obstacle_max_width = 80
obstacle_min_height = 30
obstacle_max_height = 80
obstacles = []

# define game mode
mode = "manual"

# define game score
score = 0

# define functions
def draw_car(x, y):
    screen.blit(car_img, (x, y))

def draw_obstacle(obstacle):
    pygame.draw.rect(screen, RED, obstacle)

def generate_obstacle():
    obstacle_width = random.randint(obstacle_min_width, obstacle_max_width)
    obstacle_height = random.randint(obstacle_min_height, obstacle_max_height)
    obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    obstacle_y = -obstacle_height
    return pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

def move_obstacles():
    global score
    for obstacle in obstacles:
        obstacle.move_ip(0, obstacle_speed)
        if obstacle.bottom >= 0 and obstacle.top < SCREEN_HEIGHT:
            draw_obstacle(obstacle)
        else:
            obstacles.remove(obstacle)
            obstacles.append(generate_obstacle())
            score += 1

def check_collision():
    for obstacle in obstacles:
        if car_rect.colliderect(obstacle):
            return True
    return False

# start game loop
def game_loop():
    running = True
    mode = "manual"
    while running:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    mode = "auto"
                if event.key == pygame.K_m:
                    mode = "manual"
                if event.key == pygame.K_e:
                    running = False
                if mode == "manual":
                    if event.key == pygame.K_LEFT:
                        car_x -= car_speed
                    if event.key == pygame.K_RIGHT:
                        car_x += car_speed
                    if event.key == pygame.K_UP:
                        car_speed += 1
                    if event.key == pygame.K_DOWN:
                        car_speed -= 1
                        if car_speed < 0:
                            car_speed = 0
        # move car
        if mode == "auto":
            if car_rect.left < 0:
                car_x = 0
            elif car_rect.right > SCREEN_WIDTH:
                car_x = SCREEN_WIDTH - car_rect.width
            else:
                car_x += random.randint(-1, 1)
        elif mode == "manual":
            if car_x < 0:
                car_x = 0
            elif car_x > SCREEN_WIDTH - car_rect.width:
                car_x = SCREEN_WIDTH - car_rect.width
        # move obstacles and check
        # move obstacles and check collision
        move_obstacles()
        if check_collision():
            running = False
        # fill background
        screen.fill(WHITE)
        # draw car and obstacles
        draw_car(car_x, car_y)
        for obstacle in obstacles:
            draw_obstacle(obstacle)
        # draw score
        score_text = font.render("Score: {}".format(score), True, BLACK)
        screen.blit(score_text, (10, 10))
        # update screen
        pygame.display.update()
        # set game speed
        clock.tick(60)
    
if __name__ == "__main__":
    game_loop()
    pygame.quit()
    quit()

