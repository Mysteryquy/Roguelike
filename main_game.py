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
from object_game import GameState
import assets
import camera
import config
# gamefiles
import constants
import game_map
import generator
import menu
import monster_gen
import render
from object_game import Game
from ui import Textfield, GuiContainer, FillBar, TextPane
from casting import cast_buffstats, cast_raisedead
from constants import ACTIONS


#     _______.___________..______       __    __    ______ .___________.
#    /       |           ||   _  \     |  |  |  |  /      ||           |
#   |   (----`---|  |----`|  |_)  |    |  |  |  | |  ,----'`---|  |----`
#    \   \       |  |     |      /     |  |  |  | |  |         |  |     
# .----)   |      |  |     |  |\  \----.|  `--'  | |  `----.    |  |
# |_______/       |__|     | _| `._____| \______/   \______|    |__|


class Preferences:
    def __init__(self):
        self.vol_sound = .5
        self.vol_music = .25


#  o         o   __o__
# <|>       <|>    |
# / \       / \   / \
# \o/       \o/   \o/
#  |         |     |
# < >       < >   < >
#  \         /     |
#   o       o      o
#   <\__ __/>    __|>_


#  _______      ___      .___  ___.  _______
# /  _____|    /   \     |   \/   | |   ____|
# |  |  __     /  ^  \    |  \  /  | |  |__
# |  | |_ |   /  /_\  \   |  |\/|  | |   __|
# |  |__| |  /  _____  \  |  |  |  | |  |____
# \______| /__/     \__\ |__|  |__| |_______|


def invoke_command(command):
    arguments = command.split()
    for c in arguments:
        print(c)
    if command[0] == "gen_worm":
        config.GAME.current_objects.append(monster_gen.gen_pest_worm(((int(arguments[1]), int(arguments[2])))))
    elif command[0] == "gen_item":
        generator.gen_item((int(arguments[1]), int(arguments[2])))


def game_main_loop():
    game_quit = False

    while not game_quit:

        if config.GAME.state == GameState.RUNNING:
            player_action = game_handle_keys()

            if player_action != ACTIONS.AUTOEXPLORED:
                config.AUTO_EXPLORING = False

            game_map.calculate_fov()

            if player_action == ACTIONS.QUIT:
                game_exit()

            if constants.takes_turn(player_action):
                for obj in config.GAME.current_objects:
                    obj.update()

                config.ROUND_COUNTER += 1

            if config.PLAYER.state == "STATUS_DEAD" or config.PLAYER.state == "STATUS_WIN":
                game_quit = True
        elif config.GAME.state == GameState.PAUSE:
            continue

        render.draw_game()

        # update the display
        pygame.display.flip()

        config.CLOCK.tick(constants.GAME_FPS)


def game_initialize():
    """Das hier startet Pygame und das Hauptfenster"""

    # makes window start at top left corner
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "30,30"
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

    print("x:")
    print(screen_height - constants.CAMERA_HEIGHT)
    config.SURFACE_INFO = pygame.Surface(
        (rest_of_screen_w, screen_height)
    )

    render.fill_surfaces()

    config.ASSETS = assets.Assets()
    config.CAMERA = camera.Camera()

    config.CLOCK = pygame.time.Clock()

    # Random Engine
    config.RANDOM_ENGINE = random.SystemRandom()

    config.FOV_CALCULATE = True

    config.CONSOLE = Textfield(
        config.SURFACE_MAIN, pygame.Rect(5, constants.CAMERA_HEIGHT - 30, constants.CAMERA_WIDTH / 1.2, 25), "console",
        constants.COLOR_GREY,
        constants.COLOR_WHITE, constants.COLOR_YELLOW_DARK_GOLD, auto_active=False, focus_key=pygame.K_o
    )

    config.PLAYER = generator.gen_player((0, 0), "dieter")

    setup_gui(rest_of_screen_w)


