import datetime
import os

import pygame
import tcod

import config
import constants
import monster_gen
import render
import menu
import game_map


def death_player(player, killer):
    player.state = "STATUS_DEAD"

    config.SURFACE_MAIN.fill(constants.COLOR_BLACK)

    screen_center = (constants.RECT_WHOLE_SCREEN.width / 2, constants.RECT_WHOLE_SCREEN.height / 2)

    render.draw_text(config.SURFACE_MAIN, "lol nibba u dead!", screen_center, constants.COLOR_WHITE, center=True)
    render.draw_text(config.SURFACE_MAIN, "Check the legacy file to know what beat yo ass up",
                     (constants.RECT_WHOLE_SCREEN.width / 2, constants.RECT_WHOLE_SCREEN.height / 2 + 100), constants.COLOR_WHITE,
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
    config.MAIN_MENU.show_menu()




def death_worm(monster, killer,):


    chance = tcod.random_get_int(None, 1, 3)
    if chance < 2:

        x, y = monster.owner.x, monster.owner.y
        new_coords = game_map.search_empty_tile(x, y, 2, 2, exclude_origin=True)
        if new_coords:
            new_mob = monster_gen.gen_pest_worm(new_coords, monster.name_instance)
            config.GAME.current_objects.append(new_mob)
            config.GAME.game_message(monster.name_instance + " has halved and its other half came to life!", msg_color=constants.COLOR_RED)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/audio/soundeffects/bite-small.wav"))
    else:
        config.GAME.game_message(monster.name_instance + " is smashed to a bloody mess!", constants.COLOR_GREY)

def death_ice_elemental(monster, killer,):


    chance = tcod.random_get_int(None, 1, 3)
    if chance < 1:

        x, y = monster.owner.x, monster.owner.y
        new_coords = game_map.search_empty_tile(x, y, 2, 2, exclude_origin=True)
        if new_coords:
            new_mob = monster_gen.gen_elemental_icicle(new_coords, monster.name_instance)
            config.GAME.current_objects.append(new_mob)
            config.GAME.game_message(monster.name_instance + " was smashed but small pieces still remain!", msg_color=constants.COLOR_RED)
    else:
        config.GAME.game_message(monster.name_instance + " is smashed to a icey mess!", constants.COLOR_GREY)


def death_gold_elemental(monster, killer):
    x, y = monster.owner.x, monster.owner.y
    new_coords = game_map.search_empty_tile(x, y, 2, 2, exclude_origin=True)
    if new_coords:
        new_mob = generator.gen_and_append_gold(new_coords)
        config.GAME.current_objects.append(new_mob)
        config.GAME.game_message(monster.name_instance + " was smashed but small pieces still remain!",
                                 msg_color=constants.COLOR_RED)
    else:
        config.GAME.game_message(monster.name_instance + " is smashed to a icey mess!", constants.COLOR_GREY)


def death_demon_boomi(monster, killer):
    #x, y = monster.owner.x, monster.owner.y

    #damage, local_radius, max_r = 8, 2, 2
    local_radius = 2

    player_location = (monster.owner.x, monster.owner.y)

    #point_selected = menu.menu_tile_select(coords_origin=player_location, max_range=max_r, penetrate_walls=False,
                                           #pierce_creature=False, radius=local_radius)

    # get sequence of tiles
    tiles_to_damage = game_map.find_radius((monster.owner.x, monster.owner.y),  local_radius)

    creature_hit = False

    # damage all creatures in tiles
    for (x, y) in tiles_to_damage:
        creature_to_damage = game_map.check_for_creature(x, y)

        if creature_to_damage:
            creature_to_damage.creature.take_damage(10, monster)

            if creature_to_damage: # is not config.PLAYER:
                creature_hit = True

    if creature_hit:
        config.GAME.game_message(
            "The Boomi explodes and splashes hot liquid on you!",
            constants.COLOR_RED)

    else:
        config.GAME.game_message(monster.name_instance + " explodes, but you doge the fiery parts!", constants.COLOR_RED)
