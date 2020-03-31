import numpy
from tcod import tcod

from src import monster_gen
from src import constants
from src.components.alignment import CreatureAlignment, Alignment
from src.components.attacker import Attacker
from src.components.block import BlocksMovement
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


def gen_stairs(level, coords, leads_to, downwards=True):
    x, y = coords
    animation_key = "S_STAIRS_DOWN" if downwards else "S_STAIRS_UP"
    level.world.create_entity(Position(x, y), Stairs(leads_to=leads_to, downwards=downwards),
                              Renderable(animation_key=animation_key, depth=constants.DEPTH_STRUCTURES,
                                         draw_explored=True))


def what_to_gen(level, coords):
    # Change to 3 to see buggy gold
    rng = 1
    x, y = coords
    if rng == 1:
        gen_and_append_enemy(level, (x, y))


level_monster_dict = {
    "DUNGEON1": [(monster_gen.gen_demon_avin, 100)],
    "DUNGEON2": [(monster_gen.gen_demon_avin, 100)],
    "DUNGEON3": [(monster_gen.gen_demon_avin, 1)]
}


def gen_and_append_enemy(level, coords):
    monsters_and_weight = level_monster_dict[level.name]
    monsters = [monster for monster, _ in monsters_and_weight]
    sum_weights = sum([weight for _, weight in monsters_and_weight])
    probabilities = [weight / sum_weights for _, weight in monsters_and_weight]
    monster_function = numpy.random.choice(monsters, 1, p=probabilities)[0]
    monster_function(level, coords)


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
                                         Death(animation_key="S_DEAD_DEMON")
                                         )
