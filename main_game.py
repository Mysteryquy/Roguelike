# 3rd party modules#3rd party modules
# capital bruh

import pygame
import tcod
import tcod.map
import os
import ctypes
import math
import pickle
import gzip
import random

# gamefiles
import constants


# a88888b. dP     dP   .d888888  888888ba   .88888.   88888888b dP         .88888.   .88888.
# d8'   `88 88     88  d8'    88  88    `8b d8'   `88  88        88        d8'   `8b d8'   `88
# 88        88aaaaa88a 88aaaaa88a 88     88 88        a88aaaa    88        88     88 88
# 88        88     88  88     88  88     88 88   YP88  88        88        88     88 88   YP88
# Y8.   .88 88     88  88     88  88     88 Y8.   .88  88        88        Y8.   .8P Y8.   .88
# Y88888P' dP     dP  88     88  dP     dP  `88888'   88888888P 88888888P  `8888P'   `88888'
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo


# TODO :
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
        # Sprite sheets#
        self.charspritesheet = obj_Spritesheet("data/Reptiles.png")
        self.enemyspritesheet = obj_Spritesheet("data/ROFL.png")
        self.scrollspritesheet = obj_Spritesheet("data/Scroll.png")
        self.reptile = obj_Spritesheet("data/Reptile0.png")
        self.flesh = obj_Spritesheet("data/Flesh.png")
        self.tile = obj_Spritesheet("data/Tile.png")
        self.rodent = obj_Spritesheet("data/Rodent0.png")

        # ANIMATIONS#
        self.A_PLAYER = self.charspritesheet.get_animation("m", 5, 16, 16, 4, (32, 32))
        self.A_ENEMY = self.enemyspritesheet.get_animation("k", 1, 16, 16, 2, (32, 32))
        self.A_SNAKE_01 = self.reptile.get_animation("d", 4, 16, 16, 2, (32, 32))
        self.A_SNAKE_02 = self.reptile.get_animation("a", 4, 16, 16, 2, (32, 32))
        self.A_MOUSE_01 = self.rodent.get_animation("a", 2, 16, 16, 2, (32, 32))

        # SPRITES#
        self.S_WALL = pygame.image.load("data/wall2.jpg")
        self.S_WALLEXPLORED = pygame.image.load("data/wallunseen2.png")

        self.S_FLOOR = pygame.image.load("data/floor.jpg")
        self.S_FLOOREXPLORED = pygame.image.load("data/floorunseen2.png")

        # FONTS#
        self.FONT_DEBUG_MESSAGE = pygame.font.Font("data/joystix.ttf", 20)
        self.FONT_MESSAGE_TEXT = pygame.font.Font("data/joystix.ttf", 20)
        self.FONT_CURSOR_TEXT = pygame.font.Font("data/joystix.ttf", constants.CELL_HEIGHT)

        ## ITEMS ##
        self.S_SWORD = [
            pygame.transform.scale(pygame.image.load("data/sword.png"), (constants.CELL_WIDTH, constants.CELL_HEIGHT))]
        self.S_SHIELD = [
            pygame.transform.scale(pygame.image.load("data/shield.png"), (constants.CELL_WIDTH, constants.CELL_HEIGHT))]
        self.S_SCROLL_01 = self.scrollspritesheet.get_image("a", 5, 16, 16, (32, 32))
        self.S_SCROLL_02 = self.scrollspritesheet.get_image("a", 2, 16, 16, (32, 32))
        self.S_SCROLL_03 = self.scrollspritesheet.get_image("b", 2, 16, 16, (32, 32))
        self.S_FLESH_SNAKE = self.flesh.get_image("a", 3, 16, 16, (32, 32))
        self.S_FLESH_EAT = self.flesh.get_image("a", 1, 16, 16, (32, 32))

        ## SPECIAL ##

        self.S_STAIRS_DOWN = self.tile.get_image("b", 2, 16, 16, (32, 32))
        self.S_STAIRS_UP = self.tile.get_image("a", 2, 16, 16, (32, 32))

        self.animation_dict = {
            "A_PLAYER": self.A_PLAYER,
            "A_ENEMY": self.A_ENEMY,
            "A_SNAKE_01": self.A_SNAKE_01,
            "A_SNAKE_02": self.A_SNAKE_02,
            "A_MOUSE_01": self.A_MOUSE_01,

            ## ITEMS ##
            "S_SWORD": self.S_SWORD,
            "S_SHIELD": self.S_SHIELD,
            "S_SCROLL_01": self.S_SCROLL_01,
            "S_SCROLL_02": self.S_SCROLL_02,
            "S_SCROLL_03": self.S_SCROLL_03,
            "S_FLESH_SNAKE": self.S_FLESH_SNAKE,

            "S_STAIRS_DOWN": self.S_STAIRS_DOWN,
            "S_STAIRS_UP": self.S_STAIRS_UP,
            "S_FLESH_EAT": self.S_FLESH_EAT
        }

        ## AUDIO ##
        self.music_main_menu = "data/audio/Broke.mp3"
        self.music_lvl_1 = "data/audio/level_1.mp3"
        self.snd_hit_1 = pygame.mixer.Sound("data/audio/hit_hurt1.wav")
        self.snd_hit_2 = pygame.mixer.Sound("data/audio/hit_hurt2.wav")
        self.snd_hit_3 = pygame.mixer.Sound("data/audio/hit_hurt3.wav")

        self.snd_list_hit = [self.snd_hit_1, self.snd_hit_2, self.snd_hit_3 ]




