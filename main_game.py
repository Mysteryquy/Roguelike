# 3rd party modules#3rd party modules
from typing import Any

import pygame
import tcod
import tcod.map
import os
import ctypes

# gamefiles
import constants


# WENN DAS GRÜN IST HAT ES GEKLAPPT

#     _______.___________..______       __    __    ______ .___________.
#    /       |           ||   _  \     |  |  |  |  /      ||           |
#   |   (----`---|  |----`|  |_)  |    |  |  |  | |  ,----'`---|  |----`
#    \   \       |  |     |      /     |  |  |  | |  |         |  |     
# .----)   |      |  |     |  |\  \----.|  `--'  | |  `----.    |  |
# |_______/       |__|     | _| `._____| \______/   \______|    |__|

class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False

class struc_Assets:
    def __init__(self):

        #Sprite sheets#
        self.charspritesheet = obj_Spritesheet("data/Reptiles.png")
        self.enemyspritesheet = obj_Spritesheet("data/ROFL.png")


        #ANIMATIONS#
        self.A_PLAYER = self.charspritesheet.get_animation("m", 5, 16, 16, 4, (32, 32))
        self.A_ENEMY = self.enemyspritesheet.get_animation("k", 1, 16, 16, 2, (32, 32))


        #SPRITES#
        self.S_WALL = pygame.image.load("data/wall2.jpg")
        self.S_WALLEXPLORED = pygame.image.load("data/wallunseen2.png")

        self.S_FLOOR = pygame.image.load("data/floor.jpg")
        self.S_FLOOREXPLORED = pygame.image.load("data/floorunseen2.png")

        #FONTS#
        self.FONT_DEBUG_MESSAGE = pygame.font.Font("data/joystix.ttf", 20)
        self.FONT_MESSAGE_TEXT = pygame.font.Font("data/joystix.ttf", 20)


#  ______   .______          __   _______   ______ .___________.    _______.
# /  __  \  |   _  \        |  | |   ____| /      ||           |   /       |
# |  |  |  | |  |_)  |       |  | |  |__   |  ,----'`---|  |----`  |   (----`
# |  |  |  | |   _  <  .--.  |  | |   __|  |  |         |  |        \   \
# |  `--'  | |  |_)  | |  `--'  | |  |____ |  `----.    |  |    .----)   |
# \______/  |______/   \______/  |_______| \______|    |__|    |_______/  


class obj_Actor:

    def __init__(self, x, y, name_object, animation, animation_speed = 1.0, creature=None, ai=None, container = None, item = None):
        self.x = x
        self.y = y
        self.animation = animation  #number of images
        self.animation_speed = animation_speed / 1.0 #in seconds

        #animation flicker speed
        self.flicker_speed = self.animation_speed / len(self.animation)
        self.flicker_timer = 0.0
        self.sprite_image = 0 #s

        self.creature = creature
        if self.creature:
            self.creature.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:
            self.container.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

    def draw(self):
        is_visible = FOV_MAP.fov[self.y, self.x]

        if is_visible:
            if len(self.animation) == 1:
                SURFACE_MAIN.blit(self.animation[0], (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

            elif len(self.animation) > 1:
                if CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1 / CLOCK.get_fps()

                if self.flicker_timer >= self.flicker_speed:
                    self.flicker_timer = 0.0

                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0

                    else:
                        self.sprite_image += 1

                SURFACE_MAIN.blit(self.animation[self.sprite_image], (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))








class obj_Game:
    def __init__(self):

        self.current_map = map_create()
        self.message_history = []

        self.current_objects = []

class obj_Spritesheet: #Bilder von Spritesheets holen

    def __init__(self, file_name):
        #Den Sheet laden.
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.tiledict = {"a" : 1 , "b" : 2 , "c" : 3 , "d" : 4 , "e" : 5 , "f" : 6 , "g" : 7 , "h" : 8 , "i" : 9 , "j" : 10 , "k" : 11 , "l" : 12 , "m" : 13 , "n" : 14 , "o" : 15, "p" : 16}

        ###############

    def get_image(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT, scale = None):

        image_list = []

        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width, row*height, width, height))

        image.set_colorkey(constants.COLOR_BLACK)

        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))

        image_list.append(image)

        return image_list

    def get_animation(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT, num_sprites = 1, scale = None):

        image_list = []

        for i in range(num_sprites):
            #Create blank image
            image = pygame.Surface([width, height]).convert()

            #copy image from sheet onto blank
            image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width+(width*i), row*height, width, height))

            #set transparency to black
            image.set_colorkey(constants.COLOR_BLACK)

            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))

            image_list.append(image)

        return image_list




