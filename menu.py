import pygame

import config
import constants
import game_map
import render
import ui


class MainMenu:
    def __init__(self, game_exit, game_load, game_new, game_main_loop, preferences_save):
        self.game_new = game_new
        self.game_load = game_load
        self.game_exit = game_exit
        self.game_main_loop = game_main_loop
        self.preferences_save = preferences_save

        self.menu_running = True

        self.title_y = constants.CAMERA_HEIGHT / 2 - 40
        self.title_x = constants.CAMERA_WIDTH / 2
        self.title_text = "Deine Mama Game.exe"

        # Button Adresses
        continue_game_button_y = self.title_y + 60
        new_game_button_y = continue_game_button_y + 60
        options_button_y = new_game_button_y + 60
        quit_button_y = options_button_y + 60

        continue_game_button = ui.Button(config.SURFACE_MAIN, "Continue", (200, 45), "button_continue",
                                         (self.title_x, continue_game_button_y), callback=self.continue_button_callback)

        new_game_button = ui.Button(config.SURFACE_MAIN, "New Game", (200, 45), "button_new_game",
                                    (self.title_x, new_game_button_y), callback=self.newgame_button_callback)

        options_button = ui.Button(config.SURFACE_MAIN, "Options", (200, 45), "button_options",
                                   (self.title_x, options_button_y), callback=self.options_button_callback)

        quit_button = ui.Button(config.SURFACE_MAIN, "QUIT GAME", (200, 45), "button_quit",
                                (self.title_x, quit_button_y), callback=self.quit_button_callback)

        self.button_container = ui.UiContainer(config.SURFACE_MAIN,
                                               constants.RECT_WHOLE_SCREEN,
                                               "menu_container",
                                               [continue_game_button, new_game_button, options_button, quit_button],
                                               color=constants.COLOR_BLUE_LIGHT,
                                               img=config.ASSETS.MAIN_MENU_BACKGROUND)

        # Slider vars #
        slider_x = constants.CAMERA_WIDTH / 2
        sound_effect_slider_y = constants.CAMERA_HEIGHT / 2 - 60
        sound_effect_vol = 0.5
        music_effect_slider_y = sound_effect_slider_y + 70

        self.sound_effect_slider = ui.Slider(config.SURFACE_MAIN, (125, 25), "sound_effect_slider",
                                             (slider_x, sound_effect_slider_y),
                                             constants.COLOR_RED,
                                             constants.COLOR_GREEN, config.PREFERENCES.vol_sound, "Sound Volume",
                                             callback=self.sound_volume_adjust_callback)

        self.music_effect_slider = ui.Slider(config.SURFACE_MAIN, (125, 25), "music_effect_slider",
                                             (slider_x, music_effect_slider_y),
                                             constants.COLOR_RED,
                                             constants.COLOR_GREEN, config.PREFERENCES.vol_music, "Music Volume",
                                             callback=self.music_volume_adjust_callback)

        self.effect_container = ui.UiContainer(config.SURFACE_MAIN,
                                               pygame.Rect(constants.CAMERA_WIDTH / 2 - 200,
                                                           constants.CAMERA_HEIGHT / 2 - 150,
                                                           400, 400),
                                               id="effect_container",
                                               elements=[self.sound_effect_slider, self.music_effect_slider],
                                               color=constants.COLOR_GREY)

    def show_menu(self):
        pygame.mixer.music.load(config.ASSETS.music_main_menu)
        pygame.mixer.music.play(-1)
        while self.menu_running:
            list_of_events = pygame.event.get()
            mouse_position = pygame.mouse.get_pos()

            game_input = (list_of_events, mouse_position)

            for event in list_of_events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.game_exit()

            self.button_container.react_multiple(game_input)

            self.button_container.draw()

            render.draw_text(config.SURFACE_MAIN, self.title_text, (self.title_x, self.title_y), constants.COLOR_RED,
                             center=True)

            pygame.display.update()

    def continue_button_callback(self, id):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(config.ASSETS.music_lvl_1)
        pygame.mixer.music.play(-1)
        # try to load game, start new if problems
        try:
            self.game_load()
            render.fill_surfaces()
        except Exception as e:
            print(e)

        self.game_main_loop()

    def newgame_button_callback(self, id):
        config.SURFACE_MAIN.blit(pygame.Surface((constants.CAMERA_HEIGHT * 2, constants.CAMERA_WIDTH * 2)),
                                 (0, 0))
        input_field = ui.Textfield(config.SURFACE_MAIN, pygame.Rect(constants.CAMERA_WIDTH / 4,
                                                                    constants.CAMERA_HEIGHT / 2, 500, 60),
                                   "name_input",
                                   constants.COLOR_GREY, constants.COLOR_WHITE,
                                   constants.COLOR_BLACK, auto_active=True,
                                   start_text="Please enter your name",
                                   focus_key=pygame.K_RETURN,
                                   font=config.ASSETS.FONT_RED1,
                                   callback=self.input_field_callback)

        input_container = ui.UiContainer(config.SURFACE_MAIN, constants.RECT_WHOLE_SCREEN, "input_container",
                                         [input_field], constants.COLOR_BLUE_LIGHT)

        while not input_container.update(pygame.event.get()):
            input_container.draw()
            config.CLOCK.tick(constants.GAME_FPS)
            pygame.display.update()

    def input_field_callback(self, id, text):
        player_name = text
        pygame.mixer.music.stop()
        pygame.mixer.music.load(config.ASSETS.music_lvl_1)
        pygame.mixer.music.play(-1)
        self.game_new(player_name)
        render.fill_surfaces()
        self.game_main_loop()

    def options_button_callback(self, id):
        self.menu_options()

    @staticmethod
    def quit_button_callback(id):
        pygame.quit()
        exit()

    def menu_options(self):
        menu_close = False
        while not menu_close:
            list_of_events = pygame.event.get()
            mouse_position = pygame.mouse.get_pos()

            game_input = (list_of_events, mouse_position)

            for event in list_of_events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.game_exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.preferences_save()
                        menu_close = True

            self.effect_container.update(game_input)
            self.effect_container.draw()
            pygame.display.update()

    @staticmethod
    def sound_volume_adjust_callback(id, current_val):
        current_sound_volume = config.PREFERENCES.vol_sound
        if current_sound_volume is not current_val:
            config.PREFERENCES.vol_sound = current_val
            config.ASSETS.volume_adjust()

    @staticmethod
    def music_volume_adjust_callback(id, current_val):
        current_music_volume = config.PREFERENCES.vol_music
        if current_music_volume is not current_val:
            config.PREFERENCES.vol_music = current_val
            config.ASSETS.volume_adjust()


