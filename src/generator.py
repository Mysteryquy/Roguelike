import numpy
from tcod import tcod

from src import monster_gen
from src import constants
from src.components.position import Position
from src.components.render import Renderable
from src.components.stairs import Stairs


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
