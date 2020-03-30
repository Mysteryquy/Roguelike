from src import esper, config
from src.components.action import HasAction


class RoundCounterProcessor(esper.Processor):
    def process(self):
        if self.world.has_component(self.player, HasAction):
            # player still has action afterwards:
            config.ROUND_COUNTER += 1
