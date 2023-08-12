
import pygame, sys, time, random


# Difficulty settings
# Easy      ->  10
# Medium    ->  30
# Hard      ->  60

difficulty = 10

# Size of window
frame_size_x = 720
frame_size_y = 480

# Checking for errors 
errors = pygame.init()
if errors[1] > 0:
    print(f'[!] Had {errors[1]} errors while initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialising the game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colours 
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(255, 0, 0)
red = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# Frames per second (fps) controller
fps_controller = pygame.time.Clock()


# Variables used in game
position_snake = [100, 50]
body_snake= [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# End of game
def game_over():
    my_font = pygame.font.SysFont('cascadia code', 90)
    game_over_surface = my_font.render('YOU ARE DEAD', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


# Main logic of game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # When a key is pressed
        elif event.type == pygame.KEYDOWN:
            # u -> Up; d -> Down; l -> Left; r -> Right
            if event.key == pygame.K_UP or event.key == ord('u'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('d'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('l'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('r'):
                change_to = 'RIGHT'
            # Esc -> used to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Movement of the snake
    if direction == 'UP':
        position_snake[1] -= 10
    if direction == 'DOWN':
        position_snake[1] += 10
    if direction == 'LEFT':
        position_snake[0] -= 10
    if direction == 'RIGHT':
        position_snake[0] += 10

    # Growth of Snake body 
    body_snake.insert(0, list(position_snake))
    if position_snake[0] == food_pos[0] and position_snake[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        body_snake.pop()

    # Spawning food 
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    
    game_window.fill(black)
    for pos in body_snake:
        # Body of snake
        pygame.draw.rect(game_window, red, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Conditions for end of game
    # Getting out of bounds
    if position_snake[0] < 0 or position_snake[0] > frame_size_x-10:
        game_over()
    if position_snake[1] < 0 or position_snake[1] > frame_size_y-10:
        game_over()
    # When the snake body touches the boundary
    for block in body_snake[1:]:
        if position_snake[0] == block[0] and position_snake[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)