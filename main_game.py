# 3rd party modules#3rd party modules
#capital bruh
from typing import Any

import pygame
import tcod
import tcod.map
import os
import ctypes
import math

# gamefiles
import constants


# a88888b. dP     dP   .d888888  888888ba   .88888.   88888888b dP         .88888.   .88888.
#d8'   `88 88     88  d8'    88  88    `8b d8'   `88  88        88        d8'   `8b d8'   `88
#88        88aaaaa88a 88aaaaa88a 88     88 88        a88aaaa    88        88     88 88
#88        88     88  88     88  88     88 88   YP88  88        88        88     88 88   YP88
#Y8.   .88 88     88  88     88  88     88 Y8.   .88  88        88        Y8.   .8P Y8.   .88
# Y88888P' dP     dP  88     88  dP     dP  `88888'   88888888P 88888888P  `8888P'   `88888'
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo


#TODO :
# Fonts wieder zurück in constants legen
# Bei der draw_text funktion ein font argument einbauen






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
        self.FONT_CURSOR_TEXT = pygame.font.Font("data/joystix.ttf", constants.CELL_HEIGHT)

        ## ITEMS ##
        self.S_SWORD = [pygame.transform.scale(pygame.image.load("data/sword.png"), (constants.CELL_WIDTH, constants.CELL_HEIGHT))]
        self.S_SHIELD = [pygame.transform.scale(pygame.image.load("data/shield.png"), (constants.CELL_WIDTH, constants.CELL_HEIGHT))]


#  ______   .______          __   _______   ______ .___________.    _______.
# /  __  \  |   _  \        |  | |   ____| /      ||           |   /       |
# |  |  |  | |  |_)  |       |  | |  |__   |  ,----'`---|  |----`  |   (----`
# |  |  |  | |   _  <  .--.  |  | |   __|  |  |         |  |        \   \
# |  `--'  | |  |_)  | |  `--'  | |  |____ |  `----.    |  |    .----)   |
# \______/  |______/   \______/  |_______| \______|    |__|    |_______/  


