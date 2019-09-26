from container import Container
from actor import Actor
from creature import Creature
from main_game import ExitPortal, Stairs
import tcod
from item import Item
import config
import death
import casting
import ai
import constants
from equipment import Equipment
import monster_gen


##PLAYER##
def gen_player(coords, player_name="Player"):
    x, y = coords
    print(coords)

    container_com = Container()
    creature_com = Creature(player_name, base_atk=666, base_def=100, custom_death=death.death_player, base_evasion=20,
                            base_hit_chance=100)
    player = Actor(x, y, "python", animation_key="A_PLAYER", animation_speed=0.5, creature=creature_com,
                   container=container_com)

    return player


##STRUCTURES##
def gen_stairs(coords, downwards=True):
    x, y = coords
    if downwards:
        stairs_com = Stairs()
        stairs = Actor(x, y, "stairs", animation_key="S_STAIRS_DOWN", depth=constants.DEPTH_STRUCTURES,
                       stairs=stairs_com, draw_explored=True)
    else:
        stairs_com = Stairs(downwards)
        stairs = Actor(x, y, "stairs", animation_key="S_STAIRS_UP", depth=constants.DEPTH_STRUCTURES,
                       stairs=stairs_com, draw_explored=True)

    config.GAME.current_objects.append(stairs)


def gen_portal(coords):
    x, y = coords

    port_com = ExitPortal()
    portal = Actor(x, y, "exit portal", animation_key="S_END_GAME_PORTAL_CLOSED", depth=constants.DEPTH_STRUCTURES,
                   exitportal=port_com, draw_explored=True)

    config.GAME.current_objects.append(portal)


def gen_end_game_item(coords):
    x, y, = coords

    item_com = Item(pickup_text=constants.END_GAME_ITEM_NAME)

    return_object = Actor(x, y, constants.END_GAME_ITEM_NAME, animation_key="S_END_GAME_ITEM",
                          depth=constants.DEPTH_ITEM, item=item_com)

    config.GAME.current_objects.append(return_object)


##ITEMS##

def gen_item(coords):
    random_number = tcod.random_get_int(None, 1, 3)

    if random_number == 1:
        new_item = gen_weapon(coords)
    elif random_number == 2:
        new_item = gen_scroll(coords)
    else:
        new_item = gen_armor(coords)

    config.GAME.current_objects.append(new_item)




def gen_scroll_lighning(coords):
    x, y = coords

    damage = tcod.random_get_int(None, 5, 7)
    m_range = tcod.random_get_int(None, 5, 7)

    item_com = Item(use_function=casting.cast_lightning, value=(damage, m_range), pickup_text="Lightning Scroll")

    return_object = Actor(x, y, "lightning scroll", animation_key="S_SCROLL_01", depth=constants.DEPTH_ITEM,
                          item=item_com)

    return return_object


def gen_scroll_fireball(coords):
    x, y = coords

    damage = tcod.random_get_int(None, 2, 4)
    radius = 1
    m_range = tcod.random_get_int(None, 9, 12)

    item_com = Item(use_function=casting.cast_fireball, value=(damage, radius, m_range), pickup_text="Fireball Scroll")

    return_object = Actor(x, y, "fireball scroll", animation_key="S_SCROLL_02", depth=constants.DEPTH_ITEM,
                          item=item_com)

    return return_object


def gen_scroll_confusion(coords):
    x, y = coords

    effect_length = tcod.random_get_int(None, 5, 10)

    item_com = Item(use_function=casting.cast_confusion, value=effect_length, pickup_text="Scroll of Confusion")

    return_object = Actor(x, y, "Konfuzius scroll", animation_key="S_SCROLL_03", depth=constants.DEPTH_ITEM,
                          item=item_com)

    return return_object


