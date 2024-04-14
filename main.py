import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Road Rash")

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# Player settings
player_width = 60
player_height = 60
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 20
player_speed = 8

# Obstacle settings
obstacle_width = 60
obstacle_height = 100
obstacle_speed = 10
obstacle_interval = 600  # milliseconds
last_obstacle_time = 0
max_obstacles = 8  # maximum number of obstacles on the screen at a time
min_obstacles = 2  # minimum number of obstacles on the screen at a time

# Score
score = 0
high_score = 0
font = pygame.font.Font(None, 36)

# Load images
player_image = pygame.image.load("bike.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_width, player_height))

roadblock_image = pygame.image.load("roadblock.png").convert_alpha()
roadblock_image = pygame.transform.scale(roadblock_image, (obstacle_width, obstacle_height))

car_image = pygame.image.load("car.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (obstacle_width, obstacle_height))

# Function to draw the player
def draw_player(x, y):
    screen.blit(player_image, (x, y))

# Function to draw obstacles
def draw_obstacle(x, y, image):
    screen.blit(image, (x, y))

# Function to display game over popup
def game_over():
    global high_score
    if score > high_score:
        high_score = score
    popup_font = pygame.font.Font(None, 50)
    game_over_text = popup_font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50))
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2))
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

# Function to generate obstacles
def generate_obstacle():
    obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    obstacle_y = -obstacle_height
    obstacle_type = random.choice(["roadblock", "car"])  # Randomly choose between roadblock and car
    if obstacle_type == "roadblock":
        image = roadblock_image
    else:
        image = car_image
    if not any(obstacle[0] <= obstacle_x <= obstacle[0] + obstacle_width or
               obstacle_x <= obstacle[0] <= obstacle_x + obstacle_width
               for obstacle in obstacles):
        obstacles.append([obstacle_x, obstacle_y, image])

# Function to increase obstacle speed
def increase_obstacle_speed():
    global obstacle_speed
    obstacle_speed += 0.1

# Main game loop
running = True
clock = pygame.time.Clock()
obstacles = []

while running:
    screen.fill(GRAY)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    # Increase obstacle speed after every 10 scores
    if score % 10 == 0 and score != 0:
        increase_obstacle_speed()

    # Generate obstacles
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle_time > obstacle_interval:
        while len(obstacles) < min_obstacles:
            generate_obstacle()
        if len(obstacles) < max_obstacles:
            generate_obstacle()
            last_obstacle_time = current_time

    # Move and draw obstacles
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed
        draw_obstacle(obstacle[0], obstacle[1], obstacle[2])
        if obstacle[1] > SCREEN_HEIGHT:
            obstacles.remove(obstacle)
            score += 1

    # Check for collisions
    for obstacle in obstacles:
        if player_x < obstacle[0] + obstacle_width and player_x + player_width > obstacle[0] and player_y < obstacle[
            1] + obstacle_height and player_y + player_height > obstacle[1]:
            if game_over():
                score = 0
                obstacles = []
                obstacle_speed = 10
                break

    # Draw player
    draw_player(player_x, player_y)

    # Draw score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw high score
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
