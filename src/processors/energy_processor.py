from src import esper
from src.components.action import HasAction
from src.components.energy import Energy


class EnergyProcessor(esper.Processor):
    def process(self):
        for ent, nrg in self.world.get_component(Energy):
            nrg.energy += nrg.increment
            if nrg.energy >= nrg.max_energy:
                nrg.energy -= nrg.max_energy
                self.world.add_component(ent, HasAction())

        pass
