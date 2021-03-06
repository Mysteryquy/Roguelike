from src import config
from src.components.health import Health, HealEvent
from src.components.name import Name
from src.components.position import Position


def cast_heal(caster: int, target=0, amount=0):
    name, health = config.GAME.current_level.world.components_for_entity(caster, Name, Health)
    target_name = " themself"
    if target != caster:
        target_name = config.GAME.current_level.world.component_for_entity(target, Name)
    config.GAME.current_level.world.add_component(target, HealEvent(amount=amount))
    config.GAME.game_message(name.name + " heals " + target_name + " for " + str(amount))


def cast_lightning(caster: int, damage: int, max_range: int, coords=None):
    pos = config.GAME.current_level.world.component_for_entity(caster, Position)

    # prompt player for a tile
    if not coords:
        point_selected = menu.menu_tile_select(coords_origin=(pos.x, pos.y), max_range=max_range, penetrate_walls=False)
    else:
        point_selected = coords

    if point_selected:
        list_of_tiles = game_map.find_line(player_location, point_selected)

        for i, (x, y) in enumerate(list_of_tiles):

            target = game_map.check_for_creature(x, y)

            if target:
                target.creature.take_damage(damage, caster.creature)


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
            creature_to_damage.creature.take_damage(damage, caster)

            if creature_to_damage is not config.PLAYER:
                creature_hit = True

    if creature_hit:
        config.GAME.game_message(
            "The fire rages and evaporates all flesh it came in contact with. Its nearly as hot as Alina Paul",
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
    new_room_number = tcod.random_get_int(None, 0, len(config.GAME.current_rooms) - 1)
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
        config.GAME.game_message("The spell fizzels and fails! You stay where you were.",
                                 msg_color=constants.COLOR_BLUE_LIGHT)


def cast_raisedead(caster, value):
    actors_to_check = game_map.objects_at_coords(coords_x=caster.x, coords_y=caster.y)
    print(actors_to_check)
    corpse = None
    for actor in actors_to_check:
        if actor.is_corpse:
            corpse = actor
            break

    if corpse:
        new_creature_coords = game_map.search_empty_tile(caster.x, caster.y, 2, 2, exclude_origin=True)
        if new_creature_coords:
            new_creature = monster_gen.gen_undead_ghost(new_creature_coords, 10)
            level.objects.append(new_creature)
            corpse.delete()
            config.GAME.game_message("YoU rAiSeD a SpOokY gHoSt!", msg_color=constants.COLOR_GREEN_DARK)
        else:
            config.GAME.game_message("The spell failed!", msg_color=constants.COLOR_GREEN_DARK)
    else:
        config.GAME.game_message("The spell failed!", msg_color=constants.COLOR_GREEN_DARK)


def cast_buffstats(caster, value):
    spell_duration = value
    setter_value = math.trunc(caster.creature.intelligence / 2)
    buff = StatusEffect(caster, spell_duration,
                        effect_dict={Status.STRENGTH: setter_value, Status.INTELLIGENCE: setter_value,
                                     Status.DEXTERITY: setter_value})
    caster.add_effect(buff)

    # TODO Create countdown
    # TODO Fix stat drawing
    # TODO Fix unupdating stats
    # TODO Add current HP while buffing it