#  ______   .______          __   _______   ______ .___________.    _______.
# /  __  \  |   _  \        |  | |   ____| /      ||           |   /       |
# |  |  |  | |  |_)  |       |  | |  |__   |  ,----'`---|  |----`  |   (----`
# |  |  |  | |   _  <  .--.  |  | |   __|  |  |         |  |        \   \
# |  `--'  | |  |_)  | |  `--'  | |  |____ |  `----.    |  |    .----)   |
# \______/  |______/   \______/  |_______| \______|    |__|    |_______/  


class obj_Actor:

    def __init__(self, x, y, name_object, animation_key, animation_speed=1.0, creature=None, ai=None, container=None,
                 item=None, equipment=None, stairs=None):
        self.x = round(x)
        self.y = round(y)
        self.name_object = name_object
        self.animation_key = animation_key
        self.animation = ASSETS.animation_dict[self.animation_key]  # number of images
        self.animation_speed = animation_speed / 1.0  # in seconds

        # animation flicker speed
        self.flicker_speed = self.animation_speed / len(self.animation)
        self.flicker_timer = 0.0
        self.sprite_image = 0  # s

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

        self.stairs = stairs
        if self.stairs:
            self.stairs.owner = self

    @property
    def display_name(self):

        if self.creature:
            return self.creature.name_instance + " the " + self.name_object

        if self.item:
            if self.equipment and self.equipment.equipped:
                return self.name_object + "(equipped)"
            else:
                return self.name_object

    def draw(self):
        is_visible = FOV_MAP.fov[self.y, self.x]

        if is_visible:
            if len(self.animation) == 1:
                SURFACE_MAP.blit(self.animation[0], (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

            elif len(self.animation) > 1:
                if CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1 / CLOCK.get_fps()

                if self.flicker_timer >= self.flicker_speed:
                    self.flicker_timer = 0.0

                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0

                    else:
                        self.sprite_image += 1

                SURFACE_MAP.blit(self.animation[self.sprite_image],
                                 (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

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

    def move_away(self, other):

        dx = self.x - other.x
        dy = self.y - other.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)

    def animation_destroy(self):

        self.animation = None

    def animation_init(self):

        self.animation = ASSETS.animation_dict[self.animation_key]  # number of images


class obj_Game:
    def __init__(self):

        self.message_history = []

        self.current_objects = []

        self.maps_previous = []

        self.maps_next = []

        self.current_map, self.current_rooms = map_create()

    def transition_next(self):
        global FOV_CALCULATE

        FOV_CALCULATE = True

        for obj in self.current_objects:
            obj.animation_destroy()

        self.maps_previous.append((PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_objects))

        if len(self.maps_next) == 0:

            self.current_objects = [PLAYER]

            PLAYER.animation_init()

            self.current_map, self.current_rooms = map_create()

            map_place_objects(self.current_rooms)

        else:
            (PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_next[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map_make_fov(self.current_map)

            FOV_CALCULATE = True

            del self.maps_next[-1]

    def transition_previous(self):
        global FOV_CALCULATE

        if len(self.maps_previous) != 0:

            for obj in self.current_objects:
                obj.animation_destroy()

            self.maps_next.append((PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_objects))

            (PLAYER.x, PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_previous[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map_make_fov(self.current_map)

            FOV_CALCULATE = True

            del self.maps_previous[-1]
        else:
            game_message("There is no previous level", constants.COLOR_WHITE)


class obj_Spritesheet:  # Bilder von Spritesheets holen

    def __init__(self, file_name):
        # Den Sheet laden.
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.tiledict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11,
                         "l": 12, "m": 13, "n": 14, "o": 15, "p": 16}

        ###############

    def get_image(self, column, row, width=constants.CELL_WIDTH, height=constants.CELL_HEIGHT, scale=None):

        image_list = []

        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column] * width, row * height, width, height))

        image.set_colorkey(constants.COLOR_BLACK)

        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))

        image_list.append(image)

        return image_list

    def get_animation(self, column, row, width=constants.CELL_WIDTH, height=constants.CELL_HEIGHT, num_sprites=1,
                      scale=None):

        image_list = []

        for i in range(num_sprites):
            # Create blank image
            image = pygame.Surface([width, height]).convert()

            # copy image from sheet onto blank
            image.blit(self.sprite_sheet, (0, 0),
                       (self.tiledict[column] * width + (width * i), row * height, width, height))

            # set transparency to black
            image.set_colorkey(constants.COLOR_BLACK)

            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))

            image_list.append(image)

        return image_list