def menu_pause():
    # This Menu pauses the game and displays a simple message in the center of THE MAP (not the screen [danke markus mit deinem vollbild kack :P])

    menu_close = False

    window_width = constants.CAMERA_WIDTH
    window_height = constants.CAMERA_HEIGHT

    menu_text = "PAUSED"
    menu_font = config.ASSETS.FONT_DEBUG_MESSAGE

    text_height = render.helper_text_height(menu_font)
    text_width = len(menu_text) * render.helper_text_width(menu_font)

    while not menu_close:

        events_list = pygame.event.get()

        for event in events_list:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    menu_close = True

        render.draw_text(config.SURFACE_MAIN, menu_text,
                         ((window_width / 2) - (text_width / 2), (window_height / 2) - (text_height / 2)),
                         constants.COLOR_BLACK, constants.COLOR_WHITE)

        config.CLOCK.tick(constants.GAME_FPS)

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
    menu_text_font = config.ASSETS.FONT_MESSAGE_TEXT

    # Helper var
    menu_text_height = render.helper_text_height(menu_text_font)

    local_inventory_surface = pygame.Surface((menu_width, menu_height))

    while not menu_close:

        # Clear the menu
        local_inventory_surface.fill(constants.COLOR_BLACK)

        # TODO Register Changes
        print_list = [obj.display_name for obj in config.PLAYER.container.inventory]
        print_list.insert(0, "Gold(" + str(config.PLAYER.container.gold) + ")")
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
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/audio/soundeffects/leather_inventory.wav"))
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse_in_window and mouse_line_selection <= len(print_list) - 1:
                        if mouse_line_selection > 0:
                            config.PLAYER.container.inventory[mouse_line_selection - 1].item.use()
                            menu_close = True

        ##Draw the list
        for line, (name) in enumerate(print_list):

            if int(line) == int(mouse_line_selection) and mouse_in_window:
                render.draw_text(local_inventory_surface, name, (0, 0 + (line * constants.INVENTORY_TEXT_HEIGHT)),
                                 constants.COLOR_WHITE, constants.COLOR_GREY)

            else:
                render.draw_text(local_inventory_surface, name, (0, 0 + (line * constants.INVENTORY_TEXT_HEIGHT)),
                                 constants.COLOR_WHITE)

        # Render Game
        render.draw_game()

        # Display Menu
        config.SURFACE_MAIN.blit(local_inventory_surface, (menu_x, menu_y))

        config.CLOCK.tick(constants.GAME_FPS)

        pygame.display.update()


