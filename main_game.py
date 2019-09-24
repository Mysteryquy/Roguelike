# 3rd party modules
import ctypes
import datetime
import gzip
import pickle
import random

import pygame
import tcod
import tcod.map
import config
import assets
import camera
import casting
# gamefiles
import constants
import generator
import game_map
import menu
import render
from ui import Textfield
from object_game import Game


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


class Stairs:

    def __init__(self, downwards=True):

        self.downwards = downwards

    def use(self):

        if self.downwards:
            config.GAME.transition_next()
        else:
            config.GAME.transition_previous()


class ExitPortal:
    def __init__(self):
        self.open_animation = "S_END_GAME_PORTAL_OPENED"
        self.end_animation = "S_END_GAME_PORTAL_CLOSED"
        self.open = False
        self.owner = None

    def update(self):

        found_item = False

        # check conditions
        portal_open = self.owner.state == "OPEN"

        for obj in config.PLAYER.container.inventory:
            if obj.name_object is constants.END_GAME_ITEM_NAME:
                found_item = True

        if found_item and not portal_open:
            self.owner.state = "OPEN"
            self.owner.animation_key = "S_END_GAME_PORTAL_OPENED"
            self.owner.animation_init()

        if not found_item and portal_open:
            self.owner.state = "CLOSED"
            self.owner.animation_key = "S_END_GAME_PORTAL_CLOSED"
            self.owner.animation_init()

    def use(self):

        print("Hans Wurst")

        if self.owner.state == "OPEN":
            config.PLAYER.state = "STATUS_WIN"

            config.SURFACE_MAIN.fill(constants.COLOR_WHITE)

            screen_center = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

            render.draw_text(config.SURFACE_MAIN, "YOU WON!", screen_center, constants.COLOR_BLACK, center=True)
            render.draw_text(config.SURFACE_MAIN, "Your win was recorded in your win file",
                             (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2 + 100), constants.COLOR_WHITE,
                             center=True)

            pygame.display.update()

            file_name = (
                    "data/userdata/winrecord_" + config.PLAYER.creature.name_instance + "." + datetime.date.today().strftime(
                "%Y%B%d") + ".txt")

            winrecord = open(file_name, "a+")

            winrecord.write("You won on the " + datetime.date.today().strftime(
                "%Y%B%d") + " as " + config.PLAYER.creature.name_instance + "\n")

            pygame.time.wait(6000)


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
    if command[0] == "gen_enemy":
        generator.gen_enemy((int(arguments[1]), int(arguments[2])))
    elif command[0] == "gen_item":
        generator.gen_item((int(arguments[1]), int(arguments[2])))


def game_main_loop():
    game_quit = False

    player_action = "no-action"

    while not game_quit:

        player_action = game_handle_keys(config.PLAYER)

        game_map.calculate_fov()

        if player_action == "QUIT":
            game_exit()

        for obj in config.GAME.current_objects:
            if obj.ai:
                if player_action != "no-action" and player_action != "console":
                    obj.ai.take_turn()
            if obj.exitportal:
                obj.exitportal.update()

        if config.PLAYER.state == "STATUS_DEAD" or config.PLAYER.state == "STATUS_WIN":
            game_quit = True

        # draw the game
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

    config.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

    config.SURFACE_MAP = pygame.Surface(
        (constants.MAP_WIDTH * constants.CELL_WIDTH, constants.MAP_HEIGHT * constants.CELL_HEIGHT))

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

    # game_new()


def game_handle_keys(player):
    # get player input
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
            return "console"
        if config.CONSOLE.update_activate(event):
            return "console"
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "QUIT"
            if event.key == pygame.K_UP:
                player.move(0, -1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_DOWN:
                player.move(0, 1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_LEFT:
                player.move(-1, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_RIGHT:
                player.move(1, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP1:
                player.move(-1, 1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP2:
                player.move(0, 1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP3:
                player.move(1, 1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP4:
                player.move(-1, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP5:
                player.move(0, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP6:
                player.move(1, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP7:
                player.move(-1, -1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP8:
                player.move(0, -1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP9:
                player.move(1, -1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_g:
                objects_at_player = game_map.objects_at_coords(config.PLAYER.x, config.PLAYER.y)

                for obj in objects_at_player:
                    if obj.item:
                        print(obj.name_object)
                        obj.item.pick_up(config.PLAYER)

            if event.key == pygame.K_d:
                if len(player.container.inventory) > 0:
                    player.container.inventory[-1].item.drop(config.PLAYER.x, config.PLAYER.y)

            if event.key == pygame.K_p:
                config.GAME.game_message("Game resumed", constants.COLOR_WHITE)
                menu.menu_pause()

            if event.key == pygame.K_i:
                menu.menu_inventory()

            if event.key == pygame.K_l:
                menu.menu_tile_select()

            if event.key == pygame.K_k:
                casting.cast_confusion(caster=config.PLAYER, effect_length=2)

            if event.key == pygame.K_m:
                generator.gen_enemy((player.x, player.y))

            if event.key == pygame.K_x:
                menu.debug_tile_select()

            if event.key == pygame.K_s:
                config.GAME.transition_next()

            if event.key == pygame.K_b:
                game_save(display_message=True)
                game_load()

            if MOD_KEY and event.key == pygame.K_PERIOD:
                list_of_objs = game_map.objects_at_coords(config.PLAYER.x, config.PLAYER.y)
                for obj in list_of_objs:
                    if obj.stairs:
                        obj.stairs.use()
                    elif obj.exitportal:
                        obj.exitportal.use()

    return "no-action"


def game_new(player_name="Player"):

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

    with gzip.open("data/userdata/savegame", "wb") as file:
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
    config.PLAYER = None
    game_initialize()
    main_menu = menu.MainMenu(game_exit, game_load, game_new, game_main_loop, preferences_save)
    main_menu.show_menu()
    #menu.menu_main(game_exit, game_load, game_new, game_main_loop, preferences_save)

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
