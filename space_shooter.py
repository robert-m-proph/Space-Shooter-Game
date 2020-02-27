 
# Robert Propheter | Space Shooter

'''
Copyright appreciated, but not required by the artist for the music. Song is
"Cyberpunk Moonlight Sonata" by Joth

Art graphics from Kenney.nl

Background image is a royalty free photo from http://www.everystockphoto.com

Explosion and laser shooting effects made using BFXR

Art and Music found on opengameart.org
'''

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'image')
snd_dir = path.join(path.dirname(__file__), 'sound')

# Global Variables
WIDTH = 480 # in pixels
HEIGHT = 600 # in pixels
FPS = 60 # frames per second
POWERUP_TIME = 5000 # 5 seconds (3,000 miliseconds)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# initialize pygame and create window
pygame.init()
pygame.mixer.init() # Allows for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Shooter!!')

clock = pygame.time.Clock()


''' Draws text on the screen '''

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

''' Displays the Game Over and Start Screens '''

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, 'Space Shooter!!', 64, WIDTH / 2, HEIGHT / 4.5)
    draw_text(screen, 'Arrow Keys Move', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, 'Spacebar Fires', 22, WIDTH / 2, HEIGHT / 1.7)    
    draw_text(screen, 'Press any key to begin', 18, WIDTH / 2, HEIGHT * 3/4)
    pygame.display.flip()
    
    # While Loop to keep Game Over screen open unless keys pressed
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
                
''' Spawns a new Mob '''

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
 
    
''' Draws and displays the sheild (health) bar '''

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    

''' Draws the Player Lives '''

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        

''' Creating the Sprites '''


''' The good guy (our player) '''

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        
        # Auto fire with the space bar
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
        # Sheild (or health of ship)
        self.shield = 100
        
        # Player Lives
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        
        # Power Level
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        
        
    def update(self):
        # Timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            
        
        # Unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        
        self.speedx = 0
        
        # Makes the game know what keys are pressed
        keystate = pygame.key.get_pressed()       
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        
        self.rect.x += self.speedx
        
        # Makes the left and right walls
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            # 1 Bullet Power Level 1
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            
            # 2 Bullets for Power Level 2
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            
            # 3 Bullets for Power Level 3
            if self.power >= 3:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()                
            
    def hide(self):
        # Hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH /2, HEIGHT + 200)


'''The Mob Sprite (Bad Guys or objects) '''

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .83 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
        # Rotation of meteors
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
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
        
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)            


''' Bullet Sprite '''

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image.set_colorkey(BLACK)        
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

        
''' Power Up Sprites '''
            
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)        
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 7
                    
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()

            
''' Explosion Sprite '''

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
    
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


''' Load all game graphics '''


# Background
background = pygame.image.load(path.join(img_dir, 'stars.png')).convert()
background_rect = background.get_rect()

# Player (ship)
player_img = pygame.image.load(path.join(img_dir, 'playerShip.png')).convert()

# Player Lives (scaled)
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

# Mobs (Meteors)
meteor_images = []
meteor_list = ['meteorBrown1.png', 'meteorBrown2.png', 'meteorBrown3.png',
               'meteorBrown4.png', 'meteorBrown5.png', 'meteorSilver1.png',
               'meteorSilver2.png', 'meteorSilver3.png', 'meteorSilver4.png',
               'meteorSilver5.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# Explosions
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(1, 10):
    filename = 'explosion{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

# Power Ups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

# Lasers
laser_img = pygame.image.load(path.join(img_dir, 'laser.png')).convert()


''' Load all game sounds '''


# Laser shooting sound
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))

# Power Ups
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))

# Explosion sounds 
expl_sounds = []
for snd in ['expl1.wav', 'expl2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

# Player Explosion
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))

# Background Music
pygame.mixer.music.load(path.join(snd_dir, 'Cyberpunk-Moonlight-Sonata.mp3'))

# Sets the volume for the music and sounds
pygame.mixer.music.set_volume(1.5)


''' Game Loop '''


# Keeps the background song in a loop
pygame.mixer.music.play(loops = -1) 

game_over = True
running = True

while running:
    # Game Over Screen to ask User to play again 
    if game_over:
        show_go_screen()
        game_over = False
        
        ''' Sprite Groups '''
        # This section resets everything if User plays again
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        powerups = pygame.sprite.Group()
        
        all_sprites.add(player)
        for i in range(8):
            newmob()           
        score = 0        
        
    # Keep loop running at the right speed
    clock.tick(FPS)
    
    ''' Process input (events) '''
    
    for event in pygame.event.get():
        # Check for closing the window
        if event.type == pygame.QUIT:
            running = False
    
    ''' Update '''
    
    all_sprites.update()
    
    #   - MOB DEATH -   Check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) # Any mobs gets hit, gets deleted
    for hit in hits:
        score += 50 - hit.radius # Adding the score
        random.choice(expl_sounds).play()
        
        # Explosion when mobs gets hit with bullet
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        
        # Spawn a Power Up
        if random.random() > 0.90:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        
        # Spawning new mobs
        newmob()

        
    #   - PLAYER DEATH -   Check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) # comes back as a list
    for hit in hits:
        player.shield -= hit.radius * 2
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide() # removes player sprite from the group
            player.lives -= 1
            player.shield = 100
    
    
    #   - POWER UPS -   Check to see if the player hit a Power Up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play() # Plays shield power up sound
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play() # Plays gun power up sound
            
    
    
    # If the player died and the explosion has finish playing
    if player.lives == 0 and not death_explosion.alive():
        game_over = True # Resets game for Game Over Screen
        
    
    ''' Draw / render '''
    
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    
    # Text
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    
    # Draw Shield Bar
    draw_shield_bar(screen, 5, 5, player.shield)
    
    # Draw the Player Lives
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    
    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()