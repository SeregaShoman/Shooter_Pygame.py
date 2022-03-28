import pygame
import os 
from os import path
import random

###############
#Resolution and Game Settings
WIDTH = 1920
HEIGHT = 1080
FPS = 80
###############
###############
# Setting the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (255, 255, 0)
###############

# Creating a game and a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
#папка ассетов
img_dir = path.join(path.dirname(__file__), 'img')
font_name = pygame.font.match_font('arial')#ШРИФТ
snd_dir = path.join(path.dirname(__file__), 'snd')

###############
#Screen text and font function
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#HP BAR
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 15
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
#LIFE COUNTER
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 35 * i
        img_rect.y = y
        surf.blit(img, img_rect)
###############
#Menu
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "HELLO", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "ARROWS MOVE SPACE TO SHOOT", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "PRESS ANY BUTTON TO CONTINUE", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#Loading all game graphics
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
background = pygame.image.load(path.join(img_dir, 'space1.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip2_red.png")).convert()
#player_img = pygame.image.load(path.join(img_dir, "pop.png")).convert()
hp_img = pygame.image.load(path.join(img_dir, "live.png")).convert()
hp_mini_img = pygame.transform.scale(hp_img, (25, 19))
hp_mini_img.set_colorkey(WHITE)
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ
bullet_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ
bullet_bust_img = pygame.image.load(path.join(img_dir, "laserGreen12.png")).convert()####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ####ПУЛИ
#########
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))#НАДИ СВУКИ ЖОПА
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'Pew__003.ogg'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'leha.ogg'))
#pygame.mixer.music.set_volume()
######
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
######
meteor_images = []
#meteor_list = ['satana.png']
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png',  
'meteorBrown_big3.png',  'meteorBrown_big4.png',  
'meteorBrown_med1.png',  'meteorBrown_med3.png']  
#'meteorBrown_small1.png',  'meteorBrown_small2.png',  'meteorBrown_small2.png', 'meteorBrown_tiny2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []#об игрока
explosion_anim['sm'] = []#моб
explosion_anim['player'] = []#ИГРОК
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = "sonicExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

class Player(pygame.sprite.Sprite):
    def __iter__(self):
        return self

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (80, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 29
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.lives = 3
        self.hidden = False
        self.last_shot = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        POWERUP_TIME = 7000
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet) 
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet_UP(self.rect.left, self.rect.centery)
                bullet2 = Bullet_UP(self.rect.right, self.rect.centery)
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet)
                bullets.add(bullet) 
                bullets.add(bullet1)
                bullets.add(bullet2)
                power_sound.play()
                shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __iter__(self):
        return self

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rotate()
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Bullet_UP(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_bust_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()



class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()
bullets1 = pygame.sprite.Group()
mobs = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites.add(bullets1)


def newmob():
    m = (Mob())
    all_sprites.add(m)
    mobs.add(m)
score = 0
pygame.mixer.music.play(loops=-1)

game_over = True
running = True
for i in range(15):
    newmob()

while running:
    all_sprites.update() 
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius / 2
        expl = Explosion(hit.rect.center, 'sm')
        random.choice(expl_sounds).play()
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:   
            death_explosion = Explosion(player.rect.center, 'player') 
            random.choice(expl_sounds).play()
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1 
            player.shield = 100
        if player.lives == 0 and not death_explosion.alive():
            running = False
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "shield":
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(15):
            newmob()
        score = 0
    
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH / 2, 10)
    draw_shield_bar(screen, 10, 10, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, hp_mini_img)
    pygame.display.flip()

pygame.quit()