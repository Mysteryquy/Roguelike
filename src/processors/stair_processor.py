from src import esper, config
from src.components.action import UseStairsAction
from src.components.position import Position
from src.components.stairs import Stairs


class StairProcessor(esper.Processor):
    def process(self):
        for ent, (pos, _) in self.level.world.get_components(Position, UseStairsAction):
            self.level.world.remove_component(ent, UseStairsAction)
            ents = self.level.entities_at_coords(pos.x, pos.y, Stairs)
            if len(ents) > 0:
                stairs = self.level.world.component_for_entity(ents[0], Stairs)
                config.GAME.transition(stairs.leads_to)

