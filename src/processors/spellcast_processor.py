from src import esper
from src.components.action import SpellcastAction
import src.resources.spells as _spells


class SpellcastProcessor(esper.Processor):
    def process(self):
        for ent, spell in self.level.world.get_component(SpellcastAction):
            _spells.spell_dict[spell.spell](ent, spell.args)
            self.level.world.remove_component(ent, SpellcastAction)
