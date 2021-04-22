import random
import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, K_p
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
        if self.rect.right > SCREEN_WIDTH - 30:
            self.rect.right = SCREEN_WIDTH - 30


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
        self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load("images/pilka.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))
        self.x = x
        self.y = y

    def update(self):
        global ball, ball_x, ball_y, HEALTH_LVL

        if ball_x == BallDirections.x_LEFT:
            ball.x -= ball_speed
            if ball.x < BALL_R:
                ball_x = BallDirections.x_RIGHT

        if ball_y == BallDirections.y_DOWN:
            ball.y += ball_speed
            if ball.y >= SCREEN_HEIGHT - BALL_R:
                ball_x = BallDirections.x_LEFT
                ball_y = BallDirections.y_UP
                HEALTH_LVL -= 1

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

health_icons = [Health(100 + 10 * i, 15) for i in range(HEALTH_LVL)]
health = pygame.sprite.Group()
for health_icon in health_icons:
    health.add(health_icon)

bricks = pygame.sprite.Group()


def generate_level():
    global bricks, GAME_LVL, ball_speed, player, ball

    player = Player(305, 450)
    ball = Ball(315, 440)
    bricks = pygame.sprite.Group()
    rows = 7
    max_number_of_bricks = int((SCREEN_WIDTH - BRICK_WIDTH) / BRICK_WIDTH)

    for row in range(rows):
        brick_pattern = [random.randrange(2) for i in range(max_number_of_bricks + 1)]
        brick_locations = [
            Brick(1 / 2 * BRICK_WIDTH + i * BRICK_WIDTH,
                  GAME_BORDER + (row * BRICK_HEIGHT))
            for i in range(len(brick_pattern)) if brick_pattern[i] == 1]
        for brick in brick_locations:
            bricks.add(brick)

    ball_speed += GAME_LVL


def text_objects(font, text, color, text_center):
    rendered = font.render(text, True, color)
    return rendered, rendered.get_rect(center=text_center)


def button(text, pos_x, pos_y, width, heigth, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if pos_x + width > mouse[0] > pos_x and pos_y + heigth > mouse[1] > pos_y:
        pygame.draw.rect(screen, hover_color, (pos_x, pos_y, width, heigth))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (pos_x, pos_y, width, heigth))
    screen.blit(*text_objects(font, text, (0, 0, 0),
                              (pos_x + width / 2, pos_y + heigth / 2)))


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
    global ball_x, ball_y

    if pygame.sprite.spritecollideany(ball, bricks):
        brick_to_delete = pygame.sprite.spritecollideany(ball, bricks)
        brick_to_delete.kill()

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
    global lvl_won, LVL
    lvl_won = False
    LVL += 1
    generate_level()
    print("LEVEL: ", LVL)
    print("ball speed: ", ball_speed)


next_level()

while running:

    if HEALTH_LVL <= 0:
        game_lost = True

    if len(bricks) == 0 and HEALTH_LVL > 0:
        if LVL >= MAX_LVL:
            game_won = True
        else:
            lvl_won = True

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key in (K_ESCAPE, K_p):
                paused = not paused

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    if paused:
        screen.fill((255, 255, 255))
        button("CONTINUE", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 - 50, 150, 50,
               (0, 255, 0), (0, 0, 255), resume)
        button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 + 10, 150,
               50, (255, 0, 0), (0, 0, 255), quit_game)
    elif game_lost:
        screen.fill((0, 0, 0))
        button("YOU LOST!", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 - 50, 150, 50,
               (0, 0, 255), (0, 0, 255))
        button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 + 10, 150,
               50, (255, 0, 0), (0, 0, 255), quit_game)
    elif game_won:
        screen.fill((0, 0, 0))
        button("YOU WON!!!", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 - 50, 150, 50,
               (0, 0, 255), (0, 0, 255))
        button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 + 10, 150,
               50, (255, 0, 0), (0, 0, 255), quit_game)
    elif lvl_won:
        screen.fill((0, 0, 0))
        button("NEXT LEVEL", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 - 50, 150, 50,
               (0, 255, 0), (0, 0, 255), next_level)
        button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 + 10, 150,
               50, (255, 0, 0), (0, 0, 255), quit_game)
    else:
        screen.fill((0, 0, 0))

        for brick in bricks:
            screen.blit(brick.surf, brick.rect)
        screen.blit(player.surf, player.rect)
        screen.blit(ball.surf, ball.rect)

        screen.blit(font.render('HEALTH:', False, (255, 255, 255)), (20, 10))
        for n, health_icon in enumerate(health):
            if n < HEALTH_LVL:
                screen.blit(health_icon.surf, health_icon.rect)

        detect_brick_collision()
        ball.update()
        detect_collision()

    clock.tick(60)
    pygame.display.flip()
    # pygame.display.update()

pygame.quit()