def debug_tile_select():
    x, y = menu_tile_select()
    objects = game_map.objects_at_coords(x, y)
    config.GAME.game_message("Mouse position: " + str((x, y)))


def debug_tile_select_pathing():
    (x, y) = menu_tile_select()
    print("Path from" + str((config.PLAYER.x, config.PLAYER.y)) + " to " + str((x, y)) + " :" + str(
        game_map.get_path_from_player(x, y)))


def menu_tile_select(coords_origin=None, max_range=None, penetrate_walls=True, pierce_creature=False, radius=None):
    """
    """
    # This menu let the player select a tile.
    # It pauses the game and produces an on screen rectangle when the player presses the mb will return the map address

    menu_close = False

    previous = None
    previous_drawn = []

    while not menu_close:

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Get button clicks
        events_list = pygame.event.get()

        int_x, int_y = config.CAMERA.coords_from_position(mouse_x, mouse_y)

        valid_tiles = []

        if coords_origin:
            full_list_tiles = game_map.find_line(coords_origin, (int_x, int_y))
            for i, (x, y) in enumerate(full_list_tiles):

                valid_tiles.append((x, y))

                if not penetrate_walls and not game_map.is_walkable(x, y):
                    break

                if not pierce_creature and game_map.check_for_creature(x, y):
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
                    if previous:
                        for x, y in previous_drawn:
                            if config.GAME.current_map[x][y].was_drawn and not game_map.is_visible(x, y):
                                config.SURFACE_MAP.blit(
                                    config.ASSETS.tile_dict[config.GAME.current_map[x][y].texture_explored],
                                    (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                            else:
                                config.SURFACE_MAP.blit(config.ASSETS.MAP_DARK_GREY_RECT,
                                                        (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                    return valid_tiles[-1]

        render.draw_game()

        if previous:
            for x, y in previous_drawn:
                if x >= constants.MAP_WIDTH+1 or y >= constants.MAP_HEIGHT+1:
                    continue
                if config.GAME.current_map[x][y].was_drawn and not game_map.is_visible(x,y):
                    config.SURFACE_MAP.blit(config.ASSETS.tile_dict[config.GAME.current_map[x][y].texture_explored],
                                            (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    config.SURFACE_MAP.blit(config.ASSETS.MAP_DARK_GREY_RECT,
                                            (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

        previous = int_x, int_y
        previous_drawn = []

        # Draw Rectangle at mouse position on top of game, dont draw the last tile in grey
        for (tile_x, tile_y) in valid_tiles[:-1]:
            render.draw_tile_rect((tile_x, tile_y), constants.COLOR_GREY)
            if not game_map.is_visible(tile_x, tile_y):
                previous_drawn.append((tile_x, tile_y))
        last_tile_x, last_tile_y = valid_tiles[-1]
        render.draw_tile_rect((last_tile_x, last_tile_y), constants.COLOR_RED, mark="X")
        if not game_map.is_visible(last_tile_x, last_tile_y):
            previous_drawn.append((last_tile_x, last_tile_y))

        if radius:
            area_effect = game_map.find_radius(valid_tiles[-1], radius)

            for (tile_x, tile_y) in area_effect:
                render.draw_tile_rect((tile_x, tile_y))
                if not game_map.is_visible(tile_x, tile_y):
                    previous_drawn.append((tile_x, tile_y))
        config.SURFACE_MAIN.blit(config.SURFACE_MAP, (0, 0), config.CAMERA.rect)

        # update the display
        pygame.display.flip()

        # tick the CLOCK
        config.CLOCK.tick(constants.GAME_FPS)
