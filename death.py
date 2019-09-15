import config
import constants
import render
import os
import pygame
import datetime

def death_snake(monster):
    # On death, most monsters stop moving tho
    config.GAME.game_message(monster.creature.name_instance + " is slaughtered into ugly bits of flesh!", constants.COLOR_GREY)
    # print (monster.creature.name_instance + " is slaughtered into ugly bits of flesh!")
    monster.animation = config.ASSETS.S_FLESH_SNAKE
    monster.animation_key = "S_FLESH_SNAKE"
    monster.creature = None
    monster.ai = None
    monster.depth = constants.DEPTH_CORPSE
    creature.get_xp(PLAYER.creature)


def death_mouse(mouse):
    # On death, most monsters stop moving tho
    config.GAME.game_message(mouse.creature.name_instance + " is killed. Eat it to heal up a bit!", constants.COLOR_GREY)
    # print (monster.creature.name_instance + " is slaughtered into ugly bits of flesh!")
    mouse.animation = config.ASSETS.S_FLESH_EAT
    mouse.animation_key = "S_FLESH_EAT"
    mouse.creature = None
    mouse.ai = None


def death_player(player):
    player.state = "STATUS_DEAD"

    config.SURFACE_MAIN.fill(constants.COLOR_BLACK)

    screen_center = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

    render.draw_text(config.SURFACE_MAIN, "lol nibba u dead!", screen_center, constants.COLOR_WHITE, center=True)
    render.draw_text(config.SURFACE_MAIN, "Check the legacy file to know what beat yo ass up",
              (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2 + 100), constants.COLOR_WHITE, center=True)

    pygame.display.update()

    file_name = ("data/userdata/legacy_" + config.PLAYER.creature.name_instance + "." + datetime.date.today().strftime(
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



