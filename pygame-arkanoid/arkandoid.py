import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, K_p

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

uruchomiona = True
pause = False
HEALTH_LVL = 3


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


class Klocek(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((20, 10))
        self.surf = pygame.image.load("images/klocek.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))

    def set_kolor(self, color):
        self.surf.fill(color)


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load("images/pilka.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))


class Health(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((5, 5))
        self.surf = pygame.image.load("images/pilka.png").convert()
        self.rect = self.surf.get_rect(center=(x, y))

    def set_kolor(self, color):
        self.surf.fill(color)


pygame.display.set_caption("Arkanoid d_siemieniuk")

player = Player(305, 450)

klocek = Klocek(40, 40)

ball = Ball(315, 440)

health_icons = [Health(100, 15), Health(110, 15), Health(120, 15)]

klocki = pygame.sprite.Group()
klocki.add(klocek)

health = pygame.sprite.Group()
for health_icon in health_icons:
    health.add(health_icon)

font = pygame.font.SysFont('Arial MS', 20)


def generate_level():
    pass


def update_ball_position():
    pass


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

while uruchomiona:

    if HEALTH_LVL <= 0:
        uruchomiona = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

    for klocek in klocki:
        screen.blit(klocek.surf, klocek.rect)
    screen.blit(player.surf, player.rect)
    screen.blit(ball.surf, ball.rect)

    screen.blit(font.render('HEALTH:', False, (255, 255, 255)), (20, 10))
    for n, health_icon in enumerate(health):
        if n < HEALTH_LVL:
            screen.blit(health_icon.surf, health_icon.rect)

    if pygame.sprite.spritecollideany(ball, klocki):
        delete_klocek = pygame.sprite.spritecollideany(ball, klocki)
        delete_klocek.kill()
        # usuniecie klocka

    clock.tick(60)
    pygame.display.flip()
    # pygame.display.update()

pygame.quit()