class obj_Actor:

    def __init__(self, x, y, name_object, animation, animation_speed = 1.0, creature=None, ai=None, container = None, item = None, equipment = None):
        self.x = x
        self.y = y
        self.name_object = name_object
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

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

            self.item = com_Item()
            self.item.owner = self

    @property
    def display_name(self):

        if self.creature:
            return (self.creature.name_instance + " the " + self.name_object)

        if self.item:
            if self.equipment and self.equipment.equipped:
                return (self.name_object + "(equipped)")
            else:
                return self.name_object



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

    def distance_to(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def move_towards(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)







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

    def __init__(self, name_instance, base_atk = 2, base_def = 0, hp=10, death_function=None):
        self.name_instance = name_instance
        self.base_atk = base_atk
        self.base_def = base_def
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):

        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            # im Tuturial ist das print unten rot aber anscheined geht es trotzdem
            self.attack(target)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target):

        damage_dealt = self.power - target.creature.defense

        game_message(
            self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage_dealt) + " damage!",
              constants.COLOR_WHITE)
        target.creature.take_damage(damage_dealt)

    def take_damage(self, damage):
        self.hp -= damage
        game_message(self.name_instance + "`s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

        if self.hp <= 0:

            if self.death_function is not None:
                self.death_function(self.owner)

    def heal(self, value):

        self.hp + value

        if self.hp > self.maxhp:
            self.hp = self.maxhp

    @property
    def power(self):

        total_power = self.base_atk

        if self.owner.container:
            object_bonuses = [obj.equipment.attack_bonus for obj in self.owner.container.equipped_items]

            for bonus in object_bonuses:
                if bonus:
                    total_power += bonus

        return total_power

    @property
    def defense(self):

        total_defense = self.base_def

        if self.owner.container:
            object_bonuses = [obj.equipment.defense_bonus for obj in self.owner.container.equipped_items]

            for bonus in object_bonuses:
                if bonus:
                    total_defense += bonus

        return total_defense

class com_Container(object):

    def __init__(self, volume = 10.0, inventory = []):
        self.inventory = inventory
        self.max_volume = volume
        self._volume = 0.0


    @property
    def volume(self):
        return self._volume

    ## TODO Get Names of everything in inventory

    @property
    def equipped_items(self):

        list_of_equipped_items = [obj for obj in self.inventory if obj.equipment and obj.equipment.equipped]

        return list_of_equipped_items


    ## TODO Get weight of everything in cointainer

class com_Item:
    def __init__(self, weight = 0.0, volume = 0.0, use_function = None, value = None):
        self.weight = weight
        self.volume = volume
        self.value = value
        self.use_function = use_function
        self.container = None

    ## Pick up this item
    def pick_up(self, actor):

        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
                game_message("Not enough room to pick up")

            else:
                game_message("Picked up")
                actor.container.inventory.append(self.owner)
                GAME.current_objects.remove(self.owner)
                self.container = actor.container

    ## Drop Item
    def drop(self, new_x, new_y):
        GAME.current_objects.append(self.owner)
        self.container.inventory.remove(self.owner)
        self.owner.x = new_x
        self.owner.y = new_y
        game_message("Item dropped")
        self.container = None


    ##  Use item
    def use(self):

        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return



        if self.use_function:
            result = self.use_function(self.container.owner, self.value)

            if result is not None:
                print("use function failed")

            else:
                self.container.inventory.remove(self.owner)

class com_Equipment:

    def __init__(self, attack_bonus = None, defense_bonus = None, slot = None):

        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.slot = slot

        self.equipped = False

    def toggle_equip(self):

        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):

        # check for equ in slot
        #TODO change this to be different
        all_equipped_items = self.owner.item.container.equipped_items


        for item in all_equipped_items:
            if item.equipment.slot and (item.equipment.slot == self.slot):
                game_message("Equipment slot is occupied!", constants.COLOR_RED)
                return

        # toggle self.equipped
        self.equipped = True

        game_message("Item equipped")

    def unequip(self):

        # toggle self.equipped
        self.equipped = False

        game_message("Item uneqipped")

#   _____  .___ 
#  /  _  \ |   |
# /  /_\  \|   |
# /    |    \   |
# \____|__  /___|
#        \/ 

class ai_Confuse:

    def __init__(self, old_ai, num_turns):

        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:
            self.owner.creature.move(tcod.random_get_int(None, -1, 1), tcod.random_get_int(None, -1, 1))

            self.num_turns -= 1

        else:
            self.owner.ai = self.old_ai

            game_message( self.owner.display_name + " has broken free!" , constants.COLOR_GREEN)

class ai_Chase:
    # A basic AI which chases the player and tries to bump into him



    def take_turn(self):
        monster = self.owner

        if tcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):

            # Move to the player if far away
            if monster.distance_to(PLAYER) >= 2:
                self.owner.move_towards(PLAYER)

            # if close enough, attack player
            elif PLAYER.creature.hp > 0:
                monster.creature.attack(PLAYER)




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

def map_find_line(coords1, coords2, include_origin=False):
    'Converts who x,y coords into a list of tiles. coords1 = (x1, y1) coords2 = (x2, y2)'

    x1, y1 = coords1
    x2, y2 = coords2

    if x1 == x2 and y1 == y2:
        return [(x1, y1)]

    if include_origin:
        return list(tcod.line_iter(x1, y1, x2, y2))
    else:
        tmp = tcod.line_iter(x1, y1, x2, y2)
        tmp.__next__()
        return list(tmp)

def map_check_for_wall(x,y):
    return GAME.current_map[x][y].block_path