def gen_weapon_sword(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="Sword", value=100, pickup_text="Sword")

    return_object = Actor(x, y, "sword", animation_key="S_SWORD", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_weapon_longsword_1(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="Longsword Type 1", value=100, pickup_text="Longsword Type 1")

    return_object = Actor(x, y, "Longsword Type 1", animation_key="S_WEP_LONGSWORD_1", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_weapon_longsword_2(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="Longsword Type 2", value=100, pickup_text="Longsword Type 2")

    return_object = Actor(x, y, "Longsword Type 2", animation_key="S_WEP_LONGSWORD_2", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_weapon_longsword_3(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="Longsword Type 3", value=100, pickup_text="Longsword Type 3")

    return_object = Actor(x, y, "Longsword Type 3", animation_key="S_WEP_LONGSWORD_3", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_weapon_longsword_4(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="Longsword Type 4", value=100, pickup_text="Longsword Type 4")

    return_object = Actor(x, y, "Longsword Type 4", animation_key="S_WEP_LONGSWORD_4", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_weapon_longsword_5(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="Longsword Type 5", value=100, pickup_text="Longsword Type 5")

    return_object = Actor(x, y, "Longsword Type 5", animation_key="S_WEP_LONGSWORD_5", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_weapon_longaxe_1(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="2 Handed Axe Type 1", value=100, pickup_text="2 Handed Axe Type 1")

    return_object = Actor(x, y, "2 Handed Axe Type 1", animation_key="S_WEP_LONGAXE_1", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_weapon_longaxe_2(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(attack_bonus=bonus, equip_text="2 Handed Axe Type 2", value=100, pickup_text="2 Handed Axe Type 2")

    return_object = Actor(x, y, "2 Handed Axe Type 2", animation_key="S_WEP_LONGAXE_2", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_armor_shield_1(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(defense_bonus=bonus, equip_text="Shield 1", value=100, pickup_text="Shield 1")

    return_object = Actor(x, y, "shield 1", animation_key="S_ARM_SHIELD_1", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_armor_shield_2(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(defense_bonus=bonus, equip_text="Shield 2", value=100, pickup_text="Shield 2")

    return_object = Actor(x, y, "shield 2", animation_key="S_ARM_SHIELD_2", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_armor_shield_3(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(defense_bonus=bonus, equip_text="Shield 3", value=100, pickup_text="Shield 3")

    return_object = Actor(x, y, "shield 3", animation_key="S_ARM_SHIELD_3", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_armor_shield_4(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(defense_bonus=bonus, equip_text="Shield 4", value=100, pickup_text="Shield 4")

    return_object = Actor(x, y, "shield 4", animation_key="S_ARM_SHIELD_4", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_armor_shield_5(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(defense_bonus=bonus, equip_text="Shield 5", value=100, pickup_text="Shield 5")

    return_object = Actor(x, y, "shield 5", animation_key="S_ARM_SHIELD_5", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_armor_shield_6(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(defense_bonus=bonus, equip_text="Shield 6", value=100, pickup_text="Shield 6")

    return_object = Actor(x, y, "shield 6", animation_key="S_ARM_SHIELD_6", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_armor_shield_7(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(defense_bonus=bonus, equip_text="Shield 7", value=100, pickup_text="Shield 7")

    return_object = Actor(x, y, "shield 7", animation_key="S_ARM_SHIELD_7", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def gen_gold(coords):

    x, y = coords

    value = tcod.random_get_int(None, 1, 100)

    equipment_com = Gold(value=value)

    return_object = Actor(x, y, "Gold", animation_key="S_MONEY_SMALL", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


def what_to_gen(coords):


    #Change to 3 to see buggy gold
    RNG = tcod.random_get_int(None, 1, 2)
    x,y = coords

    if RNG == 1:
        gen_enemy((x, y))
    elif RNG == 2:
        gen_item((x, y))
    elif RNG == 3:
        gen_gold((x,y))
    # More stuff to come!











gen_monster_dict = {
    0: monster_gen.gen_reptile_anaconda,
    1: monster_gen.gen_rodent_mouse,
    2: monster_gen.gen_pest_worm,
    3: monster_gen.gen_dog_dog,
    4: monster_gen.gen_reptile_cobra,
    5: monster_gen.gen_pest_snail,
    6: monster_gen.gen_slime_small,
}


def gen_enemy(coords):
    random_number = tcod.random_get_int(None, 0, 200)


    gen_function = gen_monster_dict[random_number % len(gen_monster_dict)]

    new_enemy = gen_function(coords)

    config.GAME.current_objects.append(new_enemy)


gen_weapon_dict = {
    0: gen_weapon_longsword_1,
    1: gen_weapon_longsword_2,
    2: gen_weapon_longsword_3,
    3: gen_weapon_longsword_4,
    4: gen_weapon_longsword_5,
    5: gen_weapon_sword,
    6: gen_weapon_longaxe_1,
    7: gen_weapon_longaxe_2,
}


def gen_weapon(coords):
    random_number = tcod.random_get_int(None, 0, 200)


    gen_function = gen_weapon_dict[random_number % len(gen_weapon_dict)]

    new_item = gen_function(coords)

    return new_item


gen_scroll_dict = {
    0: gen_scroll_fireball,
    1: gen_scroll_confusion,
    2: gen_scroll_lighning,
}


def gen_scroll(coords):
    random_number = tcod.random_get_int(None, 0, 200)


    gen_function = gen_scroll_dict[random_number % len(gen_scroll_dict)]

    new_item = gen_function(coords)

    return new_item


gen_armor_dict = {
    0: gen_armor_shield_1,
    1: gen_armor_shield_2,
    2: gen_armor_shield_3,
    3: gen_armor_shield_4,
    4: gen_armor_shield_5,
    5: gen_armor_shield_6,
    6: gen_armor_shield_7,
}


def gen_armor(coords):
    random_number = tcod.random_get_int(None, 0, 200)


    gen_function = gen_armor_dict[random_number % len(gen_armor_dict)]

    new_item = gen_function(coords)

    return new_item


