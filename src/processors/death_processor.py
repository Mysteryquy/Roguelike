from src import esper
from src.components.death import Death
from src.components.health import Health


class DeathProcessor(esper.Processor):
    def process(self):
        for ent, (renderable, health, death) in self.world.get_components(Renderable, Health, Death):
            pass