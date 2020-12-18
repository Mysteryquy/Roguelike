import random

from src import esper, config, constants
from src.components.ai import Ai, AiType, AiConfuse, AiChase, AiFlee
from src.components.action import MovementAction, HasAction
from src.components.position import Position


class AiProcessor(esper.Processor):

    def process(self):
        for ent, (ai, _) in self.level.world.get_components(AiConfuse, HasAction):
            if ai.duration > 0:
                dx = random.randint(-1,1)
                dy = random.randint(-1,1)
                self.level.world.add_component(ent, MovementAction(dx=dx,dy=dy))
                self.level.world.remove_component(ent, HasAction)
                ai.duration -= 1
            else:
                self.level.world.remove_component(ent, AiConfuse)
                self.level.world.add_component(ent, ai.old_ai)
                # TODO delete this
                config.GAME.game_message("A creature has stopped being confused", constants.COLOR_GREEN)

        for ent, (pos, ai, _) in self.level.world.get_components(Position, AiChase, HasAction):
            if ai.act_unseen or self.level.is_visible(pos.x, pos.y):
                path = iter(self.level.pathing.get_path(pos.x, pos.y, ai.target.x, ai.target.y))
                next_x, next_y = next(path, (0, 0))
                self.level.world.add_component(ent, MovementAction(next_x - pos.x, next_y - pos.y))
                self.level.world.remove_component(ent, HasAction)

