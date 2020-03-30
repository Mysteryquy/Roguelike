from src import constants
from src.components.ai import AiChase
from src.components.attacker import Attacker
from src.components.block import BlocksMovement
from src.components.energy import Energy
from src.components.health import Health
from src.components.name import Name
from src.components.position import Position
from src.components.render import Renderable


def gen_demon_avin(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20),Position(x, y), Attacker(attack=8, defense=2, hit_chance=5, evasion_chance=3),
                              Name("Avin"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_AVIN"),
                              Energy(100),
                              BlocksMovement()
                              )
