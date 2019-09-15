import menu
import config
import constants
import ai
import render
import map


def cast_heal(caster, value):
    if caster.creature.hp == caster.creature.maxhp:
        config.GAME.game_message("HP is allready full")
        return "canceled"

    else:
        config.GAME.game_message(caster.name_object + " healed for " + str(value) + " HP")
        caster.creature.heal(value)
        print(caster.creature.hp)

    return None


def cast_lightning(caster, T_damage_maxrange):
    damage, m_range = T_damage_maxrange

    player_location = (caster.x, caster.y)

    # prompt player for a tile
    point_selected = menu.menu_tile_select(coords_origin=player_location, max_range=m_range, penetrate_walls=False)

    if point_selected:
        list_of_tiles = map.find_line(player_location, point_selected)

        for i, (x, y) in enumerate(list_of_tiles):

            target = map.check_for_creature(x, y)

            if target:
                target.creature.take_damage(damage)


def cast_fireball(caster, T_damage_radius_range):
    # defs
    damage, local_radius, max_r = T_damage_radius_range

    player_location = (caster.x, caster.y)

    point_selected = menu.menu_tile_select(coords_origin=player_location, max_range=max_r, penetrate_walls=False,
                                      pierce_creature=False, radius=local_radius)

    # get sequence of tiles
    tiles_to_damage = map.find_radius(point_selected, local_radius)

    creature_hit = False

    # damage all creatures in tiles
    for (x, y) in tiles_to_damage:
        creature_to_damage = map.check_for_creature(x, y)

        if creature_to_damage:
            creature_to_damage.creature.take_damage(damage)

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
        target = map.check_for_creature(tile_x, tile_y)

        if target:
            # temporarily confuse monster
            old_ai = target.ai
            target.ai = ai.ai_Confuse(old_ai, num_turns=effect_length)
            target.ai.owner = target

            config.GAME.game_message("The creature is confused", constants.COLOR_GREEN)

