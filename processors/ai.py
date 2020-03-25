import esper
from components.ai import Ai


class AiProcessor(esper.Processor):
    def __init__(self):
        pass

    def process(self):
        for ent, ai in self.world.get_component(Ai):
            # handle stuff here...
            pass