class obj_Room:
    # This is a rectangle that lives on the map

    def __init__(self, coords, size):
        self.x1, self.y1 = coords
        self.w, self.h = size

        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    @property
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2

        return center_x, center_y

    def intercept(self, other):
        # return True if other obj intersects with this one
        objects_intersect = (
                self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

        return objects_intersect


class obj_Camera:

    def __init__(self):
        self.width = constants.CAMERA_WIDTH
        self.height = constants.CAMERA_HEIGHT
        self.x, self.y = (0, 0)

    def update(self):
        target_x = PLAYER.x * constants.CELL_WIDTH + (constants.CELL_WIDTH / 2)
        target_y = PLAYER.y * constants.CELL_HEIGHT + (constants.CELL_HEIGHT / 2)

        distance_x, distance_y = self.map_dist((target_x, target_y))

        # Durch das 1 kann der Effekt erzeugt werden, dass die Cam dem Spieler "folgt" und nicht an ihm festgeklebt ist. Kann geändert werden nach Geschmack
        self.x += int(distance_x * 1)
        self.y += int(distance_y * 1)

    @property
    def rectangle(self):
        pos_rect = pygame.Rect((0, 0), (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

        pos_rect.center = (self.x, self.y)

        return pos_rect

    @property
    def map_address(self):
        map_x = self.x / constants.CELL_WIDTH
        map_y = self.y / constants.CELL_HEIGHT

        return map_x, map_y

    def win_to_map(self, coords):
        tar_x, tar_y = coords

        # convert window coords to distance from camera
        cam_d_x, cam_d_y = self.cam_dist((tar_x, tar_y))

        # distance from cam -> map cords
        map_p_x = self.x + cam_d_x
        map_p_y = self.y + cam_d_y

        return map_p_x, map_p_y

    def map_dist(self, coords):
        new_x, new_y = coords

        dist_x = new_x - self.x
        dist_y = new_y - self.y

        return dist_x, dist_y

    def cam_dist(self, coords):
        win_x, win_y = coords

        dist_x = win_x - (self.width / 2)
        dist_y = win_y - (self.height / 2)

        return dist_x, dist_y


#                                                         __
#  ____  ____   _____ ______   ____   ____   ____   _____/  |_  ______
# _/ ___\/  _ \ /     \\____ \ /  _ \ /    \_/ __ \ /    \   __\/  ___/
# \  \__(  <_> )  Y Y  \  |_> >  <_> )   |  \  ___/|   |  \  |  \___ \
# \___  >____/|__|_|  /   __/ \____/|___|  /\___  >___|  /__| /____  >
#     \/            \/|__|               \/     \/     \/          \/ 


class com_Creature:

    def __init__(self, name_instance, base_atk=2, base_def=0, hp=10, death_function=None):
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

        if damage_dealt > 0 and self.owner is PLAYER:
            pygame.mixer.Sound.play(RANDOM_ENGINE.choice(ASSETS.snd_list_hit))

    def take_damage(self, damage):
        self.hp -= damage
        game_message(self.name_instance + "`s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

        if self.hp <= 0:

            if self.death_function is not None:
                self.death_function(self.owner)

    def heal(self, value):

        self.hp = self.hp + value

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

    def __init__(self, volume=10.0, inventory=None):
        if inventory is None:
            inventory = []
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
    def __init__(self, weight=0.0, volume=0.0, use_function=None, value=None, pickup_text=None):
        self.weight = weight
        self.volume = volume
        self.value = value
        self.use_function = use_function
        self.pickup_text = pickup_text
        self.container = None

    ## Pick up this item
    def pick_up(self, actor):

        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
                game_message("Not enough room to pick up")

            else:
                if self.pickup_text:
                    game_message("Picked up " + self.pickup_text)
                else:
                    game_message("Picked up")
                actor.container.inventory.append(self.owner)
                self.owner.animation_destroy()
                GAME.current_objects.remove(self.owner)
                self.container = actor.container

    ## Drop Item
    def drop(self, new_x, new_y):
        GAME.current_objects.append(self.owner)
        self.owner.animation_init()
        self.container.inventory.remove(self.owner)
        self.owner.x = new_x
        self.owner.y = new_y
        game_message("Item dropped")

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

    def __init__(self, attack_bonus=None, defense_bonus=None, slot=None, equip_text=None):

        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.slot = slot
        self.equip_text = equip_text
        self.equipped = False

    def toggle_equip(self):

        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):

        # check for equ in slot
        all_equipped_items = self.owner.item.container.equipped_items

        for item in all_equipped_items:
            if item.equipment.slot and (item.equipment.slot == self.slot):
                game_message("Equipment slot is occupied!", constants.COLOR_RED)
                return

        # toggle self.equipped
        self.equipped = True
        if self.equip_text:
            game_message("Equipped the " + self.equip_text)
        else:
            game_message("Item equipped")

    def unequip(self):

        # toggle self.equipped
        self.equipped = False

        game_message("Item uneqipped")


class com_Stairs:

    def __init__(self, downwards=True):

        self.downwards = downwards

    def use(self):

        if self.downwards:
            GAME.transition_next()
        else:
            GAME.transition_previous()


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

            game_message(self.owner.display_name + " has broken free!", constants.COLOR_GREEN)


def map_is_visible(x, y):
    global FOV_MAP

    return FOV_MAP.fov[y, x]


class ai_Chase:
    # A basic AI which chases the player and tries to bump into him
    # TODO Let the creature move around walls

    def take_turn(self):
        monster = self.owner

        # if tcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):

        if map_is_visible(monster.x, monster.y):
            # Move to the player if far away
            if monster.distance_to(PLAYER) >= 2:
                self.owner.move_towards(PLAYER)

            # if close enough, attack player
            elif PLAYER.creature.hp > 0:
                monster.creature.attack(PLAYER)


class ai_Flee:

    def take_turn(self):
        monster = self.owner

        if tcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):
            self.owner.move_away(PLAYER)


def death_snake(monster):
    # On death, most monsters stop moving tho
    game_message(monster.creature.name_instance + " is slaughtered into ugly bits of flesh!", constants.COLOR_GREY)
    # print (monster.creature.name_instance + " is slaughtered into ugly bits of flesh!")
    monster.animation = ASSETS.S_FLESH_SNAKE
    monster.animation_key = "S_FLESH_SNAKE"
    monster.creature = None
    monster.ai = None


def death_mouse(mouse):
    # On death, most monsters stop moving tho
    game_message(mouse.creature.name_instance + " is killed. Eat it to heal up a bit!", constants.COLOR_GREY)
    # print (monster.creature.name_instance + " is slaughtered into ugly bits of flesh!")
    mouse.animation = ASSETS.S_FLESH_EAT
    mouse.animation_key = "S_FLESH_EAT"
    mouse.creature = None
    mouse.ai = None


# .___  ___.      ___      .______
# |   \/   |     /   \     |   _  \
# |  \  /  |    /  ^  \    |  |_)  |
# |  |\/|  |   /  /_\  \   |   ___/
# |  |  |  |  /  _____  \  |  |
# |__|  |__| /__/     \__\ | _|

def map_create():
    global PLAYER
    new_map = [[struc_Tile(True) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    # generate new room
    list_of_rooms = []

    for i in range(constants.MAP_MAX_NUM_ROOMS):

        w = tcod.random_get_int(None, constants.ROOM_MIN_WIDTH, constants.ROOM_MAX_WIDTH)
        h = tcod.random_get_int(None, constants.ROOM_MIN_HEIGHT, constants.ROOM_MAX_HEIGHT)
        if len(list_of_rooms) == 0:
            x = 3
            y = 2
        else:
            x = tcod.random_get_int(None, 2, constants.MAP_WIDTH - w - 2)
            y = tcod.random_get_int(None, 2, constants.MAP_HEIGHT - h - 2)

        # create the room
        new_room = obj_Room((x, y), (w, h))

        failed = False

        # TODO check for interference
        for other_room in list_of_rooms:
            if new_room.intercept(other_room):
                failed = True
                break

        if not failed:

            map_create_room(new_map, new_room)
            current_center = new_room.center
            (x, y) = current_center
            current_center = (int(round(x)), int(round(y)))

            if len(list_of_rooms) != 0:
                previous_center = list_of_rooms[-1].center

                (x, y) = previous_center
                previous_center = (int(round(x)), int(round(y)))
                map_create_tunnels(current_center, previous_center, new_map)

            list_of_rooms.append(new_room)

    map_make_fov(new_map)

    return new_map, list_of_rooms


def map_create_room(new_map, new_room):
    for x in range(new_room.x1, new_room.x2):
        for y in range(new_room.y1, new_room.y2):
            new_map[x][y].block_path = False


def map_place_objects(room_list):
    global PLAYER

    top_level = (len(GAME.maps_previous) == 0)

    for room in room_list:

        first_room = (room == room_list[0])
        last_room = (room == room_list[-1])

        if first_room:
            x, y = room.center
            PLAYER.x, PLAYER.y = int(x), int(y)

        if first_room and not top_level:
            gen_stairs((PLAYER.x, PLAYER.y), downwards=False)

        if last_room:
            gen_stairs(room.center)

        x = tcod.random_get_int(None, room.x1 + 1, room.x2 - 1)
        y = tcod.random_get_int(None, room.y1 + 1, room.y2 - 1)

        gen_enemy((x, y))

        x = tcod.random_get_int(None, room.x1 + 1, room.x2 - 1)
        y = tcod.random_get_int(None, room.y1 + 1, room.y2 - 1)

        gen_item((x, y))


def map_create_tunnels(coords1, coords2, new_map):
    coin_flip = (tcod.random_get_int(None, 0, 1) == 1)

    (x1, y1) = coords1
    (x2, y2) = coords2

    if coin_flip:
        for x in range(min(x1, x2), max(x1, x2)):
            new_map[x][y1].block_path = False
        for y in range(min(y1, y2), max(y1, y2)):
            new_map[x2][y].block_path = False

    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            new_map[x1][y].block_path = False
        for x in range(min(x1, x2), max(x1, x2) + 1):
            new_map[x][y2].block_path = False


def map_check_for_creature(x, y, exclude_object=None):
    target = None

    if exclude_object:
        # ceck objectlist to find creature at that location that isnt excluded
        for obj in GAME.current_objects:
            if (obj is not exclude_object and
                    obj.x == x and
                    obj.y == y and
                    obj.creature):
                target = obj

            if target:
                return target

    else:
        # ceck objectlist to find any creature at that location
        for obj in GAME.current_objects:
            if (obj.x == x and
                    obj.y == y and
                    obj.creature):
                target = obj

            if target:
                return target


def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = tcod.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            # same as before, but now we have array for walkable and transparent
            FOV_MAP.walkable[x][y] = not incoming_map[x][y].block_path
            FOV_MAP.transparent[y][x] = not incoming_map[x][y].block_path


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
    """Converts who x,y coords into a list of tiles. coords1 = (x1, y1) coords2 = (x2, y2)"""

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


def map_check_for_wall(x, y):
    return GAME.current_map[x][y].block_path


def map_find_radius(coords, radius):
    center_x, center_y = coords

    tile_list = []

    start_x = (center_x - radius)
    end_x = (center_x + radius + 1)

    start_y = (center_y - radius)
    end_y = (center_y + radius + 1)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            tile_list.append((x, y))

    return tile_list


# _______  .______          ___   ____    __    ____  __  .__   __.   _______
# |       \ |   _  \        /   \  \   \  /  \  /   / |  | |  \ |  |  /  _____|
# |  .--.  ||  |_)  |      /  ^  \  \   \/    \/   /  |  | |   \|  | |  |  __
# |  |  |  ||      /      /  /_\  \  \            /   |  | |  . `  | |  | |_ |
# |  '--'  ||  |\  \----./  _____  \  \    /\    /    |  | |  |\   | |  |__| |
# |_______/ | _| `._____/__/     \__\  \__/  \__/     |__| |__| \__|  \______|

def draw_game():
    global SURFACE_MAIN, SURFACE_MAP, GAME

    # clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    SURFACE_MAP.fill(constants.COLOR_BLACK)

    CAMERA.update()

    # draw the map
    draw_map(GAME.current_map)

    for obj in GAME.current_objects:
        obj.draw()

    SURFACE_MAIN.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)
    # print(CAMERA.rectangle)

    draw_debug()
    draw_messages()


def draw_map(map_to_draw):
    cam_x, cam_y = CAMERA.map_address
    display_map_w = constants.CAMERA_WIDTH / constants.CELL_WIDTH
    display_map_h = constants.CAMERA_HEIGHT / constants.CELL_HEIGHT

    render_w_min = int(cam_x - (display_map_w / 2))
    render_h_min = int(cam_y - (display_map_h / 2))
    render_w_max = int(cam_x + (display_map_w / 2))
    render_h_max = int(cam_y + (display_map_h / 2))

    if render_w_min < 0:
        render_w_min = 0
    if render_h_min < 0:
        render_h_min = 0
    if render_w_max > constants.MAP_WIDTH:
        render_w_max = constants.MAP_WIDTH
    if render_h_max > constants.MAP_HEIGHT:
        render_h_max = constants.MAP_HEIGHT

    for x in range(render_w_min, render_w_max):
        for y in range(render_h_min, render_h_max):

            is_visible = FOV_MAP.fov[y, x]
            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path:

                    SURFACE_MAP.blit(ASSETS.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    SURFACE_MAP.blit(ASSETS.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            elif map_to_draw[x][y].explored:

                if map_to_draw[x][y].block_path:  # Bruh was will der von mir

                    SURFACE_MAP.blit(ASSETS.S_WALLEXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    SURFACE_MAP.blit(ASSETS.S_FLOOREXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def draw_debug():
    draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), (0, 0), constants.COLOR_WHITE, constants.COLOR_BLACK)


def draw_messages():
    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history
    else:
        to_draw = GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_height(ASSETS.FONT_MESSAGE_TEXT)

    # info = pygame.display.Info()
    # screen_height = info.current_h

    start_y = (constants.CAMERA_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 5

    i = 0

    for message, color in to_draw:
        draw_text(SURFACE_MAIN, message, (0, start_y + i * text_height), color, constants.COLOR_BLACK)

        i += 1


def draw_text(display_surface, text_to_display, T_coords, text_color, back_color=None, center=False):
    # This function takes in some text and display

    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)
    if not center:
        text_rect.topleft = T_coords
    else:
        text_rect.center = T_coords

    display_surface.blit(text_surf, text_rect)


def draw_tile_rect(coords, color=None, tile_alpha=None, mark=None):
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
        draw_text(new_surface, "X", (constants.CELL_WIDTH / 2, constants.CELL_HEIGHT / 2), constants.COLOR_BLACK,
                  center=True)

    SURFACE_MAP.blit(new_surface, (int(new_x), int(new_y)))


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


# o   o   O   o-o  o-O-o   o-o
# |\ /|  / \ o       |    /
# | O | o---o|  -o   |   O
# |   | |   |o   |   |    \
# o   o o   o o-o  o-O-o   o-o

def cast_heal(caster, value):
    if caster.creature.hp == caster.creature.maxhp:
        game_message("HP is allready full")
        return "canceled"

    else:
        game_message(caster.name_object + " healed for " + str(value) + " HP")
        caster.creature.heal(value)
        print(caster.creature.hp)

    return None


def cast_lightning(caster, T_damage_maxrange):
    damage, m_range = T_damage_maxrange

    player_location = (caster.x, caster.y)

    # prompt player for a tile
    point_selected = menu_tile_select(coords_origin=player_location, max_range=m_range, penetrate_walls=False)

    if point_selected:
        list_of_tiles = map_find_line(player_location, point_selected)

        for i, (x, y) in enumerate(list_of_tiles):

            target = map_check_for_creature(x, y)

            if target:
                target.creature.take_damage(damage)


def cast_fireball(caster, T_damage_radius_range):
    # defs
    damage, local_radius, max_r = T_damage_radius_range

    player_location = (caster.x, caster.y)

    point_selected = menu_tile_select(coords_origin=player_location, max_range=max_r, penetrate_walls=False,
                                      pierce_creature=False, radius=local_radius)

    # get sequence of tiles
    tiles_to_damage = map_find_radius(point_selected, local_radius)

    creature_hit = False

    # damage all creatures in tiles
    for (x, y) in tiles_to_damage:
        creature_to_damage = map_check_for_creature(x, y)

        if creature_to_damage:
            creature_to_damage.creature.take_damage(damage)

            if creature_to_damage is not PLAYER:
                creature_hit = True

    if creature_hit:
        game_message("The fire rages and evaporates all flesh it came in contact with. Its nearly as hot as Alina Paul",
                     constants.COLOR_RED)


def cast_confusion(caster, effect_length):
    # select tile
    point_selected = menu_tile_select()

    # get target
    if point_selected:
        (tile_x, tile_y) = point_selected
        target = map_check_for_creature(tile_x, tile_y)

        if target:
            # temporarily confuse monster
            old_ai = target.ai
            target.ai = ai_Confuse(old_ai, num_turns=effect_length)
            target.ai.owner = target

            game_message("The creature is confused", constants.COLOR_GREEN)


#  o         o   __o__
# <|>       <|>    |
# / \       / \   / \
# \o/       \o/   \o/
#  |         |     |
# < >       < >   < >
#  \         /     |
#   o       o      o
#   <\__ __/>    __|>_

class ui_Button:

    def __init__(self,
                 surface,
                 button_text,
                 size,
                 center_coords,
                 color_box_mouseover=constants.COLOR_RED,
                 color_box_default=constants.COLOR_GREEN,
                 color_text_mouseover=constants.COLOR_WHITE,
                 color_text_default=constants.COLOR_GREY):

        self.surface = surface
        self.button_text = button_text
        self.size = size
        self.center_coords = center_coords

        self.c_box_mo = color_box_mouseover
        self.c_box_default = color_box_default
        self.c_text_mo = color_text_mouseover
        self.c_text_default = color_text_default
        self.c_c_box = color_box_default
        self.c_c_text = color_text_default

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center_coords

    def update(self, player_input):

        mouse_clicked = False

        local_events, local_mousepos = player_input
        mouse_x, mouse_y = local_mousepos

        mouse_over = (self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom)

        for event in local_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True

        if mouse_over and mouse_clicked:
            return True

        if mouse_over:
            self.c_c_box = self.c_box_mo
            self.c_c_text = self.c_text_mo
        else:
            self.c_c_box = self.c_box_default
            self.c_c_text = self.c_text_default

    def draw(self):

        pygame.draw.rect(self.surface, self.c_c_box, self.rect)
        draw_text(self.surface, self.button_text, self.center_coords, self.c_c_text, center=True)


# .___  ___.  _______ .__   __.  __    __       _______.
# |   \/   | |   ____||  \ |  | |  |  |  |     /       |
# |  \  /  | |  |__   |   \|  | |  |  |  |    |   (----`
# |  |\/|  | |   __|  |  . `  | |  |  |  |     \   \
# |  |  |  | |  |____ |  |\   | |  `--'  | .----)   |
# |__|  |__| |_______||__| \__|  \______/  |_______/

def menu_main():
    game_initialize()

    menu_running = True

    title_y = constants.CAMERA_HEIGHT / 2 - 40
    title_x = constants.CAMERA_WIDTH / 2
    title_text = "Untitled (but very cool) Game "

    SURFACE_MAIN.fill(constants.COLOR_BLACK)
    draw_text(SURFACE_MAIN, title_text, (title_x, title_y), constants.COLOR_RED, center=True)

    test_button = ui_Button(SURFACE_MAIN, "Start Game", (200, 45), (title_x, title_y + 40))

    pygame.mixer.music.load(ASSETS.music_main_menu)
    pygame.mixer.music.play(-1)

    while menu_running:

        list_of_events = pygame.event.get()
        mouse_position = pygame.mouse.get_pos()

        game_input = (list_of_events, mouse_position)

        for event in list_of_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                game_exit()

        if test_button.update(game_input):
            pygame.mixer.music.stop()
            game_start()


        test_button.draw()

        pygame.display.update()


def menu_pause():
    # This Menu pauses the game and displays a simple message in the center of THE MAP (not the screen [danke markus mit deinem vollbild kack :P])

    menu_close = False

    window_width = constants.CAMERA_WIDTH
    window_height = constants.CAMERA_HEIGHT

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

        draw_text(SURFACE_MAIN, menu_text,
                  ((window_width / 2) - (text_width / 2), (window_height / 2) - (text_height / 2)),
                  constants.COLOR_BLACK, constants.COLOR_WHITE)

        CLOCK.tick(constants.GAME_FPS)

        # Man Muss das jedes mal updaten wenn man was malt
        pygame.display.flip()


def menu_inventory():
    # Initalize to False, when True, the menu closes
    menu_close = False

    # Calculate window dimensions
    window_width = constants.CAMERA_WIDTH
    window_height = constants.CAMERA_HEIGHT

    # Menu characteristcs
    menu_width = 500
    menu_height = 400
    menu_x = (window_width / 2) - (menu_width / 2)
    menu_y = (window_height / 2) - (menu_height / 2)

    # Menu text characteristcs
    menu_text_font = ASSETS.FONT_MESSAGE_TEXT

    # Helper var
    menu_text_height = helper_text_height(menu_text_font)

    local_inventory_surface = pygame.Surface((menu_width, menu_height))

    while not menu_close:

        # Clear the menu
        local_inventory_surface.fill(constants.COLOR_BLACK)

        # TODO Register Changes
        print_list = [obj.display_name for obj in PLAYER.container.inventory]

        events_list = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_x_rel = mouse_x - menu_x
        mouse_y_rel = mouse_y - menu_y

        mouse_in_window = (0 < mouse_x_rel < menu_width and
                           0 < mouse_y_rel < menu_height)

        pepegarechnung = mouse_y_rel / constants.INVENTORY_TEXT_HEIGHT
        mouse_line_selection = int(pepegarechnung)

        for event in events_list:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_i:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse_in_window and mouse_line_selection <= len(print_list) - 1:
                        PLAYER.container.inventory[mouse_line_selection].item.use()
                        menu_close = True

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
        SURFACE_MAIN.blit(local_inventory_surface, (menu_x, menu_y))

        CLOCK.tick(constants.GAME_FPS)

        pygame.display.update()


def debug_tile_select():
    global GAME, FOV_MAP
    (x, y) = menu_tile_select()
    print((x, y))
    print(FOV_MAP.fov[y, x])


def menu_tile_select(coords_origin=None, max_range=None, penetrate_walls=True, pierce_creature=False, radius=None):
    """
    """
    # This menu let the player select a tile.
    # It pauses the game and produces an on screen rectangle when the player presses the mb will return the map address

    menu_close = False

    while not menu_close:

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Get button clicks
        events_list = pygame.event.get()

        mapx_pixel, mapy_pixel = CAMERA.win_to_map((mouse_x, mouse_y))

        # Mouse map selection
        map_coord_x = mapx_pixel / constants.CELL_WIDTH
        map_coord_y = mapy_pixel / constants.CELL_HEIGHT

        # transform into integers
        int_x = int(map_coord_x)
        int_y = int(map_coord_y)

        valid_tiles = []

        if coords_origin:
            full_list_tiles = map_find_line(coords_origin, (int_x, int_y))
            for i, (x, y) in enumerate(full_list_tiles):

                valid_tiles.append((x, y))

                if not penetrate_walls and map_check_for_wall(x, y):
                    break

                if not pierce_creature and map_check_for_creature(x, y):
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
                    return valid_tiles[-1]

        # Draw Game first
        SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
        SURFACE_MAP.fill(constants.COLOR_BLACK)

        CAMERA.update()

        # draw the map
        draw_map(GAME.current_map)

        for obj in GAME.current_objects:
            obj.draw()

        draw_tile_rect((int_x, int_y))  # Hier ?
        # Draw Rectangle at mouse position on top of game, dont draw the last tile in grey
        for (tile_x, tile_y) in valid_tiles[:-1]:
            draw_tile_rect((tile_x, tile_y), constants.COLOR_GREY)
        last_tile_x, last_tile_y = valid_tiles[-1]
        draw_tile_rect((last_tile_x, last_tile_y), constants.COLOR_RED, mark="X")

        if radius:
            area_effect = map_find_radius(valid_tiles[-1], radius)

            for (tile_x, tile_y) in area_effect:
                draw_tile_rect((tile_x, tile_y))

        SURFACE_MAIN.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)
        # print(CAMERA.rectangle)

        draw_debug()
        draw_messages()

        # update the display
        pygame.display.flip()

        # tick the CLOCK
        CLOCK.tick(constants.GAME_FPS)


#                                 _
#  __ _  ___ _ __   ___ _ __ __ _| |_ ___
# / _` |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \
# | (_| |  __/ | | |  __/ | | (_| | ||  __/
# \__, |\___|_| |_|\___|_|  \__,_|\__\___|
# |___/

##PLAYER##
def gen_player(coords):
    x, y = coords
    print(coords)

    container_com = com_Container()
    creature_com = com_Creature("SPIELER", base_atk=4)
    player = obj_Actor(x, y, "python", animation_key="A_PLAYER", animation_speed=0.5, creature=creature_com,
                       container=container_com)

    return player


##STRUCTURES##
def gen_stairs(coords, downwards=True):
    x, y = coords
    if downwards:
        stairs_com = com_Stairs()
        stairs = obj_Actor(x, y, "stairs", animation_key="S_STAIRS_DOWN", stairs=stairs_com)
    else:
        stairs_com = com_Stairs(downwards)
        stairs = obj_Actor(x, y, "stairs", animation_key="S_STAIRS_UP", stairs=stairs_com)

    GAME.current_objects.append(stairs)


##ITEMS##

def gen_item(coords):
    global GAME

    random_number = tcod.random_get_int(None, 1, 6)

    if random_number == 1:
        new_item = gen_scroll_confusion(coords)
    elif random_number == 2:
        new_item = gen_scroll_fireball(coords)
    elif random_number == 3:
        new_item = gen_scroll_confusion(coords)
    elif random_number == 4:
        new_item = gen_weapon_sword(coords)
    elif random_number == 5:
        new_item = gen_armor_shield(coords)
    else:
        new_item = gen_scroll_lighning(coords)

    GAME.current_objects.append(new_item)


def gen_scroll_lighning(coords):
    x, y = coords

    damage = tcod.random_get_int(None, 5, 7)
    m_range = tcod.random_get_int(None, 5, 7)

    item_com = com_Item(use_function=cast_lightning, value=(damage, m_range), pickup_text="Lightning Scroll")

    return_object = obj_Actor(x, y, "lightning scroll", animation_key="S_SCROLL_01", item=item_com)

    return return_object


def gen_scroll_fireball(coords):
    x, y = coords

    damage = tcod.random_get_int(None, 2, 4)
    radius = 1
    m_range = tcod.random_get_int(None, 9, 12)

    item_com = com_Item(use_function=cast_fireball, value=(damage, radius, m_range), pickup_text="Fireball Scroll")

    return_object = obj_Actor(x, y, "fireball scroll", animation_key="S_SCROLL_02", item=item_com)

    return return_object


def gen_scroll_confusion(coords):
    x, y = coords

    effect_length = tcod.random_get_int(None, 5, 10)

    item_com = com_Item(use_function=cast_confusion, value=effect_length, pickup_text="Scroll of Confusion")

    return_object = obj_Actor(x, y, "Konfuzius scroll", animation_key="S_SCROLL_03", item=item_com)

    return return_object


def gen_weapon_sword(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = com_Equipment(attack_bonus=bonus, equip_text="Sword")

    return_object = obj_Actor(x, y, "sword", animation_key="S_SWORD", equipment=equipment_com)

    return return_object


def gen_armor_shield(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = com_Equipment(defense_bonus=bonus, equip_text="Shield")

    return_object = obj_Actor(x, y, "shield", animation_key="S_SHIELD", equipment=equipment_com)

    return return_object


## ENEMYS ##

def gen_enemy(coords):
    random_number = tcod.random_get_int(None, 0, 100)

    if random_number <= 15:
        new_enemy = gen_snake_anaconda(coords)

    elif random_number <= 50:
        new_enemy = gen_mouse(coords)

    else:
        new_enemy = gen_snake_cobra(coords)

    GAME.current_objects.append(new_enemy)


def gen_snake_anaconda(coords):
    x, y = coords

    max_health = tcod.random_get_int(None, 15, 20)
    base_attack = tcod.random_get_int(None, 3, 6)

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = com_Creature(creature_name, death_function=death_snake, hp=max_health, base_atk=base_attack)
    ai_com = ai_Chase()

    snake = obj_Actor(x, y, "Anaconda", animation_key="A_SNAKE_01", creature=creature_com, ai=ai_com, )

    return snake


def gen_snake_cobra(coords):
    x, y = coords

    max_health = tcod.random_get_int(None, 5, 10)
    base_attack = tcod.random_get_int(None, 1, 3)

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = com_Creature(creature_name, death_function=death_snake, hp=max_health, base_atk=base_attack)
    ai_com = ai_Chase()

    snake = obj_Actor(x, y, "Cobra", animation_key="A_SNAKE_02", creature=creature_com, ai=ai_com, )

    return snake


def gen_mouse(coords):
    x, y = coords

    max_health = 1
    base_attack = 0

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = com_Creature(creature_name, death_function=death_mouse, hp=max_health, base_atk=base_attack)
    ai_com = ai_Flee()

    item_com = com_Item(use_function=cast_heal, value=2)

    mouse = obj_Actor(x, y, "Mouse", animation_key="A_MOUSE_01", creature=creature_com, ai=ai_com, item=item_com)

    return mouse


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
            game_exit()

        elif player_action != "no-action":
            for obj in GAME.current_objects:
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

        # update the display
        pygame.display.flip()

        CLOCK.tick(constants.GAME_FPS)


def game_initialize():
    """Das hier startet Pygame und das Hauptfenster"""

    global SURFACE_MAIN, SURFACE_MAP, PLAYER, ENEMY, FOV_CALCULATE, CLOCK, ASSETS, CAMERA, RANDOM_ENGINE
    # makes window start at top left corner
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "30,30"
    # disable scaling of windows
    ctypes.windll.user32.SetProcessDPIAware()

    # initialize Pygame
    pygame.init()
    pygame.display.set_caption("Roguelike")

    pygame.key.set_repeat(200,70)

    tcod.namegen_parse("data/namegen/jice_celtic.cfg")

    # looks for resolution of the display of the user
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

    SURFACE_MAP = pygame.Surface(
        (constants.MAP_WIDTH * constants.CELL_WIDTH, constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    CAMERA = obj_Camera()

    ASSETS = struc_Assets()

    CLOCK = pygame.time.Clock()

    # Random Engine
    RANDOM_ENGINE = random.SystemRandom()

    FOV_CALCULATE = True

    # game_new()


def game_handle_keys():
    global FOV_CALCULATE

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
                cast_confusion(caster=PLAYER, effect_length=2)

            if event.key == pygame.K_m:
                cast_lightning(caster=PLAYER, T_damage_maxrange=5)

            if event.key == pygame.K_x:
                debug_tile_select()

            if event.key == pygame.K_s:
                GAME.transition_next()

            if event.key == pygame.K_b:
                game_save(display_message=True)
                game_load()

            if MOD_KEY and event.key == pygame.K_PERIOD:
                list_of_objs = map_objects_at_coords(PLAYER.x, PLAYER.y)
                for obj in list_of_objs:
                    if obj.stairs:
                        obj.stairs.use()

    return "no-action"


def game_message(game_msg, msg_color=constants.COLOR_GREY):
    GAME.message_history.append((game_msg, msg_color))


def game_new():
    global GAME, PLAYER

    PLAYER = gen_player((0, 0))
    # starts a nre game and map
    GAME = obj_Game()
    GAME.current_objects.append(PLAYER)

    map_place_objects(GAME.current_rooms)


def game_exit():
    game_save()

    # quit the game
    pygame.quit()
    exit()


def game_save(display_message=False):
    if display_message:
        game_message("Saved Game", constants.COLOR_WHITE)

    for obj in GAME.current_objects:
        obj.animation_destroy()

    with gzip.open("data/savegame", "wb") as file:
        pickle.dump([GAME, PLAYER], file)


def game_load():
    global GAME, PLAYER, FOV_CALCULATE

    with gzip.open("data/savegame", "rb") as file:
        GAME, PLAYER = pickle.load(file)

    for obj in GAME.current_objects:
        obj.animation_init()

    map_make_fov(GAME.current_map)
    FOV_CALCULATE = True
    map_calculate_fov()


def game_start():
    try:
        game_load()
    except:
        game_new()

    game_main_loop()


if __name__ == '__main__':
    menu_main()

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
