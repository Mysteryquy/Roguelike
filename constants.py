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


#Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_DARK_GREY = (50, 50, 50)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

#game colors
COLOR_DEFAULT_BG = COLOR_GREY


#SPRITES

S_PLAYER = pygame.image.load("data/sprites/python.png")
S_ENEMY = pygame.image.load("data/sprites/enemy1.png")

S_WALL = pygame.image.load("data/sprites/wall2.jpg")
S_WALLEXPLORED = pygame.image.load("data/sprites/wallunseen.png")

S_FLOOR = pygame.image.load("data/sprites/floor.jpg")
S_FLOOREXPLORED = pygame.image.load("data/sprites/floorunseen.png")

#FOV SETTINGS Er hat anstelle der Null "libcod.FOV_BASIC" da stehen
FOV_ALGO = libtcodpy.FOV_RESTRICTIVE
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 5

#FONT SETTINGS
FONT_DEBUG_MESSAGE = pygame.font.Font("data/joystix.ttf", 20)
FONT_MESSAGE_TEXT = pygame.font.Font("data/joystix.ttf", 12)

#MESSAGE DEFAULTS
NUM_MESSAGES = 4
