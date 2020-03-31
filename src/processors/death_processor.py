from src import esper, config, constants
from src.components.death import Death, Dead
from src.components.experience import Experience
from src.components.health import Health
from src.components.name import Name
from src.components.position import Position
from src.components.render import Renderable


class DeathProcessor(esper.Processor):
    def process(self):
        for ent, (renderable, _, death, pos, name) in \
                self.level.world.get_components(Renderable, Dead, Death, Position, Name):
            print("DEAD")
            if death.animation_key:
                self.level.world.create_entity(
                    Renderable(animation_key=death.animation_key, depth=constants.DEPTH_CORPSE),
                    Position(pos.x, pos.y))

            if death.killer:
                killer_name = next(self.level.world.try_component(death.killer, Name))
                config.GAME.game_message(name.name + " is slain by " + killer_name.name, constants.COLOR_RED)
                killer_xp = next(self.level.world.try_component(death.killer, Experience), None)
                killed_xp = next(self.level.world.try_component(ent, Experience), None)
                if killer_xp and killed_xp:
                    killer_xp.current_experience += killed_xp.on_death

            else:
                config.GAME.game_message(name.name + " dies", constants.COLOR_RED_LIGHT)
            if death.custom_death:
                death.custom_death()

            self.level.world.delete_entity(ent)
