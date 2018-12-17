import pygame
import random
import sys
from os import path
import math

img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')

WIDTH = 640
HEIGHT = 480
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("K.M.I.O.")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('ARCADECLASSIC')

def main_menu():
    global screen

    menu_song = pygame.mixer.music.load(path.join(sound_folder, 'kmio.xm'))
    pygame.mixer.music.play(-1)

    title = pygame.image.load(path.join(img_dir, "kmio.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)
    screen.blit(title, (0,0))
    pygame.display.update()
    draw_text(screen, "Press Enter to Begin", 30, WIDTH/2, HEIGHT/2)
    draw_text(screen, "or Q to Quit", 30, WIDTH/2, (HEIGHT/2)+40)
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                pygame.mixer.music.stop()
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
            else:
                pygame.display.update()

    ready = pygame.mixer.Sound(path.join(sound_folder, 'Go sound.wav'))
    ready.play()
    screen.fill(BLACK)
    draw_text(screen, "Get Ready!", 40, WIDTH/2, HEIGHT/2)
    pygame.display.update()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(60, 48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
             self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.speedy = 0
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        sprites.add(bullet)
        bullets.add(bullet)
        shooting_sound.play()


class EBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
        self.speedx = 10


    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = 10


    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (80, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 8)
        self.move_to_player(player)
        if self.rect.x >= player.rect.x - 10 or self.rect.x <= player.rect.x + 10:
            self.shoot()
        if self.rect.y >= player.rect.y - 10 or self.rect.y <= player.rect.y + 10:
            self.shoot()

    def move_to_player(self, player):
        self.dx = self.rect.x - player.rect.x
        self.dy = self.rect.y - player.rect.y
        dist = math.sqrt(self.dx  ** 2 + self.dy  ** 2)

        try:
            self.dx = self.dx / dist
            self.dy = self.dy / dist
        except ZeroDivisionError:
            dist = 1
        self.rect.x += self.dx * self.speedx
        self.rect.y += self.dy * self.speedy


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = EBullet(self.rect.centerx, self.rect.bottom)
            sprites.add(bullet)
            enemy.add(bullet)




background = pygame.image.load(path.join(img_dir, 'KBO_HiRes_CROP.jpg'))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'KMIO_ship.png'))
enemy_img = pygame.image.load(path.join(img_dir, 'ufo.png'))
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))


sprites = pygame.sprite.Group()
enemy = pygame.sprite.Group()
player = Player()
bullets = pygame.sprite.Group()
sprites.add(player)


for i in range(8):
    m = Enemy()
    sprites.add(m)
    enemy.add(m)
running = True
menu_display = True
while running:

    if menu_display:
        main_menu()
        pygame.time.wait(3000)

        #Stop menu music
        pygame.mixer.music.stop()
        #Play the gameplay music
        pygame.mixer.music.load(path.join(sound_folder, 'kmio level 1.xm'))
        pygame.mixer.music.play(-1)

        menu_display = False

    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    sprites.update()

    hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
    for hit in hits:
            m  = Enemy()
            sprites.add(m)
            enemy.add(m)

    hits = pygame.sprite.spritecollide(player, enemy, False)
    if hits:
        running = False

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
