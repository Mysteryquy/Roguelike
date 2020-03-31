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
        for ent, (pos, movement_action) in self.level.world.get_components(Position, MovementAction):
            goal_x, goal_y = pos.x + movement_action.dx, pos.y + movement_action.dy
            ents = self.level.entities_at_coords(goal_x, goal_y, BlocksMovement, exclude_ent=None)
            if len(ents) > 0:
                self.level.world.remove_component(ent, MovementAction)
                # cannot use movement action normally, check other stuff
                target = next((e for e in ents if self.level.world.has_component(e, BlocksMovement)), None)
                assert target is not None
                assert self.level.world.has_component(ent, Alignment)
                alignment_mover = self.level.world.component_for_entity(ent, Alignment)
                alignment_target = self.level.world.component_for_entity(target, Alignment).alignment if \
                    self.level.world.has_component(target, Alignment) else None

                if alignment_target:
                    # if the target has no alignment, no action is made
                    if CreatureAlignment.can_bump(alignment_mover.alignment, alignment_target):
                        if self.level.world.has_component(ent, Attacker):
                            self.level.world.add_component(ent, MeleeAttackAction(target))
                    elif CreatureAlignment.can_swap(alignment_mover.alignment, alignment_target):
                        pos2 = self.level.world.component_for_entity(target, Position)
                        tmp = pos
                        pos.x, pos.y = pos2.x, pos2.y
                        pos2.x, pos2.y = tmp.x, tmp.y
            else:
                # can freely move
                if self.level.is_walkable(goal_x, goal_y):
                    pos.x, pos.y = goal_x, goal_y
                    config.FOV_CALCULATE = True
                self.level.world.remove_component(ent, MovementAction)


def distance_between(pos1: Position, pos2: Position) -> float:
    dx, dy = pos1.x - pos2.x, pos1.y - pos2.y
    return math.hypot(dx, dy)
