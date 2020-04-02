from src import esper, config
from src.components.action import UseStairsAction
from src.components.position import Position
from src.components.stairs import Stairs


class StairProcessor(esper.Processor):
    def process(self):
        for ent, (pos, _) in self.level.world.get_components(Position, UseStairsAction):
            self.level.world.remove_component(ent, UseStairsAction)
            stairs = self.level.first_component_at_position(pos, Stairs)
            if stairs:
                config.GAME.transition(stairs.leads_to)
