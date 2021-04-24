import random
import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, K_p, \
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from enum import Enum
from game_settings import *

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial MS', 20)


class BallDirections(Enum):
    x_LEFT = 1
    x_RIGHT = 2
    y_UP = 3
    y_DOWN = 4


ball_x = BallDirections.x_LEFT
ball_y = BallDirections.y_UP

game_score = 0
best_scores = [0, 0, 0, 0, 0]
click = False


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((30, 10))
        self.surf.fill((255, 0, 0))
        self.surf = pygame.image.load("images/belka.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-3, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Brick(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.surf = pygame.image.load("images/klocek.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))
        self.x = x
        self.y = y

    def set_color(self, color):
        self.surf.fill(color)


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((BALL_R, BALL_R))
        self.surf.fill(white)
        self.surf = pygame.image.load("images/pilka.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))
        self.x = x
        self.y = y

    def update(self):
        global ball, ball_x, ball_y, health_lvl

        if ball_x == BallDirections.x_LEFT:
            ball.x -= ball_speed
            if ball.x < BALL_R:
                ball_x = BallDirections.x_RIGHT

        if ball_y == BallDirections.y_DOWN:
            ball.y += ball_speed
            if ball.y >= SCREEN_HEIGHT - BALL_R:
                ball_y = BallDirections.y_UP
                health_lvl -= 1

        if ball_y == BallDirections.y_UP:
            ball.y -= ball_speed
            if ball.y < GAME_BORDER:
                ball_y = BallDirections.y_DOWN

        if ball_x == BallDirections.x_RIGHT:
            ball.x += ball_speed
            if ball.x > SCREEN_WIDTH - BALL_R:
                ball_x = BallDirections.x_LEFT

        self.rect = self.surf.get_rect(center=(self.x, self.y))


class Health(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((5, 5))
        self.surf = pygame.image.load("images/pilka.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))

    def set_color(self, color):
        self.surf.fill(color)


pygame.display.set_caption("Arkanoid d_siemieniuk")

player = Player(305, 450)
ball = Ball(315, 440)

health_icons = [Health(100 + 10 * i, 15) for i in range(health_lvl)]
health = pygame.sprite.Group()
for health_icon in health_icons:
    health.add(health_icon)

bricks = pygame.sprite.Group()


def generate_level():
    global bricks, lvl, ball_speed, player, ball

    player = Player(305, 450)
    ball = Ball(315, 440)
    bricks = pygame.sprite.Group()
    rows = 5
    max_number_of_bricks = int((SCREEN_WIDTH - BRICK_WIDTH) / BRICK_WIDTH)

    for row in range(rows):
        brick_pattern = [random.randrange(3) for i in
                         range(max_number_of_bricks + 1)]  # 1/3 chance
        brick_locations = [
            Brick(1 / 2 * BRICK_WIDTH + i * BRICK_WIDTH,
                  GAME_BORDER + (row * BRICK_HEIGHT))
            for i in range(len(brick_pattern)) if brick_pattern[i] == 1]
        for brick in brick_locations:
            bricks.add(brick)
    ball_speed += 0.5 * lvl


def text_objects(font, text, color, text_center):
    rendered = font.render(text, True, color)
    return rendered, rendered.get_rect(center=text_center)


def button(text, pos_x, pos_y, width, height, color, hover_color, action=None,
           text_color=black):
    global click
    mouse = pygame.mouse.get_pos()
    if pos_x + width > mouse[0] > pos_x and pos_y + height > mouse[1] > pos_y:
        pygame.draw.rect(screen, hover_color, (pos_x, pos_y, width, height))
        if click and action is not None:
            click = False
            action()
    else:
        pygame.draw.rect(screen, color, (pos_x, pos_y, width, height))
    screen.blit(*text_objects(font, text, text_color,
                              (pos_x + width / 2, pos_y + height / 2)))


def resume():
    global paused
    paused = False


def quit_game():
    global running
    running = False


# pygame.mixer.music.load("sounds/intro.mp3")
# pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play(-1)

def detect_collision():
    global ball, player, ball_x, ball_y
    if ball.rect.colliderect(player):
        ball_y = BallDirections.y_UP


def detect_brick_collision():
    global ball_x, ball_y, game_score

    if pygame.sprite.spritecollideany(ball, bricks):
        brick_to_delete = pygame.sprite.spritecollideany(ball, bricks)
        brick_to_delete.kill()
        game_score += POINTS_PER_BRICK

        if ball_y == BallDirections.y_UP:
            if ball.y == (brick.y + 20 - ball_speed):
                ball_y = BallDirections.y_DOWN
            else:
                if ball_x == BallDirections.x_LEFT:
                    ball_x = BallDirections.x_RIGHT
                else:
                    ball_x = BallDirections.x_LEFT
        else:
            if ball.y <= brick.y:
                ball_y = BallDirections.y_UP
            else:
                if ball_x == BallDirections.x_LEFT:
                    ball_x = BallDirections.x_RIGHT
                else:
                    ball_x = BallDirections.x_LEFT


def next_level():
    global lvl_won, lvl
    lvl_won = False
    lvl += 1
    generate_level()
    print("LEVEL: ", lvl)
    print("ball speed: ", ball_speed)


def reset_game():
    global display_menu, game_lost, game_won, lvl_won, paused, score_menu
    global health_lvl, lvl, ball_speed, game_score

    display_menu = True
    game_lost = False
    game_won = False
    lvl_won = False
    paused = False
    score_menu = False
    health_lvl = HEALTH_LVL
    lvl = LVL
    ball_speed = BALL_SPEED
    game_score = 0


def display_main_menu():
    if paused or lvl_won:
        save_game_score()
    reset_game()
    screen.fill(dark_grey)
    button("NEW GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 - 35, 150, 50,
           light_grey, light_blue, play_game)
    button("SCORES", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 25, 150, 50,
           light_grey, light_blue, display_highest_scores_menu)
    button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 85, 150,
           50, light_grey, light_orange, quit_game)


def play_game():
    global display_menu
    display_menu = False
    next_level()


def pause():
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    s.set_alpha(5)
    s.fill(light_grey)
    screen.blit(s, (0, 0))

    button("CONTINUE", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 - 35, 150, 50,
           light_grey, light_blue, resume)
    button("MAIN MENU", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 25, 150, 50,
           light_grey, light_blue, display_main_menu)
    button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 85, 150,
           50, light_grey, light_orange, quit_game)


def back_to_main_menu():
    global display_menu, score_menu
    display_menu = True
    score_menu = False


def display_highest_scores_menu():
    global display_menu, score_menu
    display_menu = False
    score_menu = True

    screen.fill(dark_grey)
    button("HIGHEST SCORES:", SCREEN_WIDTH / 2 - 75, 10, 150, 50,
           light_blue, light_blue)
    button("MAIN MENU", SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT - 100, 150, 50,
           light_grey, light_blue, back_to_main_menu)
    button("QUIT GAME", SCREEN_WIDTH / 2 + 10, SCREEN_HEIGHT - 100, 150,
           50, light_grey, light_orange, quit_game)

    for n, score in enumerate(best_scores):
        screen.blit(font.render(str(n) + ": " + str(score), False, light_orange),
                    (SCREEN_WIDTH / 2 - 10, 100 + 20 * n))


def save_game_score():
    global best_scores, game_score
    if len(bricks) == 0 and health_lvl == HEALTH_LVL:
        game_score += 500  # bonus
    if game_score not in best_scores:
        all_scores = best_scores.copy()
        all_scores.append(game_score)
        best_scores = sorted(all_scores, reverse=True)[0:5]


def display_game_lost_menu():
    screen.fill(dark_grey)
    button("YOU LOST!", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 - 35, 150, 50,
           light_grey, light_grey)
    button("MAIN MENU", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 25, 150, 50,
           light_grey, light_blue, display_main_menu)
    button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 85, 150,
           50, light_grey, light_orange, quit_game)


