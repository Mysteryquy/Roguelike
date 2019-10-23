import ai
import config
import constants
import game_map
import menu
import tcod
import pygame
import render


def cast_heal(caster, value):
    if caster.creature.hp == caster.creature.maxhp:
        config.GAME.game_message("HP is allready full")
        return "canceled"

    else:
        config.GAME.game_message(caster.name_object + " healed for " + str(value) + " HP")
        caster.creature.heal(value)
        print(caster.creature.hp)

    return None


def cast_lightning(caster, T_damage_maxrange, coords=None):
    damage, m_range = T_damage_maxrange

    player_location = (caster.x, caster.y)

    # prompt player for a tile
    if not coords:
        point_selected = menu.menu_tile_select(coords_origin=player_location, max_range=m_range, penetrate_walls=False)
    else:
        point_selected = coords

    if point_selected:
        list_of_tiles = game_map.find_line(player_location, point_selected)

        for i, (x, y) in enumerate(list_of_tiles):

            target = game_map.check_for_creature(x, y)

            if target:
                target.creature.take_damage(damage,caster.creature)


def cast_fireball(caster, T_damage_radius_range):
    # defs
    damage, local_radius, max_r = T_damage_radius_range

    player_location = (caster.x, caster.y)

    point_selected = menu.menu_tile_select(coords_origin=player_location, max_range=max_r, penetrate_walls=False,
                                      pierce_creature=False, radius=local_radius)

    # get sequence of tiles
    tiles_to_damage = game_map.find_radius(point_selected, local_radius)

    creature_hit = False

    # damage all creatures in tiles
    for (x, y) in tiles_to_damage:
        creature_to_damage = game_map.check_for_creature(x, y)

        if creature_to_damage:
            creature_to_damage.creature.take_damage(damage,caster)

            if creature_to_damage is not config.PLAYER:
                creature_hit = True

    if creature_hit:
        config.GAME.game_message("The fire rages and evaporates all flesh it came in contact with. Its nearly as hot as Alina Paul",
                     constants.COLOR_RED)


def cast_confusion(caster, effect_length):
    # select tile
    point_selected = menu.menu_tile_select()

    # get target
    if point_selected:
        (tile_x, tile_y) = point_selected
        target = game_map.check_for_creature(tile_x, tile_y)

        if target:
            # temporarily confuse monster
            old_ai = target.ai
            target.ai = ai.AiConfuse(old_ai, num_turns=effect_length)
            target.ai.owner = target

            config.GAME.game_message("The creature is confused", constants.COLOR_GREEN)


def cast_teleportation(caster, value):

    # generate the target destination
    new_room_number = tcod.random_get_int(None, 0, len(config.GAME.current_rooms) -1)
    new_room = config.GAME.current_rooms[new_room_number]
    new_x = tcod.random_get_int(None, new_room.left + 1, new_room.right - 1)
    new_y = tcod.random_get_int(None, new_room.top + 1, new_room.bottom - 1)


    if not game_map.check_for_creature(new_x, new_y):
        # add in some cool effects
        config.GAME.game_message("You teleported to a different location!", msg_color=constants.COLOR_BLUE_LIGHT)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/audio/teleport.wav"))
        # actually teleport the player
        caster.x, caster.y = new_x, new_y
        config.FOV_CALCULATE = True

    else:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/audio/teleport_fail.wav"))
        config.GAME.game_message("The spell fizzels and fails! You stay where you were.", msg_color=constants.COLOR_BLUE_LIGHT)


def cast_raisedead(caster, value):
    actors_to_check = game_map.objects_at_coords(coords_x= caster.x, coords_y=caster.y)
    print(actors_to_check)
    for actor in actors_to_check:
        print(actor.is_corpse)
        if actor.is_corpse:


