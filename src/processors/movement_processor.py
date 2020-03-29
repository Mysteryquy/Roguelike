import math

from src import esper
from src.components.attacker import Attacker
from src.components.block import BlocksMovement
from src.components.health import Health
from src.components.movement import MovementAction
from src.components.position import Position


class MovementProcessor(esper.Processor):
    def process(self):
        for ent, (pos, movement_action) in self.world.get_components(Position, MovementAction):
            goal_x, goal_y = pos.x + movement_action.dx, pos.y + movement_action.dy
            ents = self.level.entities_at_coords(goal_x, goal_y, BlocksMovement)
            if len(ents) > 0:
                # cannot use movement action, see if maybe melee attack action may be used instead
                to_attack = next((e for e in ents if self.world.has_component(e, Health)), None)
                if self.level.world.has_component(ent, Attacker) and to_attack:
                    self.world.remove_component(ent, MovementAction)
                    self.world.add_component(ent, MeleeAttackAction(to_attack))
            else:
                # can freely move
                pos.x, pos.y = goal_x, goal_y


def distance_between(pos1: Position, pos2: Position) -> float:
    dx, dy = pos1.x - pos2.x, pos1.y - pos2.y
    return math.hypot(dx, dy)