#                                                         __
#  ____  ____   _____ ______   ____   ____   ____   _____/  |_  ______
# _/ ___\/  _ \ /     \\____ \ /  _ \ /    \_/ __ \ /    \   __\/  ___/
# \  \__(  <_> )  Y Y  \  |_> >  <_> )   |  \  ___/|   |  \  |  \___ \
# \___  >____/|__|_|  /   __/ \____/|___|  /\___  >___|  /__| /____  >
#     \/            \/|__|               \/     \/     \/          \/ 


class com_Creature:

    def __init__(self, name_instance, hp=10, death_function=None):
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):

        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            # im Tuturial ist das print unten rot aber anscheined geht es trotzdem
            self.attack(target, 10)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):

        game_message(
            self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!",
              constants.COLOR_WHITE)
        target.creature.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        game_message(self.name_instance + "`s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

        if self.hp <= 0:

            if self.death_function is not None:
                self.death_function(self.owner)



# TODO class com_item:

class com_Container(object):

    def __init__(self, volume = 10.0, inventory = []):
        self.inventory = inventory
        self.max_volume = volume
        self._volume = 0.0


    @property
    def volume(self):
        return self._volume

    ## TODO Get Names of everything in inventory




    ## TODO Get weight of everything in cointainer

class com_Item:
    def __init__(self, weight = 0.0, volume = 0.0):
        self.weight = weight
        self.volume = volume

    ## TODO Pick up this item
    def pick_up(self, actor):

        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
                game_message("Not enough room to pick up")

            else:
                game_message("Picked up")
                actor.container.inventory.append(self.owner)
                GAME.current_objects.remove(self.owner)
                self.container = actor.container

    ## TODO Drop Item
    def drop(self):
        GAME.current_objects.append(self.owner)
        self.container.inventory.remove(self.owner)
        game_message("Item dropped")


    ## TODO Use item


#   _____  .___ 
#  /  _  \ |   |
# /  /_\  \|   |
# /    |    \   |
# \____|__  /___|
#        \/ 

class ai_Test:

    def take_turn(self):
        self.owner.creature.move(tcod.random_get_int(None, -1, 1), tcod.random_get_int(None, -1, 1))


def death_monster(monster):
    # On death, most monsters stop moving tho
    game_message(monster.creature.name_instance + " is slaughtered into ugly bits of flesh!", constants.COLOR_GREY)
    # print (monster.creature.name_instance + " is slaughtered into ugly bits of flesh!")

    monster.creature = None
    monster.ai = None


# .___  ___.      ___      .______
# |   \/   |     /   \     |   _  \
# |  \  /  |    /  ^  \    |  |_)  |
# |  |\/|  |   /  /_\  \   |   ___/
# |  |  |  |  /  _____  \  |  |
# |__|  |__| /__/     \__\ | _|

def map_create():
    new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT - 1].block_path = True

    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH - 1][y].block_path = True

    map_make_fov(new_map)

    return new_map


def map_check_for_creature(x, y, exclude_object=None):
    target = None

    if exclude_object:
        # ceck objectlist to find creature at that location that isnt excluded
        for object in GAME.current_objects:
            if (object is not exclude_object and
                    object.x == x and
                    object.y == y and
                    object.creature):
                target = object

            if target:
                return target

    else:
        # ceck objectlist to find any creature at that location
        for object in GAME.current_objects:
            if (object.x == x and
                    object.y == y and
                    object.creature):
                target = object

            if target:
                return target


def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = tcod.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            # same as before, but now we have array for walkable and transparent
            FOV_MAP.walkable[x][y] = not incoming_map[x][y].block_path
            FOV_MAP.transparent[x][y] = not incoming_map[x][y].block_path


def map_calculate_fov():
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        FOV_MAP.compute_fov(PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
                            constants.FOV_ALGO)

def map_objects_at_coords(coords_x, coords_y):

    object_options = [obj for obj in GAME.current_objects
                        if obj.x == coords_x and obj.y == coords_y]

    return object_options

# _______  .______          ___   ____    __    ____  __  .__   __.   _______
# |       \ |   _  \        /   \  \   \  /  \  /   / |  | |  \ |  |  /  _____|
# |  .--.  ||  |_)  |      /  ^  \  \   \/    \/   /  |  | |   \|  | |  |  __
# |  |  |  ||      /      /  /_\  \  \            /   |  | |  . `  | |  | |_ |
# |  '--'  ||  |\  \----./  _____  \  \    /\    /    |  | |  |\   | |  |__| |
# |_______/ | _| `._____/__/     \__\  \__/  \__/     |__| |__| \__|  \______|

def draw_game():
    global SURFACE_MAIN

    # clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME.current_map)

    for obj in GAME.current_objects:
        obj.draw()

    draw_debug()
    draw_messages()

    # update the display
    pygame.display.flip()


