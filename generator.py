# coding=utf-8
import tcod

import casting
import config
import constants
import death
import monster_gen
from actor import Actor
from container import Container
from creature import Creature
from equipment import Equipment
from item import Item, Gold
from structure import ExitPortal, Stairs, Structure
import random
import numpy.random


##PLAYER##
def gen_player(coords, player_name="Player"):
    x, y = coords
    container_com = Container()
    creature_com = Creature(player_name, base_atk=666, base_def=1, custom_death=death.death_player, base_evasion=20,
                            base_hit_chance=100, alignment=Creature.CreatureAlignment.PLAYER, strength=10,
                            dexterity=7, intelligence=5)
    player = Actor(x, y, "python", animation_key="A_PLAYER", animation_speed=0.5, creature=creature_com,
                   container=container_com)

    return player


##STRUCTURES##
def gen_stairs(level, coords, downwards=True):
    x, y = coords
    if downwards:
        stairs_com = Stairs(constants.LevelNames.next_level_name(level.name), downwards=downwards)
    else:
        stairs_com = Stairs(constants.LevelNames.previous_level_name(level.name), downwards=downwards)

    animation_key = "S_STAIRS_DOWN" if downwards else "S_STAIRS_UP"
    stairs = Actor(x, y, "stairs", animation_key=animation_key, depth=constants.DEPTH_STRUCTURES,
                   structure=stairs_com, draw_explored=True)

    level.objects.append(stairs)
    print("dddd")
    level.stairs.append(stairs)


def gen_portal(level, coords):
    x, y = coords

    port_com = ExitPortal()
    portal = Actor(x, y, "exit portal", animation_key="S_END_GAME_PORTAL_CLOSED", depth=constants.DEPTH_STRUCTURES,
                   structure=port_com, draw_explored=True)

    level.objects.append(portal)


def gen_end_game_item(level, coords):
    x, y, = coords

    item_com = Item(pickup_text=constants.END_GAME_ITEM_NAME)

    return_object = Actor(x, y, constants.END_GAME_ITEM_NAME, animation_key="S_END_GAME_ITEM",
                          depth=constants.DEPTH_ITEM, item=item_com)

    level.objects.append(return_object)


def gen_and_append_item(level, coords):
    random_number = tcod.random_get_int(None, 1, 3)

    if random_number == 1:
        new_item = gen_weapon(level, coords)
    elif random_number == 2:
        new_item = gen_scroll(level, coords)
    else:
        new_item = gen_armor_shield(level, coords)
    print(new_item.name_object)
    level.objects.append(new_item)


def gen_scroll_lighning(level, coords):
    x, y = coords

    damage = tcod.random_get_int(None, 5, 7)
    m_range = tcod.random_get_int(None, 5, 7)

    item_com = Item(use_function=casting.cast_lightning, value=(damage, m_range), pickup_text="Lightning Scroll")

    return_object = Actor(x, y, "lightning scroll", animation_key="S_SCROLL_01", depth=constants.DEPTH_ITEM,
                          item=item_com)

    return return_object


def gen_scroll_fireball(level, coords):
    x, y = coords

    damage = tcod.random_get_int(None, 2, 4)
    radius = 1
    m_range = tcod.random_get_int(None, 9, 12)

    item_com = Item(use_function=casting.cast_fireball, value=(damage, radius, m_range), pickup_text="Fireball Scroll")

    return_object = Actor(x, y, "fireball scroll", animation_key="S_SCROLL_02", depth=constants.DEPTH_ITEM,
                          item=item_com)

    return return_object


def gen_scroll_confusion(level, coords):
    x, y = coords

    effect_length = tcod.random_get_int(None, 5, 10)

    item_com = Item(use_function=casting.cast_confusion, value=effect_length, pickup_text="Scroll of Confusion")

    return_object = Actor(x, y, "Konfuzius scroll", animation_key="S_SCROLL_03", depth=constants.DEPTH_ITEM,
                          item=item_com)

    return return_object


def gen_scroll_teleportation(level, coords):
    x, y = coords

    item_com = Item(use_function=casting.cast_teleportation, pickup_text="Scroll of Teleportation")

    return_object = Actor(x, y, "Tele-Scroll", animation_key="S_SCROLL_04", depth=constants.DEPTH_ITEM,
                          item=item_com)

    return return_object


def gen_potion_buffstats(level, coords):
    x, y = coords

    item_com = Item(use_function=casting.cast_buffstats, pickup_text="Potion of Statpower")

    return_object = Actor(x, y, "Potion of Statpower", animation_key="S_POTION_01", depth=constants.DEPTH_ITEM,
                          item=item_com)

    return return_object


