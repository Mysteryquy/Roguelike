from __future__ import annotations
# 3rd party modules
import ctypes
import gzip
import os
import pickle
import random

import pygame
import tcod
import tcod.map
from src.object_game import GameState
from src import config, camera, assets, map_helper, render_helper, menu, constants
# gamefiles
from src.object_game import Game
from src.ui import Textfield, GuiContainer, FillBar, TextPane


class Preferences:
    def __init__(self):
        self.vol_sound = .5
        self.vol_music = .25


def game_main_loop():
    game_quit = False

    while not game_quit:
        if config.GAME.state == GameState.RUNNING:
            config.GAME.current_level.world.process()
        elif config.GAME.state == GameState.PAUSE:
            continue
        # update the display
        pygame.display.flip()

        config.CLOCK.tick(constants.GAME_FPS)


def game_initialize():
    # disable scaling of windows
    ctypes.windll.user32.SetProcessDPIAware()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

    # initialize Pygame
    pygame.init()
    pygame.display.set_caption("Roguelike")

    pygame.key.set_repeat(50, 100)

    try:
        preferences_load()
    except:
        config.PREFERENCES = Preferences()

    tcod.namegen_parse("data/namegen/jice_celtic.cfg")

    # looks for resolution of the display of the user
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    from src import constants
    constants.CAMERA_WIDTH = int(round(screen_width * constants.CAMERA_WIDTH_FRACT))
    constants.CAMERA_HEIGHT = int(round(screen_height * constants.CAMERA_HEIGHT_FRACT))

    rest_of_screen_w = screen_width - constants.CAMERA_WIDTH

    constants.RECT_WHOLE_SCREEN = pygame.Rect(0, 0, screen_width, screen_height)

    config.ROUND_COUNTER = 0

    config.SURFACE_MAIN = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME | pygame.DOUBLEBUF)
    config.SURFACE_MAIN.set_alpha(None)

    config.SURFACE_MAP = pygame.Surface(
        (constants.MAP_WIDTH * constants.CELL_WIDTH, constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    config.SURFACE_MINI_MAP = pygame.Surface(
        (rest_of_screen_w, rest_of_screen_w))

    config.SURFACE_INFO = pygame.Surface(
        (rest_of_screen_w, screen_height)
    )

    render_helper.fill_surfaces()

    config.ASSETS = assets.Assets()
    config.CAMERA = camera.Camera()

    config.CLOCK = pygame.time.Clock()

    # Random Engine
    config.RANDOM_ENGINE = random.SystemRandom()

    config.FOV_CALCULATE = True

    config.CONSOLE = Textfield(config.SURFACE_MAIN,
                               pygame.Rect(5, constants.CAMERA_HEIGHT - 30, constants.CAMERA_WIDTH / 1.2, 25),
                               "console", constants.COLOR_GREY, constants.COLOR_WHITE, constants.COLOR_YELLOW_DARK_GOLD,
                               focus_key=pygame.K_o)

    setup_gui(rest_of_screen_w)


def setup_gui(rest_of_screen_w):
    health_bar = FillBar(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 5, rest_of_screen_w, 30), "health_bar",
                         constants.COLOR_RED_LIGHT, constants.COLOR_RED_DARK, "Health", 100,
                         constants.COLOR_BLACK)

    mana_bar = FillBar(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 40, rest_of_screen_w, 30), "mana_bar",
                       constants.COLOR_BLUE_LIGHT, constants.COLOR_BLUE_DARK, "Mana", 100,
                       constants.COLOR_WHITE)

    xp_bar = FillBar(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 75, rest_of_screen_w, 30), "xp_bar",
                     constants.COLOR_YELLOW_LIGHT, constants.COLOR_YELLOW_DARK_GOLD, "XP",
                     100,
                     constants.COLOR_BLACK)

    str_pane = TextPane(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 110, 50, 20), "str",
                        constants.COLOR_RED, "STR: ")
    dex_pane = TextPane(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 135, 50, 20), "dex",
                        constants.COLOR_GREEN, "DEX: ")
    int_pane = TextPane(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 160, 50, 20), "int",
                        constants.COLOR_BLUE, "INT: ")

    config.GUI = GuiContainer(config.SURFACE_INFO, pygame.Rect(0, 0, 0, 0), "GUI", health_bar, mana_bar, xp_bar,
                              str_pane, dex_pane, int_pane)


def game_new(player_name):
    config.GAME = Game(game_load=game_load, game_save=game_save, player_name=player_name)

    config.GAME.current_level.place_objects()

    config.FOV_CALCULATE = True
    config.GAME.current_level.calculate_fov()


def game_exit():
    game_save()

    # quit the game
    pygame.quit()
    exit()


def game_save(display_message=False):
    if display_message:
        config.GAME.game_message("Saved Game", constants.COLOR_WHITE)

    with gzip.open("data/userdata/savegame", "w+b") as file:
        pickle.dump([config.GAME], file)


def game_load():
    with gzip.open("data/userdata/savegame") as file:
        config.GAME, config.PLAYER = pickle.load(file)

    map_helper.make_fov(config.GAME.current_map)
    config.FOV_CALCULATE = True
    map_helper.calculate_fov()


def preferences_save():
    with gzip.open("data/userdata/pref", "wb") as file:
        pickle.dump(config.PREFERENCES, file)


def preferences_load():
    with gzip.open("data/userdata/pref") as file:
        config.PREFERENCES = pickle.load(file)


if __name__ == '__main__':
    game_initialize()
    config.MAIN_MENU = menu.MainMenu(game_exit, game_load, game_new, game_main_loop, preferences_save)
    config.MAIN_MENU.show_menu()
