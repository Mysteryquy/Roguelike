import pygame
import tcod as libtcodpy

pygame.init()

CAMERA_WIDTH = 1000
CAMERA_HEIGHT = 800
CELL_WIDTH = 32
CELL_HEIGHT = 32

#Map limitations
MAP_WIDTH = 20
MAP_HEIGHT = 20
MAP_MAX_NUM_ROOMS = 10
MAP_NUM_LEVELS = 2


#Room limitations
ROOM_MAX_HEIGHT = 7
ROOM_MAX_WIDTH = 3
ROOM_MIN_HEIGHT = 5
ROOM_MIN_WIDTH = 3


#FPS LIMIT
GAME_FPS = 60

INVENTORY_TEXT_HEIGHT = 20

END_GAME_ITEM_NAME = "Orb of Mystery" \
                     ""


#Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_DARK_GREY = (50, 50, 50)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

#game colors
COLOR_DEFAULT_BG = COLOR_GREY



#FOV SETTINGS Er hat anstelle der Null "libcod.FOV_BASIC" da stehen
FOV_ALGO = libtcodpy.FOV_RESTRICTIVE
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 5

#FONT SETTINGS
FONT_DEBUG_MESSAGE = pygame.font.Font("data/joystix.ttf", 20)
FONT_MESSAGE_TEXT = pygame.font.Font("data/joystix.ttf", 12)

#MESSAGE DEFAULTS
NUM_MESSAGES = 4

# DEPTH
DEPTH_PLAYER = -100
DEPTH_CREATURE = 1
DEPTH_ITEM = 2
DEPTH_CORPSE = 100
DEPTH_STRUCTURES = 101

#xp related stuff
XP_NEEDED = {
    1: 400,
    2: 600,
    3: 1000
}
MAX_LEVEL = 3