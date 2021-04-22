import random
import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, K_p

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BORDER = 10
GAME_BORDER = 40
BRICK_WIDTH = 20
BRICK_HEIGHT = 10
BALL_R = 5

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

uruchomiona = True
pause = False
HEALTH_LVL = 3
ball_speed = 2
ball_x = 'left'
ball_y = 'up'
font = pygame.font.SysFont('Arial MS', 20)


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
        self.surf = pygame.Surface((BALL_R, BALL_R))
        self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load("images/pilka.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))
        self.x = x
        self.y = y

    def update(self):
        global ball, ball_x, ball_y, HEALTH_LVL
        if ball_x == "left":
            ball.x -= ball_speed
            if ball.x < BALL_R:
                ball_x = "right"
        if ball_y == "down":
            ball.y += ball_speed
            if ball.y >= SCREEN_HEIGHT - BALL_R:
                ball_x = "left"
                ball_y = "up"
                HEALTH_LVL -= 1
        if ball_y == "up":
            ball.y -= ball_speed
            if ball.y < GAME_BORDER:
                ball_y = 'down'
        if ball_x == "right":
            ball.x += ball_speed
            if ball.x > SCREEN_WIDTH - BALL_R:
                ball_x = "left"
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

# brick = Brick(40, 40)

bricks = pygame.sprite.Group()
# bricks.add(brick)

# health_icons = [Health(100, 15), Health(110, 15), Health(120, 15)]
health_icons = [Health(100 + 10 * i, 15) for i in range(HEALTH_LVL)]
health = pygame.sprite.Group()
for health_icon in health_icons:
    health.add(health_icon)


def generate_level():
    global bricks
    rows = 7
    max_number_of_bricks = int((SCREEN_WIDTH - 2 * GAME_BORDER) / BRICK_WIDTH)
    for row in range(rows):
        brick_pattern = [random.randrange(2) for i in range(max_number_of_bricks + 1)]
        print(brick_pattern)
        print(len(brick_pattern))
        brick_locations = [
            Brick(GAME_BORDER + i * BRICK_WIDTH, 2*GAME_BORDER + (row * BRICK_HEIGHT))
            for i in range(len(brick_pattern)) if brick_pattern[i] == 1]
        print(len(brick_locations))
        for brick in brick_locations:
            bricks.add(brick)


# def update_ball_position():
#     pass


def text_objects(font, text, color, text_center):
    rendered = font.render(text, True, color)
    return rendered, rendered.get_rect(center=text_center)


def button(text, pos_x, pos_y, width, heigth, color, hover_color, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if pos_x + width > mouse[0] > pos_x and pos_y + heigth > mouse[1] > pos_y:
        pygame.draw.rect(screen, hover_color, (pos_x, pos_y, width, heigth))
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, color, (pos_x, pos_y, width, heigth))
    screen.blit(*text_objects(font, text, (0, 0, 0),
                              (pos_x + width / 2, pos_y + heigth / 2)))


def unpause():
    global pause
    pause = False


def quitgame():
    global uruchomiona
    uruchomiona = False


# pygame.mixer.music.load("sounds/intro.mp3")
# pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play(-1)

def detect_collision():
    global ball, player, ball_x, ball_y
    if ball.rect.colliderect(player):
        print("Player-ball contact detected")
        ball_y = "up"


def detect_brick_collision():
    global ball_x, ball_y
    if pygame.sprite.spritecollideany(ball, bricks):
        brick_to_delete = pygame.sprite.spritecollideany(ball, bricks)
        brick_to_delete.kill()
        # usuniecie klocka

        if ball_y == "up":
            if ball.y == (brick.y + 20 - ball_speed):
                ball_y = "down"
            else:
                if ball_x == "left":
                    ball_x = "right"
                else:
                    ball_x = "left"
        else:
            if ball.y <= brick.y:
                ball_y = "up"
            else:
                if ball_x == "left":
                    ball_x = "right"
                else:
                    ball_x = "left"


generate_level()

while uruchomiona:

    if HEALTH_LVL <= 0:
        uruchomiona = False

    for event in pygame.event.get():
        if event.type == QUIT:
            uruchomiona = False
        elif event.type == KEYDOWN:
            if event.key in (K_ESCAPE, K_p):
                pause = not pause

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    if pause:
        screen.fill((255, 255, 255))
        button("CONTINUE", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 - 50, 150, 50,
               (0, 255, 0), (0, 0, 255), unpause)
        button("QUIT GAME", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 + 10, 150,
               50, (255, 0, 0), (0, 0, 255), quitgame)
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
