import random

import numpy
from tcod import tcod

from src import monster_gen, item_gen
from src import constants
from src.components.alignment import CreatureAlignment, Alignment
from src.components.attacker import Attacker
from src.components.block import BlocksMovement
from src.components.container import Container
from src.components.death import Death
from src.components.energy import Energy
from src.components.experience import Experience
from src.components.health import Health
from src.components.name import Name
from src.components.persisent import Persistent
from src.components.player import Player
from src.components.position import Position
from src.components.render import Renderable
from src.components.stairs import Stairs
from src.components.stats import Stats
import src.death as _death


def gen_stairs(level, coords, leads_to, downwards=True):
    x, y = coords
    animation_key = "S_STAIRS_DOWN" if downwards else "S_STAIRS_UP"
    level.world.create_entity(Position(x, y), Stairs(leads_to=leads_to, downwards=downwards),
                              Renderable(animation_key=animation_key, depth=constants.DEPTH_STRUCTURES,
                                         draw_explored=True))


def what_to_gen(level, coords):
    # Change to 3 to see buggy gold
    rng = random.randint(1, 2)
    x, y = coords
    if rng == 1:
        monster_gen.gen_and_append_enemy(level, coords)
    if rng == 2:
        item_gen.gen_item(level, coords)


def gen_player(level, coords, player_name):
    x, y = coords
    level.world.add_components_to_player(Player(), Persistent(), Position(x, y),
                                         Name(player_name), Health(100),
                                         Stats(10, 10, 10),
                                         Energy(100),
                                         Renderable(animation_key="A_PLAYER", animation_speed=1.0),
                                         Attacker(attack=666, hit_chance=100, evasion_chance=10, defense=5),
                                         Stats(strength=10, dexterity=10, intelligence=10),
                                         BlocksMovement(),
                                         Alignment(CreatureAlignment.PLAYER),
                                         Experience(),
                                         Container(),
                                         Death(animation_key="S_DEAD_DEMON", custom_death=_death.death_player)
                                         )
