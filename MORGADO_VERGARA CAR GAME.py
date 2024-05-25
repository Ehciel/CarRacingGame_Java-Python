import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
CAR_WIDTH, CAR_HEIGHT = 70, 100
ENEMY_CAR_WIDTH, ENEMY_CAR_HEIGHT = 70, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60
CAR_SPEED = 10  # Sensitivity of car movement
LINE_WIDTH = 10
LINE_HEIGHT = 60
LINE_GAP = 20
NUM_LANES = 4

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()

# Load car images
player_car = pygame.transform.scale(pygame.image.load('player_car.png'), (CAR_WIDTH, CAR_HEIGHT))
enemy_car = pygame.transform.scale(pygame.image.load('enemy_car.png'), (ENEMY_CAR_WIDTH, ENEMY_CAR_HEIGHT))

# Load background music
pygame.mixer.music.load('game start.mp3')  

# Load sound effects
game_over_sound = pygame.mixer.Sound('background.mp3')  

# Font for scoreboard and game over screen
font = pygame.font.SysFont(None, 36)

# Player starting position
player_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
player_y = SCREEN_HEIGHT - CAR_HEIGHT - 20

# Enemy car list
enemy_cars = []
enemy_speed = 8

# Time related variables
ADD_ENEMY_EVENT = pygame.USEREVENT + 1
initial_spawn_time = 2000  # 2 seconds initial spawn time
spawn_time = initial_spawn_time
pygame.time.set_timer(ADD_ENEMY_EVENT, spawn_time)

# Score
score = 0
highest_score = 0

# History of player scores
player_history = []

# Start background music
pygame.mixer.music.play(-1)  

def get_player_name():
    input_background = pygame.image.load('input_background.JPG').convert()
    input_background = pygame.transform.scale(input_background, (SCREEN_WIDTH, SCREEN_HEIGHT))  
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    # Set up the font
    font = pygame.font.SysFont(None, 38)
    prompt_text = font.render("Enter your name:", True, WHITE)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.blit(input_background, (0, 0))  
        
        # Display player history
        y_offset = 10
        for record in player_history:
            record_text = font.render(f"{record['name']}: {record['score']}", True, WHITE)
            screen.blit(record_text, (10, y_offset))
            y_offset += 40

        # Blit the prompt text above the input box
        screen.blit(prompt_text, (input_box.x, input_box.y - 40))

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

    return text

def add_enemy():
    x = random.randint(0, SCREEN_WIDTH - ENEMY_CAR_WIDTH)
    y = -ENEMY_CAR_HEIGHT
    enemy_cars.append([x, y])

def move_enemies():
    global score
    for car in enemy_cars:
        car[1] += enemy_speed
        if car[1] > SCREEN_HEIGHT:
            enemy_cars.remove(car)
            score += 10  
def draw_enemies():
    for car in enemy_cars:
        screen.blit(enemy_car, (car[0], car[1]))

def draw_player():
    screen.blit(player_car, (player_x, player_y))

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    player_name_text = font.render(f"Player: {player_name}", True, WHITE)
    highest_score_text = font.render(f"Highest Score: {highest_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(player_name_text, (10, 50))
    screen.blit(highest_score_text, (10, 90))

def check_collision():
    player_rect = pygame.Rect(player_x, player_y, CAR_WIDTH, CAR_HEIGHT)
    for car in enemy_cars:
        enemy_rect = pygame.Rect(car[0], car[1], ENEMY_CAR_WIDTH, ENEMY_CAR_HEIGHT)
        if player_rect.colliderect(enemy_rect):
            return True
    return False

def increase_difficulty():
    global enemy_speed, spawn_time
    enemy_speed += 0.01  # Gradually increase the speed of enemies
    new_spawn_time = max(500, spawn_time - 10) 
    if new_spawn_time < spawn_time:
        spawn_time = new_spawn_time
        pygame.time.set_timer(ADD_ENEMY_EVENT, int(spawn_time))  # Update the timer with the new spawn interval

def draw_lanes():
    lane_color = WHITE
    lane_x_positions = [
        SCREEN_WIDTH // NUM_LANES * i - LINE_WIDTH // 2 for i in range(1, NUM_LANES)
    ]
    
    for lane_x in lane_x_positions:
        for y in range(0, SCREEN_HEIGHT, LINE_HEIGHT + LINE_GAP):
            pygame.draw.rect(screen, lane_color, (lane_x, y, LINE_WIDTH, LINE_HEIGHT))
    
    # Draw left and right edges
    pygame.draw.rect(screen, lane_color, (0, 0, LINE_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, lane_color, (SCREEN_WIDTH - LINE_WIDTH, 0, LINE_WIDTH, SCREEN_HEIGHT))

def game_over_screen():
    global highest_score
    if score > highest_score:
        highest_score = score
    game_over_text = font.render("Game Over", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    highest_score_text = font.render(f"Highest Score: {highest_score}", True, WHITE)
    player_name_text = font.render(f"Player: {player_name}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
    screen.blit(highest_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    screen.blit(player_name_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    # Draw Restart and Quit buttons
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
    pygame.draw.rect(screen, GREEN, restart_button)
    pygame.draw.rect(screen, RED, quit_button)

    restart_text = font.render("Restart", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 60))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - 35, SCREEN_HEIGHT // 2 + 130))

    pygame.mixer.music.stop()  # Stop background music when game over

    return restart_button, quit_button

if check_collision():
    game_over_sound.play()  # Play game over sound effect
    player_history.append({"name": player_name, "score": score})
    game_over = True


def reset_game():
    global player_x, player_y, enemy_cars, enemy_speed, spawn_time, score
    player_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
    player_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
    enemy_cars = []
    enemy_speed = 8
    spawn_time = initial_spawn_time
    score = 0
    pygame.time.set_timer(ADD_ENEMY_EVENT, spawn_time)

def start_screen():
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
    start_text = font.render("Start Game", True, WHITE)
    
    # Load the background image
    background_image = pygame.image.load("start_background.JPG")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    screen.blit(background_image, (0, 0))  
    pygame.draw.rect(screen, GREEN, start_button)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 15))
    pygame.display.flip()
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return

# Main game loop
running = True
game_over = False
add_enemy()  


start_screen()

# Get player name
player_name = get_player_name()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADD_ENEMY_EVENT and not game_over:
            add_enemy()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= CAR_SPEED
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - CAR_WIDTH:
            player_x += CAR_SPEED

        screen.fill(GREY)  # Clear screen and set background color

        draw_lanes()  # Draw lane lines
        move_enemies()
        draw_enemies()
        draw_player()
        draw_score()

        if check_collision():
            game_over_sound.play()  # Play game over sound effect
            player_history.append({"name": player_name, "score": score})
            game_over = True

        increase_difficulty()
    else:
        screen.fill(BLACK)
        restart_button, quit_button = game_over_screen()
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        if restart_button.collidepoint(mouse_pos) and mouse_click[0]:
            reset_game()
            game_over = False
            player_name = get_player_name()  # Ask for player name again
            start_screen()  # Play start sound again
        elif quit_button.collidepoint(mouse_pos) and mouse_click[0]:
            running = False

    pygame.display.flip()  
    clock.tick(FPS)

pygame.quit()
sys.exit()

