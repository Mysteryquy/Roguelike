from src import esper
from src.components.action import HasAction
from src.components.energy import Energy


class EnergyProcessor(esper.Processor):
    def process(self):
        if not self.level.world.has_component(self.player, HasAction):
            for ent, nrg in self.level.world.get_component(Energy):
                nrg.energy += nrg.increment
                if nrg.energy >= nrg.max_energy:
                    nrg.energy -= nrg.max_energy
                    self.level.world.add_component(ent, HasAction())


