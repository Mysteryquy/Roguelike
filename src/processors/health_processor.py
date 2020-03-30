from src import esper, config, constants
from src.components.health import TakeDamageEvent, Health
from src.components.name import Name


class HealthProcessor(esper.Processor):
    def process(self):
        for ent, (name, health, damage_event) in self.level.world.get_components(Name, Health, TakeDamageEvent):
            optional = ("by " + damage_event.source) if damage_event.source else ""
            config.GAME.game_message(name.name + " is dealt " + str(damage_event.damage) + " damage " + optional,
                                     msg_color=constants.COLOR_RED)
            health.current_health -= damage_event.damage
            self.level.world.remove_component(ent, TakeDamageEvent)
