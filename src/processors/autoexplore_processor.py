from typing import Optional, Tuple

from src import esper, config, constants
from src.components.action import StartAutoexploreAction, HasAction, MovementAction
from src.components.alignment import CreatureAlignment, Alignment
from src.components.autoexplore import AutoExploring
from src.components.position import Position
from src.components.stairs import Stairs


class AutoExploreProcessor(esper.Processor):
    def process(self):
        for ent, (_, pos, alignment) in self.level.world.get_components(StartAutoexploreAction,
                                                                        Position, Alignment):
            self.level.world.remove_component(ent, StartAutoexploreAction)
            for ent2, alignment2 in self.level.get_visible_entity_component(Alignment, exclude_ent=ent):
                if CreatureAlignment.can_bump(alignment.alignment, alignment2.alignment):
                    config.GAME.game_message("ENEMY NEARBY! Cannot explore", constants.COLOR_RED_LIGHT)
                    return

            goal = self.new_goal(pos.x, pos.y)

            if not goal:
                config.GAME.game_message(config.GAME.game_message("Cannot autoexplore", constants.COLOR_BLUE_LIGHT))
            else:
                (goal_x, goal_y), continue_after_goal = goal
                path = iter(config.GAME.pathing.get_path(pos.x, pos.y, goal_x, goal_y))
                self.level.world.add_component(ent, AutoExploring(path=path, continue_after_goal=continue_after_goal))

        for ent, (autoexploring, pos, alignment) in self.level.world.get_components(AutoExploring,
                                                                                    Position, Alignment):
            if not self.level.world.has_component(ent, HasAction):
                self.level.world.remove_component(ent, AutoExploring)
            else:
                flag = False
                for ent2, alignment2 in self.level.get_visible_entity_component(Alignment, exclude_ent=ent):
                    if CreatureAlignment.can_bump(alignment.alignment, alignment2.alignment):
                        flag = True
                        break
                if flag and not autoexploring.force_one_move:
                    config.GAME.game_message("ENEMY NEARBY! Cannot explore", constants.COLOR_RED_LIGHT)
                    self.level.world.remove_component(ent, AutoExploring)
                else:
                    autoexploring.force_one_move = False
                    x, y = next(autoexploring.path, (0, 0))
                    if (x, y) == (0, 0):
                        if not autoexploring.continue_after_goal:
                            self.level.world.remove_component(ent, AutoExploring)
                            continue
                        goal = self.new_goal(pos.x, pos.y)
                        if goal:
                            (goal_x, goal_y), continue_after_goal = self.new_goal(pos.x, pos.y)
                            autoexploring.path = iter(config.GAME.pathing.get_path(pos.x, pos.y, goal_x, goal_y))
                            autoexploring.continue_after_goal = continue_after_goal
                            x, y = next(autoexploring.path, (0, 0))
                        else:
                            config.GAME.game_message("Cannot autoexplore further", constants.COLOR_RED_LIGHT)
                            break
                    dx, dy = x - pos.x, y - pos.y
                    self.level.world.add_component(ent, MovementAction(dx, dy))
                    self.level.world.remove_component(ent, HasAction)

    def new_goal(self, start_x: int, start_y: int) -> Optional[Tuple[Tuple[int, int], bool]]:
        goal_x, goal_y = start_x, start_y
        # check room centers first
        for room in config.GAME.current_rooms:
            x, y = room.center
            if not self.level.is_explored(x, y):
                return (x, y), True
        # check all tiles
        for x in range(0, constants.MAP_WIDTH):
            for y in range(0, constants.MAP_HEIGHT):
                if not self.level.is_explored(x, y) and self.level.is_walkable(x, y):
                    return (x, y), True

        # all tiles explored, check for stairs
        for ent, (pos, stairs) in sorted(self.level.world.get_components(Position, Stairs),
                                         key=lambda t: not t[1][1].downwards,):
            if pos.x != start_x or pos.y != start_y:
                return (pos.x, pos.y), False
