import pygame
import tcod as libtcodpy

pygame.init()

GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

#Mapvars
MAP_WIDTH = 50
MAP_HEIGHT = 50
MAP_MAX_NUM_ROOMS = 10


#Room limitations
ROOM_MAX_HEIGHT = 7
ROOM_MAX_WIDTH = 5
ROOM_MIN_HEIGHT = 3
ROOM_MIN_WIDTH = 3

#FPS LIMIT
GAME_FPS = 60

INVENTORY_TEXT_HEIGHT = 20


#Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

#game colors
COLOR_DEFAULT_BG = COLOR_GREY


#SPRITES

S_PLAYER = pygame.image.load("data/python.png")
S_ENEMY = pygame.image.load("data/enemy1.png")

S_WALL = pygame.image.load("data/wall2.jpg")
S_WALLEXPLORED = pygame.image.load("data/wallunseen.png")

S_FLOOR = pygame.image.load("data/floor.jpg")
S_FLOOREXPLORED = pygame.image.load("data/floorunseen.png")

#FOV SETTINGS Er hat anstelle der Null "libcod.FOV_BASIC" da stehen
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

#FONT SETTINGS
FONT_DEBUG_MESSAGE = pygame.font.Font("data/joystix.ttf", 20)
FONT_MESSAGE_TEXT = pygame.font.Font("data/joystix.ttf", 12)

#MESSAGE DEFAULTS
NUM_MESSAGES = 4
