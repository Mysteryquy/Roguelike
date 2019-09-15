# 3rd party modules#3rd party modules
# capital bruh

import pygame
import tcod
import tcod.map
import ctypes
import pickle
import gzip
import random
import datetime
import assets
import camera
import casting
import map
import ui
import menu
from object_game import Game
# gamefiles
import constants
import config
import generator
import render




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


#  ______   .______          __   _______   ______ .___________.    _______.
# /  __  \  |   _  \        |  | |   ____| /      ||           |   /       |
# |  |  |  | |  |_)  |       |  | |  |__   |  ,----'`---|  |----`  |   (----`
# |  |  |  | |   _  <  .--.  |  | |   __|  |  |         |  |        \   \
# |  `--'  | |  |_)  | |  `--'  | |  |____ |  `----.    |  |    .----)   |
# \______/  |______/   \______/  |_______| \______|    |__|    |_______/  



#                                                         __
#  ____  ____   _____ ______   ____   ____   ____   _____/  |_  ______
# _/ ___\/  _ \ /     \\____ \ /  _ \ /    \_/ __ \ /    \   __\/  ___/
# \  \__(  <_> )  Y Y  \  |_> >  <_> )   |  \  ___/|   |  \  |  \___ \
# \___  >____/|__|_|  /   __/ \____/|___|  /\___  >___|  /__| /____  >
#     \/            \/|__|               \/     \/     \/          \/ 




class com_Stairs:

    def __init__(self, downwards=True):

        self.downwards = downwards

    def use(self):

        if self.downwards:
            config.GAME.transition_next()
        else:
            config.GAME.transition_previous()


class com_Exitportal:
    def __init__(self):
        self.OPENANIMATION = "S_END_GAME_PORTAL_OPENED"
        self.CLOSEDANIMATION = "S_END_GAME_PORTAL_CLOSED"
        self.open = False

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


#   _____  .___
#  /  _  \ |   |
# /  /_\  \|   |
# /    |    \   |
# \____|__  /___|
#        \/ 



# o   o   O   o-o  o-O-o   o-o
# |\ /|  / \ o       |    /
# | O | o---o|  -o   |   O
# |   | |   |o   |   |    \
# o   o o   o o-o  o-O-o   o-o

#  o         o   __o__
# <|>       <|>    |
# / \       / \   / \
# \o/       \o/   \o/
#  |         |     |
# < >       < >   < >
#  \         /     |
#   o       o      o
#   <\__ __/>    __|>_

# .___  ___.  _______ .__   __.  __    __       _______.
# |   \/   | |   ____||  \ |  | |  |  |  |     /       |
# |  \  /  | |  |__   |   \|  | |  |  |  |    |   (----`
# |  |\/|  | |   __|  |  . `  | |  |  |  |     \   \
# |  |  |  | |  |____ |  |\   | |  `--'  | .----)   |
# |__|  |__| |_______||__| \__|  \______/  |_______/

#                                 _
#  __ _  ___ _ __   ___ _ __ __ _| |_ ___
# / _` |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \
# | (_| |  __/ | | |  __/ | | (_| | ||  __/
# \__, |\___|_| |_|\___|_|  \__,_|\__\___|
# |___/



#  _______      ___      .___  ___.  _______
# /  _____|    /   \     |   \/   | |   ____|
# |  |  __     /  ^  \    |  \  /  | |  |__
# |  | |_ |   /  /_\  \   |  |\/|  | |   __|
# |  |__| |  /  _____  \  |  |  |  | |  |____
# \______| /__/     \__\ |__|  |__| |_______|

def game_main_loop():
    game_quit = False

    player_action = "no-action"

    while not game_quit:

        player_action = game_handle_keys()

        map.calculate_fov()

        if player_action == "QUIT":
            game_exit()

        for obj in config.GAME.current_objects:
            if obj.ai:
                if player_action != "no-action":
                    obj.ai.take_turn()
            if obj.exitportal:
                obj.exitportal.update()

        if (config.PLAYER.state == "STATUS_DEAD" or config.PLAYER.state == "STATUS_WIN"):
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

    pygame.key.set_repeat(200, 70)

    try:
       preferences_load()
    except:
        config.PREFERENCES = Preferences()

    tcod.namegen_parse("data/namegen/jice_celtic.cfg")

    # looks for resolution of the display of the user

    config.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

    config.SURFACE_MAP = pygame.Surface(
        (constants.MAP_WIDTH * constants.CELL_WIDTH, constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    config.CAMERA = camera.Camera()

    config.ASSETS = assets.Assets()

    config.CLOCK = pygame.time.Clock()

    # Random Engine
    config.RANDOM_ENGINE = random.SystemRandom()

    config.FOV_CALCULATE = True

    # game_new()


def game_handle_keys():

    # get player input
    keys_list = pygame.key.get_pressed()
    events_list = pygame.event.get()

    # Check for mid key
    MOD_KEY = (keys_list[pygame.K_RSHIFT] or keys_list[pygame.K_LSHIFT])

    # process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "QUIT"
            if event.key == pygame.K_UP:
                config.PLAYER.creature.move(0, -1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_DOWN:
                config.PLAYER.creature.move(0, 1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_LEFT:
                config.PLAYER.creature.move(-1, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_RIGHT:
                config.PLAYER.creature.move(1, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP1:
                config.PLAYER.creature.move(-1, 1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP2:
                config.PLAYER.creature.move(0, 1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP3:
                config.PLAYER.creature.move(1, 1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP4:
                config.PLAYER.creature.move(-1, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP5:
                config.PLAYER.creature.move(0, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP6:
                config.PLAYER.creature.move(1, 0)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP7:
                config.PLAYER.creature.move(-1, -1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP8:
                config.PLAYER.creature.move(0, -1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP9:
                config.PLAYER.creature.move(1, -1)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_g:
                objects_at_player = map.objects_at_coords(config.PLAYER.x, config.PLAYER.y)

                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(config.PLAYER)

            if event.key == pygame.K_d:
                if len(config.PLAYER.container.inventory) > 0:
                    config.PLAYER.container.inventory[-1].item.drop(config.PLAYER.x, config.PLAYER.y)

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
                casting.cast_lightning(caster=config.PLAYER, T_damage_maxrange=5)

            if event.key == pygame.K_x:
                menu.debug_tile_select()

            if event.key == pygame.K_s:
                config.GAME.transition_next()

            if event.key == pygame.K_b:
                game_save(display_message=True)
                game_load()

            if MOD_KEY and event.key == pygame.K_PERIOD:
                list_of_objs = map.objects_at_coords(config.PLAYER.x, config.PLAYER.y)
                for obj in list_of_objs:
                    if obj.stairs:
                        obj.stairs.use()
                    elif obj.exitportal:
                        obj.exitportal.use()

    return "no-action"


def game_new():

    config.PLAYER = generator.gen_player((0, 0))
    # starts a nre game and map
    config.GAME = Game()
    config.GAME.current_objects.append(config.PLAYER)

    map.place_objects(config.GAME.current_rooms)


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

    map.make_fov(config.GAME.current_map)
    config.FOV_CALCULATE = True
    map.calculate_fov()


def preferences_save():
    with gzip.open("data/userdata/pref", "wb") as file:
        pickle.dump(config.PREFERENCES, file)


def preferences_load():

    with gzip.open("data/userdata/pref", "rb") as file:
        config.PREFERENCES = pickle.load(file)


if __name__ == '__main__':
    menu.menu_main(game_initialize, game_exit, game_load, game_new, game_main_loop, preferences_save)

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
