from src import esper, config, constants
from src.components.death import Dead, Death
from src.components.health import TakeDamageEvent, Health
from src.components.name import Name


class HealthProcessor(esper.Processor):
    def process(self):
        for ent, (name, health, damage_event) in self.level.world.get_components(Name, Health, TakeDamageEvent):
            optional = ""
            if damage_event.source:
                name_source = next(self.level.world.try_component(damage_event.source, Name), None)
                optional = ("by " + name_source.name)
            config.GAME.game_message(name.name + " is dealt " + str(damage_event.damage) + " damage " + optional,
                                     msg_color=constants.COLOR_RED)
            if health.current_health - damage_event.damage <= 0:
                health.current_health = 0
                death = next(self.level.world.try_component(ent, Death), None)
                if death:
                    death.killer = damage_event.source
                self.level.world.add_component(ent, Dead())
            else:
                health.current_health -= damage_event.damage
            self.level.world.remove_component(ent, TakeDamageEvent)

