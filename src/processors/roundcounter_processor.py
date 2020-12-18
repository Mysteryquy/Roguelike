from src import esper, config
from src.components.action import HasAction


class RoundCounterProcessor(esper.Processor):
    def process(self):
        if not self.level.world.has_component(self.player, HasAction):
            # player used his action
            config.ROUND_COUNTER += 1