def display_game_won_menu():
    screen.fill(dark_grey)
    button("YOU WON!!!", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 - 35, 150, 50,
           light_grey, light_grey)
    button("MAIN MENU", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 25, 150, 50,
           light_grey, light_blue, display_main_menu)
    button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 85, 150,
           50, light_grey, light_orange, quit_game)


def display_lvl_won_menu():
    screen.fill(dark_grey)
    button("NEXT LEVEL", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 - 35, 150, 50,
           light_grey, light_blue, next_level)
    button("MAIN MENU", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 25, 150, 50,
           light_grey, light_blue, display_main_menu)
    button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 3 + 85, 150,
           50, light_grey, light_orange, quit_game)


while running:

    if not display_menu:

        if health_lvl <= 0:
            game_lost = True

        if len(bricks) == 0 and health_lvl > 0 and game_score > 0:
            if lvl >= MAX_LVL:
                game_won = True
            else:
                lvl_won = True

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key in (K_ESCAPE, K_p):
                paused = not paused
        elif event.type == MOUSEBUTTONDOWN:
            click = True

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    if display_menu:
        display_main_menu()
    elif score_menu:
        display_highest_scores_menu()
    elif paused:
        pause()
    elif game_lost:
        save_game_score()
        display_game_lost_menu()
    elif game_won:
        save_game_score()
        display_game_won_menu()
    elif lvl_won:
        display_lvl_won_menu()
    else:
        screen.fill(dark_grey)

        for brick in bricks:
            screen.blit(brick.surf, brick.rect)
        screen.blit(player.surf, player.rect)
        screen.blit(ball.surf, ball.rect)

        screen.blit(font.render('HEALTH:', False, light_orange), (20, 10))
        for n, health_icon in enumerate(health):
            if n < health_lvl:
                screen.blit(health_icon.surf, health_icon.rect)
        screen.blit(font.render('LEVEL: ' + str(lvl), False, light_orange), (150, 10))
        screen.blit(font.render('BALL SPEED: ' + str(ball_speed), False, light_orange),
                    (230, 10))
        screen.blit(font.render('SCORE: ' + str(game_score), False, white), (360, 10))

        detect_brick_collision()
        ball.update()
        detect_collision()

    clock.tick(60)
    pygame.display.flip()
pygame.quit()
