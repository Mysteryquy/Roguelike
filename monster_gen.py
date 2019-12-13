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
                              apply=effect.StatusEffect(owner=None, duration=20, effect_dict={Status.MAX_HP:setter_value},autostart=False))
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
                            dead_animation_key="S_FLESH_NORMAL")
    ai_com = ai.AiChase()

    elemental = Actor(x, y, "Elemental", animation_key="A_ELEMENTAL_FIRE", depth=constants.DEPTH_CREATURE,
                      creature=creature_com,
                      ai=ai_com)

    burn = effect.OnHitEffect(owner=elemental, duration=None, apply=effect.DamageOverTimeEffect(applier=elemental, duration=3, damage=1) )
    elemental.creature.add_onhit_effect(burn)


    return elemental