def map_find_radius(coords, radius):

    center_x, center_y = coords

    tile_list = []

    start_x = (center_x - radius)
    end_x =  (center_x + radius +1)

    start_y = (center_y - radius)
    end_y = (center_y + radius +1)

    for x in range(start_x ,end_x ):
        for y in range(start_y, end_y):
            tile_list.append((x,y))

    return tile_list

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

def draw_text(display_surface, text_to_display, T_coords, text_color, back_color=None, center = False):
    # This function takes in some text and display

    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)
    if not center:
        text_rect.topleft = T_coords
    else:
        text_rect.center = T_coords

    display_surface.blit(text_surf, text_rect)

def draw_tile_rect(coords, color=None, tile_alpha = None, mark = None):

    x, y = coords

    if color:
        local_color = color
    else:
        local_color = constants.COLOR_WHITE


    if tile_alpha:
        local_alpha = tile_alpha
    else:
        local_alpha = 200

    new_x = x * constants.CELL_WIDTH
    new_y = y * constants.CELL_HEIGHT

    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))

    new_surface.fill(local_color)

    new_surface.set_alpha(local_alpha)

    if mark:
        draw_text(new_surface,"X",(constants.CELL_WIDTH/2, constants.CELL_HEIGHT/2),constants.COLOR_BLACK, center = True)


    SURFACE_MAIN.blit(new_surface, (int(new_x), int(new_y)))





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

def helper_text_width(font):

    (width, height) = font.size("A")

    return width



#o   o   O   o-o  o-O-o   o-o
#|\ /|  / \ o       |    /
#| O | o---o|  -o   |   O
#|   | |   |o   |   |    \
#o   o o   o o-o  o-O-o   o-o

def cast_heal(target, value):

    if target.creature.hp == target.creature.maxhp:
        game_message("HP is allready full")

    else:
        game_message(target.name_object + " healed for " + str(value) + " HP")
        target.creature.heal(value)
        print(target.creature.hp)



    return None

def cast_lightning(damage):

    player_location = (PLAYER.x, PLAYER.y)


    # prompt player for a tile
    point_selected = menu_tile_select(coords_origin=player_location,  max_range=5, penetrate_walls=False)

    if point_selected:
        list_of_tiles = map_find_line(player_location, point_selected)

        for i, (x, y) in enumerate(list_of_tiles):

            target = map_check_for_creature(x, y)

            if target:
                target.creature.take_damage(damage)

def cast_fireball(caster, value):

    # defs
    damage = 5
    local_radius = 1
    max_r = 4
    player_location = (PLAYER.x, PLAYER.y)

    point_selected = menu_tile_select(coords_origin=player_location, max_range=max_r, penetrate_walls=False, pierce_creature=False, radius=local_radius)

    #get sequence of tiles
    tiles_to_damage = map_find_radius(point_selected, local_radius)

    creature_hit = False


    #damage all creatures in tiles
    for (x,y) in tiles_to_damage:
        creature_to_damage = map_check_for_creature(x,y)

        if creature_to_damage:
            creature_to_damage.creature.take_damage(damage)

            if creature_to_damage is not PLAYER:
                creature_hit = True

    if creature_hit:
        game_message("The fire rages and evaporates all flesh it came in contact with. Its nearly as hot as Alina Paul", constants.COLOR_RED)

def cast_confusion():

    #select tile
    point_selected = menu_tile_select()

    # get target
    if point_selected:
        (tile_x, tile_y) = point_selected
        target = map_check_for_creature(tile_x, tile_y)

        if target:
            #temporarily confuse monster
            old_ai = target.ai
            target.ai = ai_Confuse(old_ai, num_turns = 5)
            target.ai.owner = target

            game_message("The creature is confused", constants.COLOR_GREEN)












#.___  ___.  _______ .__   __.  __    __       _______.
#|   \/   | |   ____||  \ |  | |  |  |  |     /       |
#|  \  /  | |  |__   |   \|  | |  |  |  |    |   (----`
#|  |\/|  | |   __|  |  . `  | |  |  |  |     \   \
#|  |  |  | |  |____ |  |\   | |  `--'  | .----)   |
#|__|  |__| |_______||__| \__|  \______/  |_______/

