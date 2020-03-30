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
