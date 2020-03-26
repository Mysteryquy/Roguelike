import pygame
import tcod as libtcodpy
import math
from enum import Enum
from typing import List

pygame.init()

CAMERA_WIDTH_FRACT = 0.8
CAMERA_HEIGHT_FRACT = 1
CELL_WIDTH = 32
CELL_HEIGHT = 32
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 16

MAP_WIDTH = 25
MAP_HEIGHT = 25
# Map limitations (must be odd number)
assert MAP_WIDTH % 2 == 1
assert MAP_HEIGHT % 2 == 1
MAP_MAX_NUM_ROOMS = 10
MAP_NUM_LEVELS = 3

CAMERA_WIDTH = 1000
CAMERA_HEIGHT = 800

# Room limitations
ROOM_MAX_HEIGHT = 7
ROOM_MAX_WIDTH = 3
ROOM_MIN_HEIGHT = 5
ROOM_MIN_WIDTH = 3

RECT_WHOLE_SCREEN = None

# Mini Map stuff
MINI_MAP_CELL_WIDTH = 4
MINI_MAP_CELL_HEIGHT = 4

# FPS LIMIT
GAME_FPS = 60

INVENTORY_TEXT_HEIGHT = 20

END_GAME_ITEM_NAME = "Orb of Mystery" \
                     ""

# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_DARK_GREY = (50, 50, 50)
COLOR_ORANGE = (255, 128, 0)
COLOR_BROWN = (153, 77, 0)
COLOR_PINK = (224, 33, 138)

COLOR_PURPLE = (171, 39, 79)
COLOR_DARK_PURPLE = (104, 40, 96)

COLOR_RED_LIGHT = (255, 102, 102)
COLOR_RED = (255, 0, 0)
COLOR_RED_DARK = (77, 0, 0)

COLOR_GREEN_LIGHT = (191, 255, 128)
COLOR_GREEN_NEON = (57, 255, 20)
COLOR_GREEN = (0, 255, 0)
COLOR_GREEN_DARK = (68, 102, 0)

COLOR_BLUE_LIGHT = (173, 216, 230)
COLOR_BLUE = (0, 0, 255)
COLOR_BLUE_DARK = (0, 8, 51)

COLOR_YELLOW_LIGHT = (255, 255, 179)
COLOR_YELLOW = (255, 255, 0)
COLOR_YELLOW_DARK_GOLD = (128, 128, 0)

# game colors
COLOR_DEFAULT_BG = COLOR_GREY

# FOV SETTINGS Er hat anstelle der Null "libcod.FOV_BASIC" da stehen
FOV_ALGO = libtcodpy.FOV_DIAMOND
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 8

# MESSAGE DEFAULTS
NUM_MESSAGES = 4

# DEPTH
DEPTH_PLAYER = -100
DEPTH_CREATURE = 1
DEPTH_ITEM = 2
DEPTH_CORPSE = 100
DEPTH_STRUCTURES = 101

# xp related stuff
XP_NEEDED = {
    1: 300,
    2: 700,
    3: 1200,
    4: 1800,
    5: 2500,
}

MAX_LEVEL = max(XP_NEEDED.keys())

XP_NEEDED_FOR_NEXT = {}
for i in XP_NEEDED.keys():
    if i < MAX_LEVEL:
        XP_NEEDED_FOR_NEXT[i] = XP_NEEDED[i + 1] - XP_NEEDED[i]
    else:
        XP_NEEDED_FOR_NEXT[i] = math.inf

print(XP_NEEDED_FOR_NEXT)

EXPLORED_DRAW_FLAGS = pygame.BLEND_RGBA_SUB


class ACTIONS(Enum):
    CONSOLE = 1
    QUIT = 2
    MOVED = 3
    DEBUG = 4
    PICKED_UP = 5
    DROP = 6
    PAUSE = 7
    INVENTORY = 8
    TILE_SELECT = 9
    USED = 10
    STOPPED_AUTOEXPLORING = 11
    AUTOEXPLORED = 12
    NO_ACTION = 13
    SPELL = 14
    AUTOWALK = 15
    STOPPED_AUTOWALKING = 16



DEPTH_PLAYER = -100
DEPTH_CREATURE = 1
DEPTH_ITEM = 2
DEPTH_CORPSE = 100
DEPTH_STRUCTURES = 101


TAKES_TURN = {ACTIONS.MOVED, ACTIONS.PICKED_UP, ACTIONS.DROP, ACTIONS.USED, ACTIONS.AUTOEXPLORED,
              ACTIONS.STOPPED_AUTOEXPLORING, ACTIONS.SPELL, ACTIONS.AUTOWALK, ACTIONS.STOPPED_AUTOWALKING}


def takes_turn(action):
    return action in TAKES_TURN


class LevelNames:
    level_names: List[str] = ["DUNGEON1", "DUNGEON2", "DUNGEON3"]

    @classmethod
    def is_last_level(cls, level_name: str) -> bool:
        return cls.level_names.index(level_name) == len(cls.level_names) - 1

    @classmethod
    def is_first_level(cls, level_name: str) -> bool:
        return cls.level_names.index(level_name) == 0

    @classmethod
    def next_level_name(cls, level_name: str) -> str:
        if not cls.is_last_level(level_name):
            return cls.level_names[cls.level_names.index(level_name) + 1]

    @classmethod
    def previous_level_name(cls, level_name: str) -> str:
        if not cls.is_first_level(level_name):
            return cls.level_names[cls.level_names.index(level_name) - 1]
