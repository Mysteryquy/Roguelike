import random

from src import esper, config, constants
from src.components.ai import Ai, AiType, AiConfuse, AiChase, AiFlee
from src.components.action import MovementAction
from src.components.position import Position


class AiProcessor(esper.Processor):

    def process(self):
        for ent, ai in self.level.world.get_component(AiConfuse):
            if ai.duration > 0:
                dx = random.randint(-1,1)
                dy = random.randint(-1,1)
                self.level.world.add_component(ent, MovementAction(dx=dx,dy=dy))
                ai.duration -= 1
            else:
                self.level.world.remove_component(ent, AiConfuse)
                self.level.world.add_component(ent, ai.old_ai)
                # TODO delete this
                config.GAME.game_message("A creature has stopped being confused", constants.COLOR_GREEN)

        for ent, (pos, ai) in self.level.world.get_components(Position, AiChase):
            x, y = pos
            goal_x, goal_y = ai.target
            if ai.act_unseen or self.level.is_visible(x, y):
                path = iter(self.level.pathing.get_path(x, y, goal_x, goal_y))
                next_x, next_y = next(path, (0, 0))
                self.level.world.add_component(ent, MovementAction(next_x - x, next_y - y))

        for ent, (pos, ai) in self.level.world.get_components(Position, AiFlee):
            print("REEE")




