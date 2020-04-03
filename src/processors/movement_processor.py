import math

from src import esper, config
from src.components.alignment import Alignment, CreatureAlignment
from src.components.attacker import Attacker
from src.components.block import BlocksMovement
from src.components.health import Health
from src.components.action import MovementAction, MeleeAttackAction
from src.components.position import Position


class MovementProcessor(esper.Processor):
    def process(self):
        for ent, (pos, movement_action, alignment) in \
                self.level.world.get_components(Position, MovementAction, Alignment):

            goal = Position(pos.x + movement_action.dx, pos.y + movement_action.dy)
            self.level.world.remove_component(ent, MovementAction)
            target = self.level.first_entity_components_at_position(goal,
                                                                  BlocksMovement, Alignment, exclude_ent=None)
            if target:
                target_ent, (_, alignment_target) = target
                # cannot use movement action normally, check other stuff

                if alignment_target:
                    # if the target has no alignment, no action is made
                    if CreatureAlignment.can_bump(alignment.alignment, alignment_target.alignment):
                        if self.level.world.has_component(ent, Attacker):
                            self.level.world.add_component(ent, MeleeAttackAction(target_ent))
                    elif CreatureAlignment.can_swap(alignment.alignment, alignment_target.alignment):
                        pos2 = self.level.world.component_for_entity(target, Position)
                        tmp = pos
                        pos.x, pos.y = pos2.x, pos2.y
                        pos2.x, pos2.y = tmp.x, tmp.y
            else:
                # can freely move
                if self.level.is_walkable_position(goal):
                    pos.x, pos.y = goal.x, goal.y
                    config.FOV_CALCULATE = True


def distance_between(pos1: Position, pos2: Position) -> float:
    dx, dy = pos1.x - pos2.x, pos1.y - pos2.y
    return math.hypot(dx, dy)