def gen_weapon_sword(level, coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="Sword", value=100, pickup_text="Sword")

    return_object = Actor(x, y, "sword", animation_key="S_SWORD", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


longsword_name_dict = {
    1: "Silver Longsword",
    2: "Moonlight Sword",
    3: "Rediron Sword",
    4: "Black Sword",
    5: "Royal Sword"
}


def gen_weapon_longsword(level, coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)
    n = tcod.random_get_int(None, 1, len(longsword_name_dict))
    name = longsword_name_dict[n]

    equipment_com = Equipment(attack_bonus=bonus, equip_text=name, value=100, pickup_text=name)

    return_object = Actor(x, y, name, animation_key="S_WEP_LONGSWORD_" + str(n), depth=constants.DEPTH_ITEM,
                          equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_weapon_longaxe_1(level, coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="2 Handed Axe Type 1", value=100,
                              pickup_text="2 Handed Axe Type 1")

    return_object = Actor(x, y, "2 Handed Axe Type 1", animation_key="S_WEP_LONGAXE_1", depth=constants.DEPTH_ITEM,
                          equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_weapon_longaxe_2(level, coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="2 Handed Axe Type 2", value=100,
                              pickup_text="2 Handed Axe Type 2")

    return_object = Actor(x, y, "2 Handed Axe Type 2", animation_key="S_WEP_LONGAXE_2", depth=constants.DEPTH_ITEM,
                          equipment=equipment_com,
                          item=equipment_com)

    return return_object


shield_name_dict = {
    1: "Shield of Thorns",
    2: "Rediron Shield",
    3: "Mithril Shield",
    4: "Wooden Shield",
    5: "Silver Shield",
    6: "Shield of the Wolves",
    7: "Slimey Shield"

}


def gen_armor_shield(level, coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)
    n = random.choice(list(shield_name_dict))
    random_name = shield_name_dict[n]

    equipment_com = Equipment(defense_bonus=bonus, equip_text=random_name, value=100,
                              pickup_text=random_name)

    return_object = Actor(x, y, random_name, animation_key="S_ARM_SHIELD_" + str(n), depth=constants.DEPTH_ITEM,
                          equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_and_append_gold(level, coords):
    x, y = coords

    value = tcod.random_get_int(None, 1, 100)

    pic = "Default"

    if value < 31:
        pic = "S_MONEY_SMALL"
    elif value < 67:
        pic = "S_MONEY_MEDIUM"
    else:
        pic = "S_MONEY_LARGE"

    return_object = Actor(x, y, "Gold", animation_key=pic, depth=constants.DEPTH_ITEM,
                          item=Gold(value))

    level.objects.append(return_object)


def what_to_gen(level, coords):
    # Change to 3 to see buggy gold
    RNG = tcod.random_get_int(None, 1, 3)
    x, y = coords

    if RNG == 1:
        gen_and_append_enemy(level, (x, y))
    elif RNG == 2:
        gen_and_append_item(level, (x, y))
    elif RNG == 3:
        gen_and_append_gold(level, (x, y))
    # More stuff to come!


gen_monster_dict = {
    0: monster_gen.gen_reptile_anaconda,
    1: monster_gen.gen_rodent_mouse,
    2: monster_gen.gen_pest_worm,
    3: monster_gen.gen_dog_dog,
    4: monster_gen.gen_reptile_cobra,
    5: monster_gen.gen_pest_snail,
    6: monster_gen.gen_slime_small,
    7: monster_gen.gen_humanoid_goblin,
    8: monster_gen.gen_elemental_potato,
    9: monster_gen.gen_pest_small_spider,
    10: monster_gen.gen_elemental_fire,
    11: monster_gen.gen_elemental_ice,
    12: monster_gen.gen_elemental_earth,
    13: monster_gen.gen_elemental_lightning,
    14: monster_gen.gen_boss_beholder,
}

level_monster_dict = {
    "DUNGEON1": [(monster_gen.gen_slime_small,100)],
    "DUNGEON2": [(monster_gen.gen_boss_beholder, 777), (monster_gen.gen_rodent_mouse, 3)],
    "DUNGEON3": [(monster_gen.gen_cat_cat, 1)]
}


def gen_and_append_enemy(level, coords):
    monsters_and_weight = level_monster_dict[level.name]
    monsters = [monster for monster, _ in monsters_and_weight]  # anaconda,mouse,potato
    sum_weights = sum([weight for _, weight in monsters_and_weight])
    probabilities = [weight / sum_weights for _, weight in monsters_and_weight]  # 100/880, 3/880, 777/880
    monster_function = numpy.random.choice(monsters, 1, p=probabilities)[0]
    new_enemy = monster_function(level, coords)

    level.objects.append(new_enemy)


gen_weapon_dict = {
    0: gen_weapon_longsword,
    1: gen_weapon_sword,
    2: gen_weapon_longaxe_1,
    3: gen_weapon_longaxe_2,
}


def gen_weapon(level, coords):
    random_number = tcod.random_get_int(None, 0, 200)

    gen_function = random.choice(gen_weapon_dict)

    new_item = gen_function(level, coords)

    return new_item


gen_scroll_dict = {
    0: gen_scroll_fireball,
    1: gen_scroll_confusion,
    2: gen_scroll_lighning,
    3: gen_scroll_teleportation,
    4: gen_potion_buffstats
}


def gen_scroll(level, coords):
    random_number = tcod.random_get_int(None, 0, 200)

    gen_function = random.choice(gen_scroll_dict)

    new_item = gen_function(level, coords)

    return new_item