def setup_gui(rest_of_screen_w):
    health_bar = FillBar(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 5, rest_of_screen_w, 30), "health_bar",
                         constants.COLOR_RED_LIGHT, constants.COLOR_RED_DARK, "Health", config.PLAYER.creature.maxhp,
                         constants.COLOR_BLACK)

    mana_bar = FillBar(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 40, rest_of_screen_w, 30), "mana_bar",
                       constants.COLOR_BLUE_LIGHT, constants.COLOR_BLUE_DARK, "Mana", config.PLAYER.creature.max_mana,
                       constants.COLOR_WHITE)

    xp_bar = FillBar(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 75, rest_of_screen_w, 30), "xp_bar",
                     constants.COLOR_YELLOW_LIGHT, constants.COLOR_YELLOW_DARK_GOLD, "XP",
                     constants.XP_NEEDED[config.PLAYER.creature.level],
                     constants.COLOR_BLACK)

    str_pane = TextPane(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 110, 50, 20), "str",
                        constants.COLOR_RED, "STR: ")
    dex_pane = TextPane(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 135, 50, 20), "dex",
                        constants.COLOR_GREEN, "DEX: ")
    int_pane = TextPane(config.SURFACE_INFO, pygame.Rect(0, rest_of_screen_w + 160, 50, 20), "int",
                        constants.COLOR_BLUE, "INT: ")

    config.GUI = GuiContainer(config.SURFACE_INFO, pygame.Rect(0, 0, 0, 0), "GUI", health_bar, mana_bar, xp_bar,
                              str_pane, dex_pane, int_pane)


def game_handle_keys():
    # get config.PLAYER input
    keys_list = pygame.key.get_pressed()
    events_list = pygame.event.get()

    # Check for mid key
    MOD_KEY = (keys_list[pygame.K_RSHIFT] or keys_list[pygame.K_LSHIFT])

    # process input

    for event in events_list:

        if config.CONSOLE.active:
            if config.CONSOLE.react(event):
                command = config.CONSOLE.text_ready
                invoke_command(command)
            return ACTIONS.CONSOLE
        if config.CONSOLE.update_activate(event):
            return ACTIONS.CONSOLE
        if event.type == pygame.QUIT:
            return ACTIONS.QUIT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ACTIONS.QUIT

            if event.key in constants.MOVEMENT_DICT.keys():
                dx, dy = constants.MOVEMENT_DICT[event.key]
                if game_map.is_walkable(config.PLAYER.x + dx, config.PLAYER.y + dy):
                    config.PLAYER.move(dx, dy)
                    config.FOV_CALCULATE = True
                    return ACTIONS.MOVED
                else:
                    return ACTIONS.NO_ACTION

            if event.key == pygame.K_a:
                menu.debug_tile_select_pathing()
                return ACTIONS.DEBUG

            if event.key == pygame.K_g:
                objects_at_player = game_map.objects_at_coords(config.PLAYER.x, config.PLAYER.y)

                for obj in objects_at_player:
                    if obj.item:
                        print(obj.name_object)
                        obj.item.pick_up(config.PLAYER)
                return ACTIONS.PICKED_UP

            if event.key == pygame.K_d:
                if len(config.PLAYER.container.inventory) > 0:
                    config.PLAYER.container.inventory[-1].item.drop(config.PLAYER.x, config.PLAYER.y)
                return ACTIONS.DROP

            if event.key == pygame.K_p:
                config.GAME.game_message("Game resumed", constants.COLOR_WHITE)
                menu.menu_pause()
                return ACTIONS.PAUSE

            if event.key == pygame.K_i:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/audio/soundeffects/leather_inventory.wav"))
                menu.menu_inventory()
                return ACTIONS.INVENTORY

            if event.key == pygame.K_l:
                menu.menu_tile_select()
                return ACTIONS.TILE_SELECT

            if event.key == pygame.K_m:
                generator.gen_and_append_enemy((config.PLAYER.x, config.PLAYER.y))
                return ACTIONS.DEBUG

            if event.key == pygame.K_x:
                menu.debug_tile_select()
                return ACTIONS.DEBUG

            if event.key == pygame.K_s:
                config.GAME.transition_next()
                return ACTIONS.DEBUG

            if event.key == pygame.K_1:
                config.GAME.game_message("Player position: " + str((config.PLAYER.x, config.PLAYER.y)))
                return ACTIONS.DEBUG

            if event.key == pygame.K_2:
                config.GAME.game_message("Camera position: " + str(config.CAMERA.cam_map_coord))
                return ACTIONS.DEBUG

            if event.key == pygame.K_b:
                game_save(display_message=True)
                game_load()
                return ACTIONS.DEBUG

            if event.key == pygame.K_r:
                cast_raisedead(config.PLAYER, 10)
                return ACTIONS.SPELL

            if MOD_KEY and event.key == pygame.K_PERIOD:
                list_of_objs = game_map.objects_at_coords(config.PLAYER.x, config.PLAYER.y)
                for obj in list_of_objs:
                    if obj.structure:
                        obj.structure.use()
                return ACTIONS.USED

            if event.key == pygame.K_BACKQUOTE:
                game_map.start_auto_explore()
                return ACTIONS.AUTOEXPLORED

            if event.key == pygame.K_v:
                cast_buffstats(config.PLAYER, 10)
                return ACTIONS.SPELL

    if config.AUTO_EXPLORING:

        x, y = next(config.GAME.auto_explore_path, (0, 0))

        config.AUTO_EXPLORING = game_map.check_contine_autoexplore()
        if not config.AUTO_EXPLORING:
            return ACTIONS.STOPPED_AUTOEXPLORING
        if (x, y) == (0, 0):
            if game_map.autoexplore_new_goal():
                x, y = next(config.GAME.auto_explore_path, (0, 0))
            else:
                return ACTIONS.STOPPED_AUTOEXPLORING

        config.PLAYER.move_towards_point(x, y)
        config.FOV_CALCULATE = True
        return ACTIONS.AUTOEXPLORED

    return ACTIONS.NO_ACTION