def menu_pause():
    #This Menu pauses the game and displays a simple message in the center of THE MAP (not the screen [danke markus mit deinem vollbild kack :P])

    menu_close = False

    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    menu_text = "PAUSED"
    menu_font = ASSETS.FONT_DEBUG_MESSAGE

    text_height = helper_text_height(menu_font)
    text_width = len(menu_text) * helper_text_width(menu_font)



    while not menu_close:

        events_list = pygame.event.get()

        for event in events_list:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    menu_close = True

        draw_text(SURFACE_MAIN, menu_text, ((window_width /2) - (text_width /2), (window_height / 2)- (text_height / 2)),constants.COLOR_BLACK, constants.COLOR_WHITE)

        CLOCK.tick(constants.GAME_FPS)

        #Man Muss das jedes mal updaten wenn man was malt
        pygame.display.flip()

def menu_inventory():



    # Initalize to False, when True, the menu closes
    menu_close = False

    # Calculate window dimensions
    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    # Menu characteristcs
    menu_width = 200
    menu_height = 200
    menu_x = (window_width /2) - (menu_width / 2)
    menu_y = (window_height / 2)- (menu_height / 2)

    # Menu text characteristcs
    menu_text_font = ASSETS.FONT_MESSAGE_TEXT

    # Helper var
    menu_text_height = helper_text_height(menu_text_font)

    local_inventory_surface = pygame.Surface((menu_width, menu_height))

    while not menu_close:

        #Clear the menu
        local_inventory_surface.fill(constants.COLOR_BLACK)

        # TODO Register Changes
        print_list = [obj.display_name for obj in PLAYER.container.inventory]

        events_list = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_x_rel = mouse_x - menu_x
        mouse_y_rel = mouse_y - menu_y

        mouse_in_window = (mouse_x_rel > 0 and
                           mouse_y_rel > 0 and
                           mouse_x_rel < menu_width and
                           mouse_y_rel < menu_height)

        pepegarechnung = mouse_y_rel / menu_text_height
        mouse_line_selection = int(pepegarechnung)

        for event in events_list:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_i:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (mouse_in_window and mouse_line_selection <= len(print_list)-1):
                        PLAYER.container.inventory[mouse_line_selection].item.use()



        ##Draw the list
        for line, (name) in enumerate(print_list):

            if int(line) == int(mouse_line_selection) and mouse_in_window:
                draw_text(local_inventory_surface, name, (0, 0 + (line * constants.INVENTORY_TEXT_HEIGHT)),
                          constants.COLOR_WHITE, constants.COLOR_GREY)

            else:
                draw_text(local_inventory_surface, name, (0, 0 + (line * constants.INVENTORY_TEXT_HEIGHT)),
                          constants.COLOR_WHITE)





        # Render Game
        draw_game()

        # Display Menu
        SURFACE_MAIN.blit(local_inventory_surface, (menu_x , menu_y ))

        CLOCK.tick(constants.GAME_FPS)

        pygame.display.update()

