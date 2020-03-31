import datetime
import os

import pygame

from src import config, constants, render_helper


def death_player():

    config.SURFACE_MAIN.fill(constants.COLOR_BLACK)

    screen_center = (constants.RECT_WHOLE_SCREEN.width / 2, constants.RECT_WHOLE_SCREEN.height / 2)

    render_helper.draw_text(config.SURFACE_MAIN, "lol nibba u dead!", screen_center, constants.COLOR_WHITE, center=True)
    render_helper.draw_text(config.SURFACE_MAIN, "Check the legacy file to know what beat yo ass up",
                     (constants.RECT_WHOLE_SCREEN.width / 2, constants.RECT_WHOLE_SCREEN.height / 2 + 100),
                     constants.COLOR_WHITE,
                     center=True)

    pygame.display.update()

    file_name = (
                "data/userdata/legacy_" + "." + datetime.date.today().strftime(
            "%Y%B%d") + ".txt")

    file_exists = os.path.isfile(file_name)
    save_exists = os.path.isfile("data/userdata/savegame")

    if file_exists: os.remove(file_name)
    if save_exists: os.remove("data/userdata/savegame")

    legacy_file = open(file_name, "a+")

    for message, color in config.GAME.message_history:
        legacy_file.write(message + "\n")

    pygame.mixer.music.load(config.ASSETS.music_death)
    pygame.mixer.music.play()

    pygame.time.wait(12000)
    config.MAIN_MENU.show_menu()