import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
clock = pygame.time.Clock()

uruchomiona = True

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.surf = pygame.Surface((30,10))
        self.surf.fill((255,0,0))
        self.surf = pygame.image.load("images/belka.png").convert()
        self.rect =  self.surf.get_rect(center=(x, y))

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            print("pressed left")
            self.rect.move_ip(-3,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3,0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH-30:
            self.rect.right = SCREEN_WIDTH-30


class Klocek(pygame.sprite.Sprite):
 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((20,10))
        self.surf = pygame.image.load("images/klocek.png").convert()
        self.rect = self.surf.get_rect(center=(x,y))

    def set_kolor(self, color):
        self.surf.fill(color)


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.surf = pygame.Surface((5,5))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=(x, y))


pygame.display.set_caption("Arkanoid UJ")

player = Player(305,450)

klocek = Klocek(20,20)

ball = Ball(315, 440)  

klocki = pygame.sprite.Group()
klocki.add(klocek)

def generate_level():
    pass

def update_ball_position():
    pass


pygame.mixer.music.load("sounds/intro.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

while uruchomiona:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            uruchomiona = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                uruchomiona = False
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    screen.fill((0,0,0))



    for klocek in klocki:
        screen.blit(klocek.surf, klocek.rect)
    screen.blit(player.surf, player.rect)
    screen.blit(ball.surf, ball.rect)

    if pygame.sprite.spritecollideany(ball, klocki):
        delete_klocek = pygame.sprite.spritecollideany(ball, klocki)
        delete_klocek.kill()
        # usuniecie klocka

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
