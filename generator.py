from container import Container
from actor import Actor
from creature import Creature
from main_game import ExitPortal,Stairs
import tcod
from item import Item
import config
import death
import casting
import ai
import constants
from equipment import Equipment


##PLAYER##
def gen_player(coords):
    x, y = coords
    print(coords)

    container_com = Container()
    creature_com = Creature("SPIELER", base_atk=666, base_def=100, death_function=death.death_player, base_evasion=20,
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
                       stairs=stairs_com)
    else:
        stairs_com = Stairs(downwards)
        stairs = Actor(x, y, "stairs", animation_key="S_STAIRS_UP", depth=constants.DEPTH_STRUCTURES, stairs=stairs_com)

    config.GAME.current_objects.append(stairs)


def gen_portal(coords):
    x, y = coords

    port_com = ExitPortal()
    portal = Actor(x, y, "exit portal", animation_key="S_END_GAME_PORTAL_CLOSED", depth=constants.DEPTH_STRUCTURES,
                   exitportal=port_com)

    config.GAME.current_objects.append(portal)


def gen_end_game_item(coords):
    x, y, = coords

    item_com = Item(pickup_text=constants.END_GAME_ITEM_NAME)

    return_object = Actor(x, y, constants.END_GAME_ITEM_NAME, animation_key="S_END_GAME_ITEM",
                          depth=constants.DEPTH_ITEM, item=item_com)

    config.GAME.current_objects.append(return_object)


##ITEMS##

def gen_item(coords):
    random_number = tcod.random_get_int(None, 1, 6)

    if random_number == 1:
        new_item = gen_scroll_confusion(coords)
    elif random_number == 2:
        new_item = gen_scroll_fireball(coords)
    elif random_number == 3:
        new_item = gen_scroll_confusion(coords)
    elif random_number == 4:
        new_item = gen_weapon_sword(coords)
    elif random_number == 5:
        new_item = gen_armor_shield(coords)
    else:
        new_item = gen_scroll_lighning(coords)

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


def gen_armor_shield(coords):
    x, y = coords

    bonus = tcod.random_get_int(None, 1, 2)

    equipment_com = Equipment(defense_bonus=bonus, equip_text="Shield", value=100, pickup_text="Shield")

    return_object = Actor(x, y, "shield", animation_key="S_SHIELD", depth=constants.DEPTH_ITEM, equipment=equipment_com,
                          item=equipment_com)

    return return_object


## ENEMYS ##

def gen_enemy(coords):
    random_number = tcod.random_get_int(None, 0, 100)

    if random_number <= 15:
        new_enemy = gen_snake_anaconda(coords)

    elif random_number <= 50:
        new_enemy = gen_mouse(coords)

    else:
        new_enemy = gen_snake_cobra(coords)

    config.GAME.current_objects.append(new_enemy)


def gen_snake_anaconda(coords):
    x, y = coords

    max_health = tcod.random_get_int(None, 15, 20)
    base_attack = tcod.random_get_int(None, 3, 6)

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, death_function=death.death_snake, hp=max_health, base_atk=base_attack,
                            base_hit_chance=40, base_evasion=0, xp_gained=300)
    ai_com = ai.AiChase()

    snake = Actor(x, y, "Anaconda", animation_key="A_SNAKE_01", depth=constants.DEPTH_CREATURE, creature=creature_com,
                  ai=ai_com)

    return snake


def gen_snake_cobra(coords):
    x, y = coords

    max_health = tcod.random_get_int(None, 5, 10)
    base_attack = tcod.random_get_int(None, 1, 3)

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, death_function=death.death_snake, hp=max_health, base_atk=base_attack,
                            base_hit_chance=80, base_evasion=10, xp_gained=300)
    ai_com = ai.AiChase()

    snake = Actor(x, y, "Cobra", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE, creature=creature_com,
                  ai=ai_com)

    return snake


def gen_mouse(coords):
    x, y = coords

    max_health = 1
    base_attack = 0

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, death_function=death.death_mouse, hp=max_health, base_atk=base_attack,
                            base_evasion=60)
    ai_com = ai.AiFlee()

    item_com = Item(use_function=casting.cast_heal, value=2, pickup_text="Rat Carcass")

    mouse = Actor(x, y, "Mouse", animation_key="A_MOUSE_01", depth=constants.DEPTH_CREATURE, creature=creature_com,
                  ai=ai_com, item=item_com)

    return mouse