def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):

            is_visible = FOV_MAP.fov[y, x]
            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path:

                    SURFACE_MAIN.blit(ASSETS.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(ASSETS.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            elif map_to_draw[x][y].explored:

                    if map_to_draw[x][y].block_path: #Bruh was will der von mir

                        SURFACE_MAIN.blit(ASSETS.S_WALLEXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                    else:
                        SURFACE_MAIN.blit(ASSETS.S_FLOOREXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def draw_debug():
    draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), (0, 0), constants.COLOR_WHITE, constants.COLOR_BLACK)


def draw_messages():
    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history
    else:
        to_draw = GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_height(ASSETS.FONT_MESSAGE_TEXT)

    info = pygame.display.Info()
    screen_height = info.current_h

    start_y = screen_height - (constants.NUM_MESSAGES * text_height)

    i = 0

    for message, color in to_draw:
        draw_text(SURFACE_MAIN, message, (0, start_y + i * text_height), color, constants.COLOR_BLACK)

        i += 1


def draw_text(display_surface, text_to_display, T_coords, text_color, back_color=None):
    # This function takes in some text and displ#wtfays it on the refered surface#community version LUL jo is das schlimm ne aber wollte dir gerade den performance analyzer zeigen

    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)

    text_rect.topleft = T_coords

    display_surface.blit(text_surf, text_rect)


#bruh das auto einruecken aht iwe alles kaputt gemacht Ich merksvergleich das mal pls mit github und aender die da wo das broken ist BRUH oder mom
#          _______  _        _______  _______  _______  _______
# |\     /|(  ____ \( \      (  ____ )(  ____ \(  ____ )(  ____ \
# | )   ( || (    \/| (      | (    )|| (    \/| (    )|| (    \/
# | (___) || (__    | |      | (____)|| (__    | (____)|| (_____
# |  ___  ||  __)   | |      |  _____)|  __)   |     __)(_____  )
# | (   ) || (      | |      | (      | (      | (\ (         ) |
# | )   ( || (____/\| (____/\| )      | (____/\| ) \ \__/\____) |
# |/     \|(_______/(_______/|/       (_______/|/   \__/\_______)

def helper_text_objects(incoming_text, incoming_color, incoming_bg):
    if incoming_bg:
        Text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        Text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color)

    return Text_surface, Text_surface.get_rect()


def helper_text_height(font):
    (width, height) = font.size("A")
    # font_object = font.render("a", False, (0,0,0))
    # font_rect = font_object.get_rect
    return height


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

        map_calculate_fov()

        if player_action == "QUIT":
            game_quit = True

        elif player_action != "no-action":
            for obj in GAME.current_objects:
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

        CLOCK.tick(constants.GAME_FPS)

    # quit the game
    pygame.quit()
    exit()


def game_initialize():
    '''Das hier startet Pygame und das Hauptfenster'''

    global SURFACE_MAIN, GAME, PLAYER, ENEMY, FOV_CALCULATE, CLOCK, ASSETS
    # makes window start at top left corner
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    # disable scaling of windows
    ctypes.windll.user32.SetProcessDPIAware()

    # initialize Pygame
    pygame.init()

    GAME = obj_Game()

    CLOCK = pygame.time.Clock()


    # looks for resolution of the display of the user
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    SURFACE_MAIN = pygame.display.set_mode((screen_width, screen_height),
                                           pygame.NOFRAME)


    FOV_CALCULATE = True

    ASSETS = struc_Assets()


    container_com1 = com_Container()
    creature_com1 = com_Creature("greg")
    PLAYER = obj_Actor(1, 1, "python", ASSETS.A_PLAYER, animation_speed = 0.5, creature=creature_com1, container = container_com1)

    item_com1 = com_Item()
    creature_com2 = com_Creature("crabby", death_function=death_monster)
    ai_com = ai_Test()
    ENEMY = obj_Actor(2, 2, "crab", ASSETS.A_ENEMY, creature=creature_com2, ai=ai_com, item = item_com1)

    GAME.current_objects = [PLAYER, ENEMY]


def game_handle_keys():
    global FOV_CALCULATE

    # get player input
    events_list = pygame.event.get()

    # process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "QUIT"
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP1:
                PLAYER.creature.move(-1, 1)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP2:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP3:
                PLAYER.creature.move(1, 1)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP4:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP5:
                PLAYER.creature.move(0, 0)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP6:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP7:
                PLAYER.creature.move(-1, -1)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP8:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_KP9:
                PLAYER.creature.move(1, -1)
                FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_g:
                objects_at_player = map_objects_at_coords(PLAYER.x, PLAYER.y)

                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(PLAYER)

    return "no-action"


def game_message(game_msg, msg_color = constants.COLOR_GREY):
    GAME.message_history.append((game_msg, msg_color))


if __name__ == '__main__':
    game_initialize()
    game_main_loop()

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
