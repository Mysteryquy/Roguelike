from src import constants
from src.components.ai import AiChase
from src.components.alignment import Alignment, CreatureAlignment
from src.components.attacker import Attacker
from src.components.block import BlocksMovement
from src.components.death import Death
from src.components.energy import Energy
from src.components.experience import Experience
from src.components.health import Health
from src.components.name import Name
from src.components.position import Position
from src.components.render import Renderable


def gen_demon_avin(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y), Attacker(attack=8, defense=2, hit_chance=50, evasion_chance=3),
                              Name("Avin"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_AVIN"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_DEAD_DEMON")
                              )
