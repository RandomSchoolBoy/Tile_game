# Skeleton #2
# Game created by Jordan Hedgecock
import pygame as pg
import sys, random
from os import path
from settings import *
from sprites import *
from map_build import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.running = True

    def load_data(self):
        # The games current folder
        game_folder = path.dirname('__file__')
        # img main branch
        img_folder = path.join(game_folder, 'img')
        ############SPRITESHEET################
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        ############# SOUND ###################
        snd_folder = path.join(game_folder, 'snd')
        ##############LEVELS######################
        lvl_folder = path.join(game_folder, 'Levels')
        ############## MAP #######################
        self.map = Map(path.join(lvl_folder, 'map.txt'))
        
    def new(self):
        # Setup game and classes/sprites
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.skelets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 's':
                    Skelet(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # Game loop (Frames/ticks of the game)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        if caption_frames is True:
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        if grid is True:
            self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 10)
        pg.display.flip()

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                pass

    def show_start_screen(self):
        # Intro/start screen
        pass

    def show_over_screen(self):
        # Death screen
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_over_screen()
            
pg.quit()