def game_new(player_name="config.PLAYER"):
    # starts a nre game and map
    config.GAME = Game()
    config.PLAYER = generator.gen_player((0, 0), player_name=player_name)
    config.GAME.current_objects.append(config.PLAYER)

    game_map.place_objects(config.GAME.current_rooms)


def game_exit():
    game_save()

    # quit the game
    pygame.quit()
    exit()


def game_save(display_message=False):
    if display_message:
        config.GAME.game_message("Saved Game", constants.COLOR_WHITE)

    for obj in config.GAME.current_objects:
        obj.animation_destroy()

    with gzip.open("data/userdata/savegame", "w+b") as file:
        pickle.dump([config.GAME, config.PLAYER], file)


def game_load():
    with gzip.open("data/userdata/savegame", "rb") as file:
        config.GAME, config.PLAYER = pickle.load(file)

    for obj in config.GAME.current_objects:
        obj.animation_init()

    game_map.make_fov(config.GAME.current_map)
    config.FOV_CALCULATE = True
    game_map.calculate_fov()


def preferences_save():
    with gzip.open("data/userdata/pref", "wb") as file:
        pickle.dump(config.PREFERENCES, file)


def preferences_load():
    with gzip.open("data/userdata/pref", "rb") as file:
        config.PREFERENCES = pickle.load(file)


if __name__ == '__main__':
    game_initialize()
    config.MAIN_MENU = menu.MainMenu(game_exit, game_load, game_new, game_main_loop, preferences_save)
    config.MAIN_MENU.show_menu()

#              .7
#            .'/
#           / /
#          / /
#         / /
#        / /
#       / /
#      / /
#     / /         
#    / /          
#  __|/
# ,-\__\
# |f-"Y\|
# \()7L/
# cgD                            __ _
# |\(                          .'  Y '>,
#  \ \                        / _   _   \
#   \\\                       )(_) (_)(|}
#    \\\                      {  4A   } /
#     \\\                      \uLuJJ/\l
#      \\\                     |3    p)/
#       \\\___ __________      /nnm_n//
#       c7___-__,__-)\,__)(".  \_>-<_/D
#                  //V     \_"-._.__G G_c__.-__<"/ ( \
#                         <"-._>__-,G_.___)\   \7\
#                        ("-.__.| \"<.__.-" )   \ \
#                        |"-.__"\  |"-.__.-".\   \ \
#                        ("-.__"". \"-.__.-".|    \_\
#                        \"-.__""|!|"-.__.-".)     \ \
#                         "-.__""\_|"-.__.-"./      \ l
#                          ".__""">G>-.__.-">       .--,_
#                              ""  G
