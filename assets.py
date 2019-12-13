import pygame

import config
import constants


class Assets:

    def __init__(self):
        # Sprite sheets#
        self.charspritesheet = Spritesheet("data/sprites/Reptiles.png")
        self.enemyspritesheet = Spritesheet("data/sprites/ROFL.png")
        self.scrollspritesheet = Spritesheet("data/sprites/Scroll.png")
        self.reptile = Spritesheet("data/sprites/Reptile0.png")
        self.flesh = Spritesheet("data/sprites/Flesh.png")
        self.tile = Spritesheet("data/sprites/Tile.png")
        self.rodent = Spritesheet("data/sprites/Rodent0.png")
        self.tool = Spritesheet("data/sprites/Tool.png")
        self.doors = Spritesheet("data/sprites/Door0.png")
        self.demon1 = Spritesheet("data/sprites/Demon1.png")
        self.ground0 = Spritesheet("data/sprites/Ground0.png")

        # FONTS#
        self.FONT_DEBUG_MESSAGE = pygame.font.Font("data/joystix.ttf", 20)
        self.FONT_MESSAGE_TEXT = pygame.font.Font("data/joystix.ttf", 20)
        self.FONT_CURSOR_TEXT = pygame.font.Font("data/joystix.ttf", constants.CELL_HEIGHT)
        self.FONT_FANTY = pygame.font.Font("data/fanty.ttf", int(round(constants.CELL_HEIGHT / 2)))
        self.FONT_MAG1 = pygame.font.Font("data/mag1.ttf", constants.CELL_HEIGHT)
        self.FONT_MAG2 = pygame.font.Font("data/mag2.ttf", constants.CELL_HEIGHT)
        self.FONT_RED1 = pygame.font.Font("data/red1.ttf", int(constants.CELL_HEIGHT * 1.5))
        self.FONT_RED2 = pygame.font.Font("data/red2.ttf", constants.CELL_HEIGHT)

        ## ITEMS ##

        ## SPECIAL ##

        self.S_STAIRS_DOWN = self.tile.get_image("c", 1, 16, 16, (32, 32))
        self.S_STAIRS_UP = self.tile.get_image("b", 1, 16, 16, (32, 32))
        self.MAIN_MENU_BACKGROUND = pygame.image.load("data/sprites/mm.png")
        self.MAIN_MENU_BACKGROUND = pygame.transform.scale(self.MAIN_MENU_BACKGROUND,
                                                           (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
        self.S_END_GAME_ITEM = self.tool.get_image("a", 0, 16, 16, (32, 32))
        self.S_END_GAME_PORTAL_CLOSED = self.doors.get_image("d", 5, 16, 16, (32, 32))
        self.S_END_GAME_PORTAL_OPENED = self.doors.get_image("e", 5, 16, 16, (32, 32))

        self.HEALTH_BAR_BORDER = get_image_from_file("data/tilesets/GUI/CUTGUI0.png", 16, 112, 48, 48)

        self.tile_dict = {
            "S_WALL": pygame.image.load("data/sprites/wall2.jpg").convert_alpha(),
            "S_WALL_EXPLORED": pygame.image.load("data/sprites/wallunseen2.png").convert_alpha(),
            "S_FLOOR": pygame.image.load("data/sprites/floor.jpg").convert_alpha(),
            "S_FLOOR_EXPLORED": pygame.image.load("data/sprites/floorunseen2.png").convert_alpha()

        }

        self.MINIMAP_YELLOW_RECT = get_surface_rect(constants.MINI_MAP_CELL_WIDTH, constants.MINI_MAP_CELL_HEIGHT,
                                                         constants.COLOR_YELLOW)
        self.MINIMAP_GOLD_RECT = get_surface_rect(constants.MINI_MAP_CELL_WIDTH, constants.MINI_MAP_CELL_HEIGHT,
                                                  constants.COLOR_YELLOW_DARK_GOLD)
        self.MINIMAP_RED_RECT = get_surface_rect(constants.MINI_MAP_CELL_WIDTH, constants.MINI_MAP_CELL_HEIGHT,
                                                  constants.COLOR_RED_DARK)
        self.MINIMAP_WHITE_RECT = get_surface_rect(constants.MINI_MAP_CELL_WIDTH, constants.MINI_MAP_CELL_HEIGHT,
                                                  constants.COLOR_WHITE)

        self.animation_dict = {
            "A_PLAYER": get_animation_from_files(1, 7, "data/tilesets/Characters/Player", num_sprites=2),
            "A_SNAKE_ANACONDA": get_animation_from_files(2, 4, "data/tilesets/Characters/Reptile", num_sprites=2),
            "A_SNAKE_COBRA": get_animation_from_files(5, 4, "data/tilesets/Characters/Reptile", num_sprites=2),
            "A_RODENT_MOUSE": get_animation_from_files(0, 1, "data/tilesets/Characters/Rodent", num_sprites=2),
            "A_SLIME_SMALL": get_animation_from_files(0, 4, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_DOG_DOG": get_animation_from_files(0, 3, "data/tilesets/Characters/Dog", num_sprites=2),
            "A_SNAIL": get_animation_from_files(1, 7, "data/tilesets/Characters/Pest", num_sprites=2),
            "A_PEST_SMALL_SPIDER": get_animation_from_files(1, 2, "data/tilesets/Characters/Pest", num_sprites=2),
            "A_PEST_SMALL_SCORPION": get_animation_from_files(4, 2, "data/tilesets/Characters/Pest", num_sprites=2),
            "A_PEST_WORM": get_animation_from_files(0, 3, "data/tilesets/Characters/Pest", num_sprites=2),
            "A_HUMANOID_GOBLIN": get_animation_from_files(0, 8, "data/tilesets/Characters/Humanoid", num_sprites=2),
            "A_MISC_MONKEY": get_animation_from_files(0, 3, "data/tilesets/Characters/Misc", num_sprites=2),
            "A_UNDEAD_GHOST": get_animation_from_files(2, 4, "data/tilesets/Characters/Undead", num_sprites=2),
            "A_ELEMENTAL_POTATO": get_animation_from_files(0, 1, "data/tilesets/Characters/Elemental", num_sprites=2),
            "A_ELEMENTAL_FIRE": get_animation_from_files(2, 3, "data/tilesets/Characters/Elemental", num_sprites=2),


            ## ITEMS ##
            "S_SWORD": [pygame.transform.scale(pygame.image.load("data/sprites/sword.png"),
                                               (constants.CELL_WIDTH, constants.CELL_HEIGHT))],
            "S_SHIELD": [pygame.transform.scale(pygame.image.load("data/sprites/shield.png"),
                                                (constants.CELL_WIDTH, constants.CELL_HEIGHT))],
            "S_WEP_LONGSWORD_1": get_animation_from_files(0, 0, "data/tilesets/Items/MedWep", num_sprites=1),
            "S_WEP_LONGSWORD_2": get_animation_from_files(1, 0, "data/tilesets/Items/MedWep", num_sprites=1),
            "S_WEP_LONGSWORD_3": get_animation_from_files(2, 0, "data/tilesets/Items/MedWep", num_sprites=1),
            "S_WEP_LONGSWORD_4": get_animation_from_files(3, 0, "data/tilesets/Items/MedWep", num_sprites=1),
            "S_WEP_LONGSWORD_5": get_animation_from_files(4, 0, "data/tilesets/Items/MedWep", num_sprites=1),
            "S_WEP_LONGAXE_1": get_animation_from_files(0, 0, "data/tilesets/Items/MedWep", num_sprites=1),
            "S_WEP_LONGAXE_2": get_animation_from_files(0, 1, "data/tilesets/Items/MedWep", num_sprites=1),
            "S_ARM_SHIELD_1": get_animation_from_files(0, 0, "data/tilesets/Items/Shield", num_sprites=1),
            "S_ARM_SHIELD_2": get_animation_from_files(1, 0, "data/tilesets/Items/Shield", num_sprites=1),
            "S_ARM_SHIELD_3": get_animation_from_files(2, 0, "data/tilesets/Items/Shield", num_sprites=1),
            "S_ARM_SHIELD_4": get_animation_from_files(3, 0, "data/tilesets/Items/Shield", num_sprites=1),
            "S_ARM_SHIELD_5": get_animation_from_files(4, 0, "data/tilesets/Items/Shield", num_sprites=1),
            "S_ARM_SHIELD_6": get_animation_from_files(5, 0, "data/tilesets/Items/Shield", num_sprites=1),
            "S_ARM_SHIELD_7": get_animation_from_files(6, 0, "data/tilesets/Items/Shield", num_sprites=1),
            "S_SCROLL_01": get_animation_from_files(0, 0, "data/tilesets/Items/Scroll", num_sprites=1),
            "S_SCROLL_02": get_animation_from_files(0, 1, "data/tilesets/Items/Scroll", num_sprites=1),
            "S_SCROLL_03": get_animation_from_files(0, 2, "data/tilesets/Items/Scroll", num_sprites=1),
            "S_SCROLL_04": get_animation_from_files(0, 3, "data/tilesets/Items/Scroll", num_sprites=1),
            "S_POTION_01": get_animation_from_files(0, 0, "data/tilesets/Items/Potion", num_sprites=1),
            "S_MONEY_SMALL": get_animation_from_files(2, 1, "data/tilesets/Items/Money", num_sprites=1),
            "S_MONEY_MEDIUM": get_animation_from_files(1, 1, "data/tilesets/Items/Money", num_sprites=1),
            "S_MONEY_LARGE": get_animation_from_files(0, 1, "data/tilesets/Items/Money", num_sprites=1),
            "S_FLESH_SNAKE": get_animation_from_files(1, 3, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_DEAD_SLIME": get_animation_from_files(2, 5, "data/tilesets/Objects/Ground", num_sprites=1),
            "S_FLESH_SPIDER": get_animation_from_files(2, 1, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_FLESH_WORM": get_animation_from_files(2, 3, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_FLESH_NORMAL": get_animation_from_files(0, 0, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_FLESH_DOG": get_animation_from_files(7, 0, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_FLESH_SNAIL": get_animation_from_files(2, 3, "data/tilesets/Items/Flesh", num_sprites=1),

            "S_STAIRS_DOWN": self.S_STAIRS_DOWN,
            "S_STAIRS_UP": self.S_STAIRS_UP,
            "S_FLESH_EAT": self.flesh.get_image("c", 0, 16, 16, (32, 32)),
            "S_END_GAME_ITEM": self.S_END_GAME_ITEM,
            "S_END_GAME_PORTAL_OPENED": self.S_END_GAME_PORTAL_OPENED,
            "S_END_GAME_PORTAL_CLOSED": self.S_END_GAME_PORTAL_CLOSED

        }

        ## AUDIO ##

        self.snd_list = []

        self.music_death = "data/audio/death_music.mp3"
        self.music_main_menu = "data/audio/Broke.mp3"
        self.music_lvl_1 = "data/audio/level_1.mp3"
        self.snd_hit_1 = self.sound_add("data/audio/hit_hurt1.wav")
        self.snd_hit_2 = self.sound_add("data/audio/hit_hurt2.wav")
        self.snd_hit_3 = self.sound_add("data/audio/hit_hurt3.wav")

        self.snd_list_hit = [self.snd_hit_1, self.snd_hit_2, self.snd_hit_3]

        self.volume_adjust()

    def sound_add(self, file_address):
        new_sound = pygame.mixer.Sound(file_address)

        self.snd_list.append(new_sound)

        return new_sound

    def volume_adjust(self):
        for sound in self.snd_list:
            sound.set_volume(config.PREFERENCES.vol_sound)

        pygame.mixer.music.set_volume(config.PREFERENCES.vol_music)


def get_image_from_file(file, x, y, width, height):
    image = pygame.Surface([width, height]).convert()
    sprite_sheet = pygame.image.load(file)
    image.blit(sprite_sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(constants.COLOR_BLACK)
    return image


def get_animation_from_files(column, row, file_prefix,
                             width=constants.SPRITE_WIDTH, height=constants.SPRITE_HEIGHT, num_sprites=2,
                             scale=(constants.CELL_WIDTH, constants.CELL_HEIGHT)):
    image_list = []

    for i in range(num_sprites):
        # Create blank image
        image = pygame.Surface([width, height]).convert()

        sprite_sheet = pygame.image.load(file_prefix + str(i) + ".png")

        image.blit(sprite_sheet, (0, 0), (column * width, row * height, width, height))

        # set transparency to black
        image.set_colorkey(constants.COLOR_BLACK)

        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))

        image_list.append(image)

    return image_list


class Spritesheet:  # Bilder von Spritesheets holen

    tiledict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11,
                "l": 12, "m": 13, "n": 14, "o": 15, "p": 16, "z": 0}

    def __init__(self, file_name):
        # Den Sheet laden.
        self.sprite_sheet = pygame.image.load(file_name).convert()

        ###############

    def get_image(self, column, row, width=constants.CELL_WIDTH, height=constants.CELL_HEIGHT, scale=None):

        image_list = []

        image = pygame.Surface([width, height]).convert_alpha()

        image.blit(self.sprite_sheet, (0, 0), (Spritesheet.tiledict[column] * width, row * height, width, height))

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
                       (Spritesheet.tiledict[column] * width + (width * i), row * height, width, height))

            # set transparency to black
            image.set_colorkey(constants.COLOR_BLACK)

            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))

            image_list.append(image)

        return image_list


def get_surface_rect(width, height, color):
    surf = pygame.Surface([width, height]).convert()
    pygame.draw.rect(surf, color, surf.get_rect())
    return surf
