import tcod

import ai
import casting
import config
import constants
import death
from actor import Actor, TemporaryActor
from creature import Creature
from item import Item
import effect
from creature import Status

def gen_demon_pillus(coords):
    x, y = coords

    max_health = 200
    attack = 80
    defence = 20
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "Pillus"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_DEMON")
    ai_com = ai.AiChase()

    demon_pillus = Actor(x, y, "Demon", animation_key="A_DEMON_PILLUS", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return demon_pillus


def gen_demon_buffla(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 5
    doge_value = 3
    xp_granted = 100

    creature_name = "Buffla"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_DEMON")
    ai_com = ai.AiChase()

    demon_buffla = Actor(x, y, "Demon", animation_key="A_DEMON_BUFFLA", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return demon_buffla


def gen_demon_avin(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 5
    doge_value = 3
    xp_granted = 100

    creature_name = "Avin"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_DEMON")
    ai_com = ai.AiChase()

    demon_avin = Actor(x, y, "Demon", animation_key="A_DEMON_AVIN", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return demon_avin


def gen_demon_gronk(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 5
    doge_value = 3
    xp_granted = 100

    creature_name = "Gronk"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_DEMON")
    ai_com = ai.AiChase()

    demon_gronk = Actor(x, y, "Demon", animation_key="A_DEMON_GRONK", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return demon_gronk


def gen_demon_sloosh(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 5
    doge_value = 3
    xp_granted = 100

    creature_name = "Sloosh"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_DEMON")
    ai_com = ai.AiChase()

    demon_sloosh = Actor(x, y, "Demon", animation_key="A_DEMON_SLOOSH", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return demon_sloosh


def gen_demon_kolak(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 5
    doge_value = 3
    xp_granted = 100

    creature_name = "Kolak"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_DEMON")
    ai_com = ai.AiChase()

    demon_kolak = Actor(x, y, "Demon", animation_key="A_DEMON_KOLAK", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return demon_kolak


def gen_demon_absodux(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 5
    doge_value = 3
    xp_granted = 100

    creature_name = "Absodux"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_DEMON")
    ai_com = ai.AiChase()

    demon_absodux = Actor(x, y, "Demon", animation_key="A_DEMON_ABSODUX", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return demon_absodux


def gen_demon_nergal(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 5
    doge_value = 3
    xp_granted = 100

    creature_name = "Nergal"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_DEMON")
    ai_com = ai.AiChase()

    demon_nergal = Actor(x, y, "Demon", animation_key="A_DEMON_NERGAL", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return demon_nergal

def gen_demon_boomi(coords):
    x, y = coords

    max_health = 30
    attack = 5
    defence = 2
    hit_chance = 80
    doge_value = 1
    xp_granted = 300

    creature_name = "Creeper"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_DEMON", custom_death=death.death_demon_boomi)
    ai_com = ai.AiChase()

    demon_boomi = Actor(x, y, "Demon", animation_key="A_DEMON_BOOMI", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return demon_boomi


def gen_reptile_anaconda(coords):
    x, y = coords

    max_health = tcod.random_get_int(None, 15, 20)
    base_attack = tcod.random_get_int(None, 3, 6)
    setter_value = -5

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=40, base_evasion=0, xp_gained=300,
                            dead_animation_key="S_FLESH_SNAKE"
                            )
    ai_com = ai.AiChase()



    snake = Actor(x, y, "Anaconda", animation_key="A_SNAKE_ANACONDA", depth=constants.DEPTH_CREATURE, creature=creature_com,
                  ai=ai_com)

    poison = effect.OnHitEffect(owner=snake, duration=None,
                              apply_attacked=effect.StatusEffect(owner=None, duration=20, effect_dict={Status.MAX_HP:setter_value},autostart=False))
    snake.creature.add_onhit_effect(poison)

    return snake


def gen_reptile_cobra(coords):
    x, y = coords

    max_health = tcod.random_get_int(None, 5, 10)
    base_attack = tcod.random_get_int(None, 1, 3)

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=80, base_evasion=10, xp_gained=300,
                            dead_animation_key="S_FLESH_SNAKE")
    ai_com = ai.AiChase()

    snake = Actor(x, y, "Cobra", animation_key="A_SNAKE_COBRA", depth=constants.DEPTH_CREATURE, creature=creature_com,
                  ai=ai_com)

    return snake


def gen_rodent_mouse(coords):
    x, y = coords

    max_health = 1
    base_attack = 0

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_evasion=60,
                            dead_animation_key="S_FLESH_EAT", alignment=Creature.CreatureAlignment.NEUTRAL)
    ai_com = ai.AiFlee()

    item_com = Item(use_function=casting.cast_heal, value=2, pickup_text="Rat Carcass")

    mouse = Actor(x, y, "Mouse", animation_key="A_RODENT_MOUSE", depth=constants.DEPTH_CREATURE, creature=creature_com,
                  ai=ai_com, item=item_com)

    return mouse


def gen_slime_small(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    small_slime = Actor(x, y, "Small slime", animation_key="A_SLIME_SMALL", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return small_slime


def gen_slime_small_blue(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    small_slime_blue = Actor(x, y, "Small slime blue", animation_key="A_SLIME_SMALL_BLUE", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return small_slime_blue


def gen_slime_ice(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    ice_slime = Actor(x, y, "Small slime", animation_key="A_SLIME_ICE", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return ice_slime


def gen_slime_abomination(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    abomination_slime = Actor(x, y, "Abomination Slime", animation_key="A_SLIME_ABOMINATION", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return abomination_slime


def gen_cat_cat(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Citty"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    cat_cat = Actor(x, y, "Cat", animation_key="A_CAT_CAT", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cat_cat


def gen_cat_leopard(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Leo"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    cat_leopard = Actor(x, y, "Cat", animation_key="A_CAT_LEOPARD", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cat_leopard


def gen_cat_panther(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "T´Challa"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    cat_panther = Actor(x, y, "Panther", animation_key="A_CAT_PANTHER", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cat_panther


def gen_cat_tiger(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Tigress"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    cat_tiger = Actor(x, y, "Tiger", animation_key="A_CAT_TIGER", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cat_tiger


def gen_cat_lion(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Simba"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    cat_lion = Actor(x, y, "Tiger", animation_key="A_CAT_LION", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cat_lion


def gen_cat_mountain(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Mounty Cat"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    cat_mountain = Actor(x, y, "Mountain Cat", animation_key="A_CAT_MOUNTAIN", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cat_mountain


def gen_cat_snow(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Snowy Cat"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    cat_snow = Actor(x, y, "Snow Cat", animation_key="A_CAT_SNOW", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cat_snow


def gen_cat_shadow(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Nightcrawler"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    cat_shadow = Actor(x, y, "Shadow Cat", animation_key="A_CAT_SHADOW", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cat_shadow


def gen_cat_walking(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Walki-Catty"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    cat_walking = Actor(x, y, "Walking Cat", animation_key="A_CAT_WALKING", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cat_walking


def gen_slime_blob(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Blobber"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    blob_slime = Actor(x, y, "Slime Blob", animation_key="A_SLIME_BLOB", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return blob_slime


def gen_slime_cube(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = "Cubic Chaos"

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    cube_slime = Actor(x, y, "Cubic Slime", animation_key="A_SLIME_CUBE", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return cube_slime


def gen_slime_ring(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    ring_slime = Actor(x, y, "Ring Slime", animation_key="A_SLIME_RING", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return ring_slime


def gen_slime_snatcher(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    snatcher_slime = Actor(x, y, "Snatcher Slime", animation_key="A_SLIME_SNTACHER", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return snatcher_slime


def gen_slime_sack(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    sack_slime = Actor(x, y, "Sack Slime", animation_key="A_SLIME_SACK", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return sack_slime


def gen_slime_mold_yellow(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    yellow_mold = Actor(x, y, "Yellow Mold", animation_key="A_SLIME_MOLD_YELLOW", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return yellow_mold


def gen_slime_mold_brown(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    brown_mold = Actor(x, y, "Brown Mold", animation_key="A_SLIME_MOLD_BROWN", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return brown_mold


def gen_slime_mold_green(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    green_mold = Actor(x, y, "Green Mold", animation_key="A_SLIME_MOLD_GREEN", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return green_mold


def gen_slime_mold_red(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    red_mold = Actor(x, y, "Red Mold", animation_key="A_SLIME_MOLD_RED", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return red_mold


def gen_slime_mold_blue(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    blue_mold = Actor(x, y, "Blue Mold", animation_key="A_SLIME_MOLD_BLUE", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return blue_mold


def gen_slime_mold_purple(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    purple_mold = Actor(x, y, "Purple Mold", animation_key="A_SLIME_MOLD_PURPLE", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return purple_mold


def gen_slime_fire(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    small_slime = Actor(x, y, "Small slime", animation_key="A_SLIME_FIRE", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return small_slime


def gen_slime_ice_fire(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_SLIME")
    ai_com = ai.AiChase()

    ice_fire_slime = Actor(x, y, "Hot n Cold Slime", animation_key="A_SLIME_ICE_FIRE", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return ice_fire_slime


def gen_dog_dog(coords):
    x, y = coords

    max_health = 8
    attack = 2
    defence = 1
    hit_chance = 75
    doge_value = 5
    xp_granted = 40

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_DOG")
    ai_com = ai.AiCaster()

    dog = Actor(x, y, "Dog", animation_key="A_DOG_DOG", depth=constants.DEPTH_CREATURE,
                creature=creature_com,
                ai=ai_com)

    return dog


def gen_pest_snail(coords):
    x, y = coords

    max_health = 5
    attack = 2
    defence = 2
    hit_chance = 70
    doge_value = 10
    xp_granted = 40

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_SNAIL")
    ai_com = ai.AiChase()

    snail = Actor(x, y, "Snail", animation_key="A_SNAIL", depth=constants.DEPTH_CREATURE,
                  creature=creature_com,
                  ai=ai_com)

    return snail


def gen_pest_small_spider(coords):
    x, y = coords

    max_health = 10
    attack = 4
    defence = 0
    hit_chance = 70
    doge_value = 10
    xp_granted = 60

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, custom_death=None, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted, dead_animation_key = "S_FLESH_SPIDER",)
    ai_com = ai.AiChase()

    small_spider = Actor(x, y, "Small Spider", animation_key="A_PEST_SMALL_SPIDER", depth=constants.DEPTH_CREATURE,
                         creature=creature_com,
                         ai=ai_com)

    return small_spider


def gen_pest_small_scorpion(coords):
    x, y = coords

    max_health = 10
    attack = 4
    defence = 2
    hit_chance = 70
    doge_value = 10
    xp_granted = 70

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, custom_death=None, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    small_scorpion = Actor(x, y, "Small Scorpion", animation_key="A_PEST_SMALL_SCORPION", depth=constants.DEPTH_CREATURE,
                           creature=creature_com,
                           ai=ai_com)

    return small_scorpion


def gen_pest_worm(coords, name=None):
    x, y = coords

    max_health = 12
    attack = 3
    defence = 2
    hit_chance = 85
    doge_value = 15
    xp_granted = 70

    creature_name = name if name else tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, custom_death=death.death_worm, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_WORM")
    ai_com = ai.AiChase()

    worm = Actor(x, y, "Worm", animation_key="A_PEST_WORM", depth=constants.DEPTH_CREATURE,
                 creature=creature_com,
                 ai=ai_com)

    return worm


def gen_humanoid_goblin(coords):
    x, y = coords

    max_health = 13
    attack = 5
    defence = 1
    hit_chance = 85
    doge_value = 15
    xp_granted = 100

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    goblin = Actor(x, y, "Goblin", animation_key="A_HUMANOID_GOBLIN", depth=constants.DEPTH_CREATURE,
                   creature=creature_com,
                   ai=ai_com)

    return goblin


def gen_undead_ghost(coords, duration):
    x, y = coords

    max_health = 20
    attack = 10
    defence = 3
    hit_chance = 100
    doge_value = 50
    xp_granted = 0

    creature_name = "Ghostler"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            alignment=Creature.CreatureAlignment.FRIEND)
    ai_com = ai.AiChase()

    ghost = TemporaryActor(x=x, y=y, name_object="Ghost", animation_key="A_UNDEAD_GHOST", duration=10, depth=constants.DEPTH_CREATURE,
                   creature=creature_com,
                   ai=ai_com)

    return ghost


def gen_elemental_potato(coords):
    x, y = coords

    max_health = 25
    attack = 6
    defence = 0
    hit_chance = 85
    doge_value = 15
    xp_granted = 500

    creature_name = "Markus"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_POTATO", depth=constants.DEPTH_CREATURE,
                   creature=creature_com,
                   ai=ai_com)

    return elemental


def gen_elemental_fire(coords):
    x, y = coords

    max_health = 30
    attack = 5
    defence = 2
    hit_chance = 100
    doge_value = 25
    xp_granted = 1000

    creature_name = "Flamey"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_FIRE", death_text="Crumbles into a Pile of Ash")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_FIRE", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)

    burn = effect.OnHitEffect(owner=elemental, duration=None,
                              apply_attacker=effect.DamageOverTimeEffect(applier=elemental, duration=1, damage=-2),
                              apply_attacked=effect.DamageOverTimeEffect(applier=elemental, duration=3, damage=1))
    elemental.creature.add_onhit_effect(burn)


    return elemental


def gen_elemental_ice(coords):
    x, y = coords

    max_health = 30
    attack = 5
    defence = 2
    hit_chance = 100
    doge_value = 15
    xp_granted = 1000

    creature_name = "Icey"

    creature_com = Creature(creature_name, custom_death=death.death_ice_elemental, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_ICE")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_ICE", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)


    return elemental


def gen_elemental_icicle(coords):
    x, y = coords

    max_health = 30
    attack = 5
    defence = 2
    hit_chance = 100
    doge_value = 15
    xp_granted = 1000

    creature_name = "Icey-fleißi"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_ICE", death_text= "Is smashed to a little Snowball")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_ICICLE", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)


    return elemental


def gen_elemental_earth(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "Rocky"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_DEAD_EARTH", death_text=" gets composted into a mossy mess!")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_EARTH", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)


    return elemental


def gen_elemental_lightning(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "Zappy"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_LIGHTNING", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return elemental


def gen_elemental_paper(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "Papyrus"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_PAPER", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return elemental


def gen_elemental_slime(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "Slimey"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_SLIME", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return elemental


def gen_elemental_flesh(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "Flabsy"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_FLESH", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return elemental


def gen_elemental_gold(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "Richy"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_FLESH", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return elemental


def gen_elemental_mimic(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "Flabsy"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_MIMIC", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)




    return elemental


def gen_elemental_steel(coords):
    x, y = coords

    max_health = 20
    attack = 8
    defence = 2
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "STEELOX"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_STEEL", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)

    return elemental


def gen_boss_beholder(coords):
    x, y = coords

    max_health = 200
    attack = 80
    defence = 20
    hit_chance = 50
    doge_value = 30
    xp_granted = 1000

    creature_name = "8-Eyes"

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted,
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    beholder = Actor(x, y, "Boss", animation_key="A_BOSS_BEHOLDER", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)



    return beholder