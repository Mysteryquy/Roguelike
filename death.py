import config
import constants
import render
import os
import pygame
import datetime
import tcod
import monster_gen




def death_player(player, killer):
    player.state = "STATUS_DEAD"

    config.SURFACE_MAIN.fill(constants.COLOR_BLACK)

    screen_center = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

    render.draw_text(config.SURFACE_MAIN, "lol nibba u dead!", screen_center, constants.COLOR_WHITE, center=True)
    render.draw_text(config.SURFACE_MAIN, "Check the legacy file to know what beat yo ass up",
                     (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2 + 100), constants.COLOR_WHITE,
                     center=True)

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



def death_worm(monster, killer,):


    chance = tcod.random_get_int(None, 1, 3)
    if chance < 2:

        coords = monster.owner.x, monster.owner.y
        new_mob = monster_gen.gen_pest_worm(coords)
        config.GAME.current_objects.append(new_mob)
        config.GAME.game_message(monster.name_instance + " has halved and its other half came to life!", msg_color=constants.COLOR_RED)
    else:
        config.GAME.game_message(monster.name_instance + " is smashed to a bloody mess!", constants.COLOR_GREY)


def death_humanoid(monster, killer):


    config.GAME.game_message(monster.creature.name_instance + " is dead!",
                             constants.COLOR_GREY)

    monster.animation = config.ASSETS.S_FLESH_SPIDER # TODO: GIMME THAT FUCKING UPPER LEFT FLESH PICTURE PLS
    monster.animation_key = "S_FLESH_SPIDER" # TODO: GIMME THAT FUCKING UPPER LEFT FLESH PICTURE PLS
    killer.get_xp(monster.creature.xp_gained)
    monster.creature = None
    monster.ai = None
    monster.depth = constants.DEPTH_CORPSE