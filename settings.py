import pygame as pg

# game settings
TITLE = "The Depths Below"
WIDTH = 1024
HEIGHT = 768
FPS = 30

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BROWN = (104, 55, 5)

# Background Color
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
SCALE = TILESIZE // 16

# player settings
PLAYER_SPEED = 275
PLAYER_ROTSPEED = 250
PLAYER_HIT_RECT = pg.Rect(0, 0, 64, 80)

# Other settings
caption_frames = True # Caption_Frames, shows FPS in Caption
grid = True

# Sprites
SPRITESHEET = "Dungeon_tiles.png"
