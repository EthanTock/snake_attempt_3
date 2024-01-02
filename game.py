import pygame
import time
import random

MAX_HEIGHT = 720
MAX_WIDTH = 720
EYE_RADIUS = 5
EYE_DISTANCE = 10
SEGMENT_RADIUS = 40
APPLE_RADIUS = 10
FRAMERATE = 7

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((MAX_HEIGHT, MAX_WIDTH))
pygame.display.set_caption("Snake Attempt 3")
clock = pygame.time.Clock()
running = True
dt = 0

old_keys = pygame.key.get_pressed()
new_direction = "none"
current_direction = "none"
old_frame_advance_time = time.time()


# this gives me an idea for a timer class...
def has_time_passed(time_amt, old_time):
    return time.time() - old_time > time_amt


def send_in_direction(vec2, d, distance):
    if d == "up":
        vec2.y -= distance
    elif d == "down":
        vec2.y += distance
    elif d == "left":
        vec2.x -= distance
    elif d == "right":
        vec2.x += distance


def get_random_color():
    return random.choice(list(pygame.color.THECOLORS.values()))


bg_color = pygame.color.THECOLORS["gray20"]
text_color = pygame.color.THECOLORS["antiquewhite"]

head_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
snake = [(head_pos, get_random_color())]
old_snake = [seg[0].copy() for seg in snake]
score = len(snake)
alive = True
eye_color = get_random_color()


def get_segment_positions():
    return [(seg[0].x, seg[0].y) for seg in snake]


def get_open_spaces():
    open_spaces = []
    for y in range(SEGMENT_RADIUS, MAX_HEIGHT, SEGMENT_RADIUS * 2):
        open_spaces.extend([(x, y) for x in range(SEGMENT_RADIUS, MAX_WIDTH, SEGMENT_RADIUS * 2) if (x, y) not in get_segment_positions()])
    return open_spaces


def create_apple_pos():
    return pygame.Vector2(random.choice(get_open_spaces()))


def get_score():
    return len(snake)


apple_eaten = True
apple_pos = (0, 0)
apple_color = get_random_color()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bg_color)

    for segment in snake:
        pygame.draw.circle(screen, segment[1], segment[0], SEGMENT_RADIUS)

    if current_direction in ("up", "right"):
        pygame.draw.circle(screen, eye_color, (snake[0][0].x + EYE_DISTANCE, snake[0][0].y - EYE_DISTANCE), EYE_RADIUS)
    if current_direction in ("right", "down"):
        pygame.draw.circle(screen, eye_color, (snake[0][0].x + EYE_DISTANCE, snake[0][0].y + EYE_DISTANCE), EYE_RADIUS)
    if current_direction in ("down", "left"):
        pygame.draw.circle(screen, eye_color, (snake[0][0].x - EYE_DISTANCE, snake[0][0].y + EYE_DISTANCE), EYE_RADIUS)
    if current_direction in ("left", "up"):
        pygame.draw.circle(screen, eye_color, (snake[0][0].x - EYE_DISTANCE, snake[0][0].y - EYE_DISTANCE), EYE_RADIUS)

    if apple_eaten:
        apple_pos = create_apple_pos()
        apple_eaten = False
    if has_time_passed(1 / FRAMERATE, old_frame_advance_time):
        apple_color = get_random_color()
    pygame.draw.circle(screen, apple_color, apple_pos, APPLE_RADIUS)

    score_font = pygame.font.Font(None, 32)
    score_text = score_font.render(f"Score: {get_score()}", False, text_color)
    score_text_pos = score_text.get_rect(centerx=MAX_WIDTH/2, y=MAX_HEIGHT-20)
    screen.blit(score_text, score_text_pos)
    pygame.display.set_caption(f"Score: {get_score()}")

    # # constant movement
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_UP]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_DOWN]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_RIGHT]:
    #     player_pos.x += 300 * dt
    # if keys[pygame.K_LEFT]:
    #     player_pos.x -= 300 * dt

    # # stuttered movement
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_UP] and not old_keys[pygame.K_UP]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_DOWN] and not old_keys[pygame.K_DOWN]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_RIGHT] and not old_keys[pygame.K_RIGHT]:
    #     player_pos.x += 300 * dt
    # if keys[pygame.K_LEFT] and not old_keys[pygame.K_LEFT]:
    #     player_pos.x -= 300 * dt
    # old_keys = keys

    # flowing movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and current_direction != "down":
        new_direction = "up"
    elif keys[pygame.K_DOWN] and current_direction != "up":
        new_direction = "down"
    elif keys[pygame.K_RIGHT] and current_direction != "left":
        new_direction = "right"
    elif keys[pygame.K_LEFT] and current_direction != "right":
        new_direction = "left"

    if has_time_passed(1 / FRAMERATE, old_frame_advance_time):
        old_frame_advance_time = time.time()
        old_snake = [(seg[0].copy(), seg[1]) for seg in snake]
        send_in_direction(head_pos, new_direction, SEGMENT_RADIUS * 2)
        current_direction = new_direction
        snake = [(head_pos, get_random_color())]
        snake.extend(old_snake[:-1])
        eye_color = get_random_color()

    if head_pos == apple_pos:
        snake.append(old_snake[-1])
        apple_eaten = True

    # Deaths
    for segment_pos in get_segment_positions()[1:]:
        if head_pos == segment_pos:
            alive = False

    if head_pos.x < 0 or head_pos.y < 0 or head_pos.x > MAX_WIDTH or head_pos.y > MAX_HEIGHT:
        alive = False

    if not alive:
        game_over_font = pygame.font.Font(None, 32)
        game_over_text = game_over_font.render("Game Over!", False, text_color)
        game_over_text_pos = game_over_text.get_rect(centerx=MAX_WIDTH / 2, centery=MAX_HEIGHT / 2)
        screen.blit(game_over_text, game_over_text_pos)
        running = False

    pygame.display.flip()

    dt = clock.tick(60) / 1000

time.sleep(2)
print(f"Final score: {get_score()}")
