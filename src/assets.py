import pygame
from bidict import bidict

from src import config, constants


def colorize(image, new_color, flags=pygame.BLEND_RGBA_SUB):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param flags:
    :param image: Surface to create a colorized copy of
    :param new_color: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()
    # add in new RGB values
    image.fill(new_color[0:3] + (0,), None, flags)
    return image


tile_names = bidict({
    "S_WALL": 0,
    "S_FLOOR": 1,
    "W_WALL": 2,
    "W_FLOOR": 3,
    "H_WALL": 4,
    "H_FLOOR": 5,
})


# noinspection PyArgumentEqualDefault
class Assets:

    def __init__(self):
        # FONTS#
        self.FONT_DEBUG_MESSAGE = pygame.font.Font("data/joystix.ttf", 20)
        self.FONT_MESSAGE_TEXT = pygame.font.Font("data/joystix.ttf", 20)
        self.FONT_CURSOR_TEXT = pygame.font.Font("data/joystix.ttf", constants.CELL_HEIGHT)
        self.FONT_FANTY = pygame.font.Font("data/fanty.ttf", int(round(constants.CELL_HEIGHT / 2)))
        self.FONT_MAG1 = pygame.font.Font("data/mag1.ttf", constants.CELL_HEIGHT)
        self.FONT_MAG2 = pygame.font.Font("data/mag2.ttf", constants.CELL_HEIGHT)
        self.FONT_RED1 = pygame.font.Font("data/red1.ttf", int(constants.CELL_HEIGHT * 1.5))
        self.FONT_RED2 = pygame.font.Font("data/red2.ttf", constants.CELL_HEIGHT)

        self.MAIN_MENU_BACKGROUND = pygame.image.load("data/sprites/mm.png")
        self.MAIN_MENU_BACKGROUND = pygame.transform.scale(self.MAIN_MENU_BACKGROUND,
                                                           (constants.RECT_WHOLE_SCREEN.width,
                                                            constants.RECT_WHOLE_SCREEN.height))
        self.HEALTH_BAR_BORDER = get_image_from_file("data/tilesets/GUI/CUTGUI0.png", 16, 112, 48, 48)

        self.tile_dict = {
            tile_names["S_WALL"]: pygame.image.load("data/sprites/wall2.jpg").convert_alpha(),
            tile_names["S_FLOOR"]: pygame.image.load("data/sprites/floor.jpg").convert_alpha(),

        }
        t1 = (0, 50, 90, 0)
        t2 = (100, 60, 60, 0)
        t3 = (90, 0, 0, 0)
        t4 = (0, 0, 0, 0)

        self.tile_dict[tile_names["W_WALL"]] = colorize(colorize(self.tile_dict[tile_names["S_WALL"]],
                                                     t1, flags=pygame.BLEND_RGBA_ADD), t2)
        self.tile_dict[tile_names["W_FLOOR"]] = colorize(colorize(self.tile_dict[tile_names["S_FLOOR"]],
                                                      t1, flags=pygame.BLEND_RGBA_ADD), t2)

        self.tile_dict[tile_names["H_WALL"]] = colorize(colorize(self.tile_dict[tile_names["S_WALL"]],
                                                                 t3, flags=pygame.BLEND_RGBA_ADD), t4)
        self.tile_dict[tile_names["H_FLOOR"]] = colorize(colorize(self.tile_dict[tile_names["S_FLOOR"]],
                                                                 t3, flags=pygame.BLEND_RGBA_ADD), t4)

        self.tile_dict_explored = {key: colorize(self.tile_dict[key], (50, 50, 50, 0)) for key in self.tile_dict}

        self.MINIMAP_YELLOW_RECT = get_surface_rect(constants.MINI_MAP_CELL_WIDTH, constants.MINI_MAP_CELL_HEIGHT,
                                                    constants.COLOR_YELLOW)
        self.MINIMAP_GOLD_RECT = get_surface_rect(constants.MINI_MAP_CELL_WIDTH, constants.MINI_MAP_CELL_HEIGHT,
                                                  constants.COLOR_YELLOW_DARK_GOLD)
        self.MINIMAP_RED_RECT = get_surface_rect(constants.MINI_MAP_CELL_WIDTH, constants.MINI_MAP_CELL_HEIGHT,
                                                 constants.COLOR_RED_DARK)
        self.MINIMAP_WHITE_RECT = get_surface_rect(constants.MINI_MAP_CELL_WIDTH, constants.MINI_MAP_CELL_HEIGHT,
                                                   constants.COLOR_WHITE)
        self.MAP_DARK_GREY_RECT = get_surface_rect(constants.CELL_WIDTH, constants.CELL_HEIGHT,
                                                   constants.COLOR_DARK_GREY)

        self.animation_dict = {
            "A_PLAYER": get_animation_from_files(1, 7, "data/tilesets/Characters/Player", num_sprites=2),
            "A_DEMON_PILLUS": get_animation_from_files(0, 0, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_BUFFLA": get_animation_from_files(1, 0, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_AVIN": get_animation_from_files(2, 0, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_GRONK": get_animation_from_files(3, 0, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_SLOOSH": get_animation_from_files(4, 0, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_KOLAK": get_animation_from_files(5, 0, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_ABSODUX": get_animation_from_files(6, 0, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_NERGAL": get_animation_from_files(7, 0, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_BOOMI": get_animation_from_files(0, 1, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_FLABSY": get_animation_from_files(2, 1, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_HULK": get_animation_from_files(3, 1, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_HULK_ICE": get_animation_from_files(6, 1, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_HUMAN": get_animation_from_files(2, 2, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_HUMAN_2": get_animation_from_files(3, 2, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_TWINHEAD": get_animation_from_files(4, 2, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_CUTU": get_animation_from_files(5, 2, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_BALROG": get_animation_from_files(6, 2, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_QUASIT_ICE": get_animation_from_files(0, 3, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_QUASIT_WATER": get_animation_from_files(1, 3, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_QUASIT_FIRE": get_animation_from_files(2, 3, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_GREMLIN": get_animation_from_files(0, 4, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_GREMLIN_HORNED": get_animation_from_files(2, 4, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_BUNNY_DIAMOND": get_animation_from_files(0, 5, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_BUNNY_GOLD": get_animation_from_files(1, 5, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_SIREN": get_animation_from_files(0, 6, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_AMORED": get_animation_from_files(0, 7, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_ELDER": get_animation_from_files(0, 8, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_DEMON_HYPNOTOAD": get_animation_from_files(1, 8, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_SNAKE_ANACONDA": get_animation_from_files(2, 4, "data/tilesets/Characters/Reptile", num_sprites=2),
            "A_DEMON_LOL": get_animation_from_files(2, 4, "data/tilesets/Characters/Demon", num_sprites=2),
            "A_SNAKE_COBRA": get_animation_from_files(5, 4, "data/tilesets/Characters/Reptile", num_sprites=2),
            "A_RODENT_MOUSE": get_animation_from_files(0, 1, "data/tilesets/Characters/Rodent", num_sprites=2),
            "A_CAT_CAT": get_animation_from_files(0, 0, "data/tilesets/Characters/Cat", num_sprites=2),
            "A_CAT_LEOPARD": get_animation_from_files(1, 0, "data/tilesets/Characters/Cat", num_sprites=2),
            "A_CAT_PANTHER": get_animation_from_files(2, 0, "data/tilesets/Characters/Cat", num_sprites=2),
            "A_CAT_TIGER": get_animation_from_files(3, 0, "data/tilesets/Characters/Cat", num_sprites=2),
            "A_CAT_LION": get_animation_from_files(4, 0, "data/tilesets/Characters/Cat", num_sprites=2),
            "A_CAT_MOUNTAIN": get_animation_from_files(2, 1, "data/tilesets/Characters/Cat", num_sprites=2),
            "A_CAT_SNOW": get_animation_from_files(2, 2, "data/tilesets/Characters/Cat", num_sprites=2),
            "A_CAT_SHADOW": get_animation_from_files(2, 3, "data/tilesets/Characters/Cat", num_sprites=2),
            "A_CAT_WALKING": get_animation_from_files(1, 4, "data/tilesets/Characters/Cat", num_sprites=2),
            "A_SLIME_SMALL": get_animation_from_files(0, 4, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_SMALL_BLUE": get_animation_from_files(1, 4, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_ICE": get_animation_from_files(0, 3, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_ICE_FIRE": get_animation_from_files(1, 3, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_FIRE": get_animation_from_files(2, 3, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_ABOMINATION": get_animation_from_files(0, 2, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_BLOB": get_animation_from_files(1, 2, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_CUBE": get_animation_from_files(2, 2, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_RING": get_animation_from_files(0, 1, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_SNATCHER": get_animation_from_files(1, 1, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_SACK": get_animation_from_files(2, 1, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_MOLD_YELLOW": get_animation_from_files(2, 0, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_MOLD_GREEN": get_animation_from_files(3, 0, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_MOLD_BROWN": get_animation_from_files(1, 0, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_MOLD_RED": get_animation_from_files(4, 0, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_MOLD_BLUE": get_animation_from_files(0, 0, "data/tilesets/Characters/Slime", num_sprites=2),
            "A_SLIME_MOLD_PURPLE": get_animation_from_files(5, 0, "data/tilesets/Characters/Slime", num_sprites=2),
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
            "A_ELEMENTAL_ICE": get_animation_from_files(4, 3, "data/tilesets/Characters/Elemental", num_sprites=2),
            "A_ELEMENTAL_ICICLE": get_animation_from_files(2, 6, "data/tilesets/Characters/Elemental", num_sprites=2),
            "A_ELEMENTAL_EARTH": get_animation_from_files(3, 3, "data/tilesets/Characters/Elemental", num_sprites=2),
            "A_ELEMENTAL_STEEL": get_animation_from_files(3, 1, "data/tilesets/Characters/Elemental", num_sprites=2),
            "A_ELEMENTAL_LIGHTNING": get_animation_from_files(1, 3, "data/tilesets/Characters/Elemental",
                                                              num_sprites=2),
            "A_ELEMENTAL_PAPER": get_animation_from_files(1, 0, "data/tilesets/Characters/Elemental", num_sprites=2),
            "A_ELEMENTAL_SLIME": get_animation_from_files(2, 0, "data/tilesets/Characters/Elemental", num_sprites=2),
            "A_ELEMENTAL_FLESH": get_animation_from_files(7, 0, "data/tilesets/Characters/Elemental", num_sprites=2),
            "A_ELEMENTAL_MIMIC": get_animation_from_files(0, 8, "data/tilesets/Characters/Elemental", num_sprites=1),
            "A_BOSS_BEHOLDER": get_animation_from_files(2, 5, "data/tilesets/Characters/Elemental", num_sprites=2),
            "A_AQUATIC_PIRANHA": get_animation_from_files(4, 0, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_JELLYFISH": get_animation_from_files(6, 0, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_JELLYOWAR": get_animation_from_files(7, 0, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_SHARK": get_animation_from_files(0, 1, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_SHARK_WHITE": get_animation_from_files(1, 1, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_SHARK_GOLD": get_animation_from_files(2, 1, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_WHALE": get_animation_from_files(4, 1, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_WATERSNAKE": get_animation_from_files(0, 2, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_EEL": get_animation_from_files(2, 2, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_KEPLIE": get_animation_from_files(0, 3, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_SEA_DEVIL": get_animation_from_files(1, 4, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_AQUATIC_FROG_HYPNO": get_animation_from_files(1, 5, "data/tilesets/Characters/Aquatic", num_sprites=2),
            "A_BOSS_AQUATIC_KRAKEN": get_animation_from_files(0, 4, "data/tilesets/Characters/Aquatic", num_sprites=2),

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
            "S_DEAD_ICE": get_animation_from_files(1, 4, "data/tilesets/Characters/Elemental", num_sprites=1),
            "S_DEAD_FIRE": get_animation_from_files(2, 4, "data/tilesets/Characters/Elemental", num_sprites=1),
            "S_DEAD_EARTH": get_animation_from_files(0, 4, "data/tilesets/Characters/Elemental", num_sprites=1),
            "S_FLESH_SPIDER": get_animation_from_files(2, 1, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_FLESH_WORM": get_animation_from_files(2, 3, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_FLESH_NORMAL": get_animation_from_files(0, 0, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_FLESH_DOG": get_animation_from_files(7, 0, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_FLESH_SNAIL": get_animation_from_files(2, 3, "data/tilesets/Items/Flesh", num_sprites=1),
            "S_DEAD_DEMON": get_animation_from_files(4, 13, "data/tilesets/Objects/Decor", num_sprites=1),
            "S_FLESH_FISH": get_animation_from_files(2, 4, "data/tilesets/Items/Flesh", num_sprites=1),

            "S_STAIRS_DOWN": get_animation_from_files(3, 1, "data/tilesets/Objects/Tile", num_sprites=1),
            "S_STAIRS_UP": get_animation_from_files(2, 1, "data/tilesets/Objects/Tile", num_sprites=1),
            "S_FLESH_EAT": get_animation_from_files(3, 0, "data/tilesets/Items/Flesh", num_sprites=1),
            "DECOR_STATUE_01": get_animation_from_files(0, 0, "bubble_mult", num_sprites=1, opacity=50),

        }

        self.animation_dict_explored = {key: [colorize(img, (70, 70, 70, 0)) for img in self.animation_dict[key]]
                                        for key in self.animation_dict}

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
                             scale=(constants.CELL_WIDTH, constants.CELL_HEIGHT),
                             opacity=None):
    image_list = []

    for i in range(num_sprites):
        # Create blank image
        image = pygame.Surface([width, height], pygame.SRCALPHA).convert()

        sprite_sheet = pygame.image.load(file_prefix + str(i) + ".png")

        image.blit(sprite_sheet, (0, 0), (column * width, row * height, width, height))
        if opacity:
            image.convert_alpha()
            # image.set_colorkey(constants.COLOR_WHITE)
        else:
            image.convert()
            image.set_colorkey(constants.COLOR_BLACK)
        # set transparency to black

        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))

        image_list.append(image)

    return image_list


def get_surface_rect(width, height, color):
    surf = pygame.Surface([width, height]).convert()
    pygame.draw.rect(surf, color, surf.get_rect())
    return surf