def menu_tile_select(coords_origin=None, max_range=None, penetrate_walls=True, pierce_creature=False, radius = None):
    """
    """
    #This menu let the player select a tile.
    #It pauses the game and produces an on screen rectangle when the player presses the mb will return the map address

    menu_close = False

    while not menu_close:

        #Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Get button clicks
        events_list = pygame.event.get()

        #Mouse mao selection
        map_coord_x = mouse_x / constants.CELL_WIDTH
        map_coord_y = mouse_y / constants.CELL_HEIGHT

        # transform into integers
        int_x = int(map_coord_x)
        int_y = int(map_coord_y)

        valid_tiles = []

        if coords_origin:
            full_list_tiles = map_find_line(coords_origin, (int_x, int_y))
            for i, (x, y) in enumerate(full_list_tiles):

                valid_tiles.append((x,y))

                #if max_range and i == max_range - 1:
                #    print("HIER")
                #   break

                if not penetrate_walls and map_check_for_wall(x,y):
                    break

                if not pierce_creature and map_check_for_creature(x,y):
                    break

            if max_range:
                valid_tiles = valid_tiles[:max_range]
        else:
            valid_tiles = [(int_x, int_y)]

        # return map_cords when left mb is pressed
        for event in events_list:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_l:
                        menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    return (valid_tiles[-1])




        #Draw Game first
        draw_game()

        draw_tile_rect((int_x, int_y))
        #Draw Rectangle at mouse position on top of game, dont draw the last tile in grey
        for (tile_x, tile_y) in valid_tiles[:-1]:
            draw_tile_rect((tile_x,tile_y), constants.COLOR_GREY)
        last_tile_x,last_tile_y = valid_tiles[-1]
        draw_tile_rect((last_tile_x,last_tile_y), constants.COLOR_RED, mark= "X")

        if radius:
            area_effect = map_find_radius(valid_tiles[-1], radius)

            for (tile_x, tile_y) in area_effect:
                draw_tile_rect((tile_x, tile_y))

        # update the display
        pygame.display.flip()

        # tick the CLOCK
        CLOCK.tick(constants.GAME_FPS)















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

        # update the display
        pygame.display.flip()

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

    pygame.key.set_repeat(200, 70)

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
    creature_com1 = com_Creature("SPIELER")
    PLAYER = obj_Actor(1, 1, "python", ASSETS.A_PLAYER, animation_speed = 0.5, creature=creature_com1, container = container_com1)

    item_com1 = com_Item(value = 4, use_function = cast_heal)
    creature_com2 = com_Creature("Healkrabbe", death_function=death_monster)
    ai_com1 = ai_Chase()
    ENEMY = obj_Actor(2, 2, "crab", ASSETS.A_ENEMY, creature=creature_com2, ai=ai_com1, item = item_com1)

    item_com2 = com_Item(value = 5, use_function = cast_fireball)
    creature_com3 = com_Creature("Feuerballkrabbe", death_function=death_monster)
    ai_com2 = ai_Chase()
    ENEMY2 = obj_Actor(7, 2, "BOB", ASSETS.A_ENEMY, creature=creature_com3, ai=ai_com2, item=item_com2)

    #create a sword
    equipment_com1 = com_Equipment(attack_bonus= 2, slot = "hand_right")
    SWORD = obj_Actor(2,3,"Short-Sword", ASSETS.S_SWORD, equipment= equipment_com1)

    #create a shield
    equipment_com2 = com_Equipment(defense_bonus= 2, slot = "hand_left")
    SHIELD = obj_Actor(3, 3, "Buckler", ASSETS.S_SHIELD, equipment=equipment_com2)

    # create a sword2
    equipment_com3 = com_Equipment(attack_bonus=2, slot = "hand_right")
    SWORD2 = obj_Actor(2, 4, "Short-Sword", ASSETS.S_SWORD, equipment=equipment_com3)

    GAME.current_objects = [PLAYER, ENEMY, ENEMY2, SWORD, SHIELD, SWORD2]


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

            if event.key == pygame.K_d:
                if len(PLAYER.container.inventory) > 0:
                    PLAYER.container.inventory[-1].item.drop(PLAYER.x, PLAYER.y)

            if event.key == pygame.K_p:
                game_message("Game resumed", constants.COLOR_WHITE)
                menu_pause()

            if event.key == pygame.K_i:
                menu_inventory()

            if event.key == pygame.K_l:
                menu_tile_select()

            if event.key == pygame.K_k:
                cast_confusion()

            if event.key == pygame.K_m:
                cast_lightning(10)



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
