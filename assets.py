import pygame
import constants
import config


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


        # ANIMATIONS#
        #self.A_PLAYER = self.demon1.get_animation("d", 1, 16, 16, 2, (32, 32))
        self.A_PLAYER = get_animation_from_files(1,3,"TILESETS/Characters/Elemental",num_sprites=2)
        self.A_ENEMY = self.enemyspritesheet.get_animation("k", 1, 16, 16, 2, (32, 32))
        self.A_SNAKE_01 = self.reptile.get_animation("d", 4, 16, 16, 2, (32, 32))
        self.A_SNAKE_02 = self.reptile.get_animation("a", 4, 16, 16, 2, (32, 32))
        self.A_MOUSE_01 = self.rodent.get_animation("a", 1, 16, 16, 2, (32, 32))



        # SPRITES#
        self.S_WALL = pygame.image.load("data/sprites/wall2.jpg")
        self.S_WALLEXPLORED = pygame.image.load("data/sprites/wallunseen2.png")

        self.S_FLOOR = pygame.image.load("data/sprites/floor.jpg")
        self.S_FLOOREXPLORED = pygame.image.load("data/sprites/floorunseen2.png")

        # FONTS#
        self.FONT_DEBUG_MESSAGE = pygame.font.Font("data/joystix.ttf", 20)
        self.FONT_MESSAGE_TEXT = pygame.font.Font("data/joystix.ttf", 20)
        self.FONT_CURSOR_TEXT = pygame.font.Font("data/joystix.ttf", constants.CELL_HEIGHT)

        ## ITEMS ##
        self.S_SWORD = [
            pygame.transform.scale(pygame.image.load("data/sprites/sword.png"),
                                   (constants.CELL_WIDTH, constants.CELL_HEIGHT))]
        self.S_SHIELD = [
            pygame.transform.scale(pygame.image.load("data/sprites/shield.png"),
                                   (constants.CELL_WIDTH, constants.CELL_HEIGHT))]
        self.S_SCROLL_01 = self.scrollspritesheet.get_image("a", 5, 16, 16, (32, 32))
        self.S_SCROLL_02 = self.scrollspritesheet.get_image("a", 2, 16, 16, (32, 32))
        self.S_SCROLL_03 = self.scrollspritesheet.get_image("b", 2, 16, 16, (32, 32))
        self.S_FLESH_SNAKE = self.flesh.get_image("a", 3, 16, 16, (32, 32))
        self.S_FLESH_EAT = self.flesh.get_image("c", 0, 16, 16, (32, 32))
        self.S_DEAD_SLIME = self.ground0.get_image("c", 5, 16, 16, (32, 32))
        self.S_FLESH_SPIDER = self.flesh.get_image("a", 5, 16, 16, (32, 32))
        self.S_FLESH_WORM = self.flesh.get_image("d", 0, 16, 16, (32, 32))

        ## SPECIAL ##

        self.S_STAIRS_DOWN = self.tile.get_image("a", 1, 16, 16, (32, 32))
        self.S_STAIRS_UP = self.tile.get_image("b", 1, 16, 16, (32, 32))
        self.MAIN_MENU_BACKGROUND = pygame.image.load("data/sprites/mm.png")
        self.MAIN_MENU_BACKGROUND = pygame.transform.scale(self.MAIN_MENU_BACKGROUND,
                                                           (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
        self.S_END_GAME_ITEM = self.tool.get_image("a", 0, 16, 16, (32, 32))
        self.S_END_GAME_PORTAL_CLOSED = self.doors.get_image("d", 5, 16, 16, (32, 32))
        self.S_END_GAME_PORTAL_OPENED = self.doors.get_image("e", 5, 16, 16, (32, 32))

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
            "S_DEAD_SLIME" : self.S_DEAD_SLIME,
            "S_FLESH_SPIDER" : self.S_FLESH_SPIDER,
            "S_FLESH_WORM" : self.S_FLESH_WORM,

            "S_STAIRS_DOWN": self.S_STAIRS_DOWN,
            "S_STAIRS_UP": self.S_STAIRS_UP,
            "S_FLESH_EAT": self.S_FLESH_EAT,
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


def get_animation_from_files(column, row, file_prefix,
                             width=constants.SPRITE_WIDTH, height = constants.SPRITE_HEIGHT, num_sprites=2,
                             scale=(constants.CELL_WIDTH,constants.CELL_HEIGHT)):

    image_list = []

    for i in range(num_sprites):
        # Create blank image
        image = pygame.Surface([width, height]).convert()

        sprite_sheet = pygame.image.load(file_prefix + str(i) + ".png")

        image.blit(sprite_sheet, (0,0), (column*width, row*height, width, height))

        # set transparency to black
        image.set_colorkey(constants.COLOR_BLACK)

        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))

        image_list.append(image)

    return image_list




class Spritesheet:  # Bilder von Spritesheets holen

    tiledict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11,
                "l": 12, "m": 13, "n": 14, "o": 15, "p": 16}

    def __init__(self, file_name):
        # Den Sheet laden.
        self.sprite_sheet = pygame.image.load(file_name).convert()

        ###############



    def get_image(self, column, row, width=constants.CELL_WIDTH, height=constants.CELL_HEIGHT, scale=None):

        image_list = []

        image = pygame.Surface([width, height]).convert()

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


