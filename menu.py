import constants
import ui
import config
import pygame
import render
import generator
import map


def menu_main(game_initialize,game_exit,game_load,game_new,game_main_loop,preferences_save):
    game_initialize()

    menu_running = True

    title_y = constants.CAMERA_HEIGHT / 2 - 40
    title_x = constants.CAMERA_WIDTH / 2
    title_text = "Untitled (but very cool) Game "

    # Button Adresses
    continue_game_button_y = title_y + 60
    new_game_button_y = continue_game_button_y + 60
    options_button_y = new_game_button_y + 60
    quit_button_y = options_button_y + 60

    continue_game_button = ui.Button(config.SURFACE_MAIN, "Continue", (200, 45), (title_x, continue_game_button_y))

    new_game_button = ui.Button(config.SURFACE_MAIN, "New Game", (200, 45), (title_x, new_game_button_y))

    options_button = ui.Button(config.SURFACE_MAIN, "Options", (200, 45), (title_x, options_button_y))

    quit_button = ui.Button(config.SURFACE_MAIN, "QUIT GAME", (200, 45), (title_x, quit_button_y))

    pygame.mixer.music.load(config.ASSETS.music_main_menu)
    pygame.mixer.music.play(-1)

    while menu_running:

        list_of_events = pygame.event.get()
        mouse_position = pygame.mouse.get_pos()

        game_input = (list_of_events, mouse_position)

        for event in list_of_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                game_exit()

        # Button updates
        if continue_game_button.update(game_input):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(config.ASSETS.music_lvl_1)
            pygame.mixer.music.play(-1)
            # try to load game, start new if problems
            try:
                game_load()
            except:
                game_new()

            game_main_loop()
            game_initialize()

        if new_game_button.update(game_input):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(config.ASSETS.music_lvl_1)
            pygame.mixer.music.play(-1)
            game_new()
            game_main_loop()
            game_initialize()

        if options_button.update(game_input):
            menu_main_options(game_exit,preferences_save)

        if quit_button.update(game_input):
            pygame.quit()
            exit()

        config.SURFACE_MAIN.blit(config.ASSETS.MAIN_MENU_BACKGROUND, (0, 0))

        render.draw_text(config.SURFACE_MAIN, title_text, (title_x, title_y), constants.COLOR_RED, center=True)

        continue_game_button.draw()
        new_game_button.draw()
        options_button.draw()
        quit_button.draw()

        pygame.display.update()


def menu_main_options(game_exit, preferences_save):
    # MENU VARS#
    settings_menu_width = 300
    settings_menu_height = 200
    settings_menu_background_color = constants.COLOR_GREY

    # Slider vars #
    slider_x = constants.CAMERA_WIDTH / 2
    sound_effect_slider_y = constants.CAMERA_HEIGHT / 2 - 60
    sound_effect_vol = 0.5
    music_effect_slider_y = sound_effect_slider_y + 70

    # TEXT vars #
    music_text_y = sound_effect_slider_y - 30
    sound_text_y = music_effect_slider_y - 30

    window_center = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

    settings_menu_surface = pygame.Surface((settings_menu_width, settings_menu_height))

    settings_menu_rect = pygame.Rect(0, 0, settings_menu_width, settings_menu_height)

    settings_menu_rect.center = window_center

    menu_close = False

    sound_effect_slider = ui.Slider(config.SURFACE_MAIN, (125, 25), (slider_x, sound_effect_slider_y),
                                    constants.COLOR_RED,
                                    constants.COLOR_GREEN, config.PREFERENCES.vol_sound)

    music_effect_slider = ui.Slider(config.SURFACE_MAIN, (125, 25), (slider_x, music_effect_slider_y),
                                    constants.COLOR_RED,
                                    constants.COLOR_GREEN, config.PREFERENCES.vol_music)

    while not menu_close:

        list_of_events = pygame.event.get()
        mouse_position = pygame.mouse.get_pos()

        game_input = (list_of_events, mouse_position)

        for event in list_of_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                game_exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    preferences_save()
                    menu_close = True

        current_sound_volume = config.PREFERENCES.vol_sound
        current_music_volume = config.PREFERENCES.vol_music

        if current_sound_volume is not sound_effect_slider.current_val:
            config.PREFERENCES.vol_sound = sound_effect_slider.current_val
            config.ASSETS.volume_adjust()

        if current_music_volume is not music_effect_slider.current_val:
            config.PREFERENCES.vol_music = music_effect_slider.current_val
            config.ASSETS.volume_adjust()

        sound_effect_slider.update(game_input)
        music_effect_slider.update(game_input)

        # Draw the menu
        settings_menu_surface.fill(settings_menu_background_color)
        config.SURFACE_MAIN.blit(settings_menu_surface, settings_menu_rect.topleft)
        render.draw_text(config.SURFACE_MAIN, "Music Volume", (slider_x, sound_text_y), constants.COLOR_BLACK,
                         center=True)
        render.draw_text(config.SURFACE_MAIN, "Sound Volume", (slider_x, music_text_y), constants.COLOR_BLACK,
                         center=True)
        sound_effect_slider.draw()
        music_effect_slider.draw()
        pygame.display.update()


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
                        config.PLAYER.container.inventory[mouse_line_selection].item.use()
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
    (x, y) = menu_tile_select()
    objects = map.objects_at_coords(x, y)
    print(str((x,y)) + str(config.FOV_MAP.walkable[y,x]))


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

        mapx_pixel, mapy_pixel = config.CAMERA.win_to_map((mouse_x, mouse_y))

        # Mouse map selection
        map_coord_x = mapx_pixel / constants.CELL_WIDTH
        map_coord_y = mapy_pixel / constants.CELL_HEIGHT

        # transform into integers
        int_x = int(map_coord_x)
        int_y = int(map_coord_y)

        valid_tiles = []

        if coords_origin:
            full_list_tiles = map.find_line(coords_origin, (int_x, int_y))
            for i, (x, y) in enumerate(full_list_tiles):

                valid_tiles.append((x, y))

                if not penetrate_walls and map.check_for_wall(x, y):
                    break

                if not pierce_creature and map.check_for_creature(x, y):
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
        config.SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
        config.SURFACE_MAP.fill(constants.COLOR_BLACK)

        config.CAMERA.update()

        # draw the map
        render.draw_map(config.GAME.current_map)

        for obj in config.GAME.current_objects:
            obj.draw()

        render.draw_tile_rect((int_x, int_y))  # Hier ?
        # Draw Rectangle at mouse position on top of game, dont draw the last tile in grey
        for (tile_x, tile_y) in valid_tiles[:-1]:
            render.draw_tile_rect((tile_x, tile_y), constants.COLOR_GREY)
        last_tile_x, last_tile_y = valid_tiles[-1]
        render.draw_tile_rect((last_tile_x, last_tile_y), constants.COLOR_RED, mark="X")

        if radius:
            area_effect = map.find_radius(valid_tiles[-1], radius)

            for (tile_x, tile_y) in area_effect:
                render.draw_tile_rect((tile_x, tile_y))

        config.SURFACE_MAIN.blit(config.SURFACE_MAP, (0, 0), config.CAMERA.rectangle)
        # print(CAMERA.rectangle)

        render.draw_debug()
        render.draw_messages()

        # update the display
        pygame.display.flip()

        # tick the CLOCK
        config.CLOCK.tick(constants.GAME_FPS)
