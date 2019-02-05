import pygame as pg
import random, sys
from settings import *
from map_build import hit_rect_collide
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()
        
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * SCALE, height * SCALE))
        return image
        

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.run = False
        self.hit = False
        self.last_dir = 'r'
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        
    def load_images(self):                                  #X   #Y   #W  #H
        self.idle_frames = [self.game.spritesheet.get_image(128, 100, 16, 28),
                            self.game.spritesheet.get_image(144, 100, 16, 28),
                            self.game.spritesheet.get_image(160, 100, 16, 28),
                            self.game.spritesheet.get_image(176, 100, 16, 28)]
        self.idle_frames_flip = []
        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
            self.idle_frames_flip.append(pg.transform.flip(frame, True, False))
        self.run_frames_r = [self.game.spritesheet.get_image(192, 100, 16, 28),
                             self.game.spritesheet.get_image(208, 100, 16, 28),
                             self.game.spritesheet.get_image(224, 100, 16, 28),
                             self.game.spritesheet.get_image(240, 100, 16, 28)]
        self.run_frames_l = []
        for frame in self.run_frames_r:
            frame.set_colorkey(BLACK)
            self.run_frames_l.append(pg.transform.flip(frame, True, False))
        self.hit_frame = self.game.spritesheet.get_image(256, 100, 16, 28)
        self.hit_frame.set_colorkey(BLACK)
        self.hit_frame_flip = self.hit_frame

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel += vec(-PLAYER_SPEED, 0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel += vec(PLAYER_SPEED, 0)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel += vec(0, -PLAYER_SPEED)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel += vec(0, PLAYER_SPEED)
        if self.vel.x != 0:
            if self.vel.y != 0:
                self.vel.x * .7071
                self.vel.y * .7071

    def cww(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, hit_rect_collide)
            if hits:
                    if self.vel.x > 0:
                        self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
                    if self.vel.x < 0:
                        self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
                    self.vel.x = 0
                    self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, hit_rect_collide)
            if hits:
                    if self.vel.y > 0:
                        self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
                    if self.vel.y < 0:
                        self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2
                    self.vel.y = 0
                    self.hit_rect.centery = self.pos.y
            

    def update(self):
        self.animate()
        self.get_keys()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.cww('x')
        self.hit_rect.centery = self.pos.y
        self.cww('y')
        self.rect.center = self.hit_rect.center
        
    def animate(self):
        now = pg.time.get_ticks()
        # check if running
        if self.vel.x != 0 or self.vel.y != 0:
            self.run = True
        else:
            self.run = False
        # Run animation
        if self.run:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_frames_l)
                if self.vel.x < 0:
                    self.image = self.run_frames_l[self.current_frame]
                    self.last_dir = 'l'
                elif self.vel.x == 0:
                    if self.last_dir is "l":
                        self.image = self.run_frames_l[self.current_frame]
                    else:
                        self.image = self.run_frames_r[self.current_frame]
                else:
                    self.image = self.run_frames_r[self.current_frame]
                    self.last_dir = 'r'
        # Idle animation
        if not self.hit and not self.run:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                if self.last_dir is "r":
                    self.image = self.idle_frames[self.current_frame]
                else:
                    self.image = self.idle_frames_flip[self.current_frame]

class Skelet(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.skelets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.chase = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames_r[0]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        
    def load_images(self):                                    #X   #Y  #W  #H
        self.idle_frames_r = [self.game.spritesheet.get_image(368, 80, 16, 16),
                              self.game.spritesheet.get_image(384, 80, 16, 16),
                              self.game.spritesheet.get_image(400, 80, 16, 16),
                              self.game.spritesheet.get_image(416, 80, 16, 16)]
        self.idle_frames_l = []
        for frame in self.idle_frames_r:
            frame.set_colorkey(BLACK)
            self.idle_frames_l.append(pg.transform.flip(frame, True, False))
        self.run_frames_r = [self.game.spritesheet.get_image(432, 80, 16, 16),
                             self.game.spritesheet.get_image(448, 80, 16, 16),
                             self.game.spritesheet.get_image(464, 80, 16, 16),
                             self.game.spritesheet.get_image(480, 80, 16, 16)]
        self.run_frames_l = []
        for frame in self.run_frames_r:
            frame.set_colorkey(BLACK)
            self.run_frames_l.append(pg.transform.flip(frame, True, False))
        

    def update(self):
        self.animate()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(32, 16, 16, 16)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
