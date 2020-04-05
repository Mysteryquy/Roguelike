from src import esper, config, constants
from src.components.experience import Experience
from src.components.level import Level
import src.components.experience as exp
from src.components.name import Name


class ExperienceProcessor(esper.Processor):
    def process(self):
        for ent, (level, name, experience) in self.level.world.get_components(Level, Name, Experience):
            if experience.current_experience >= exp.XP_NEEDED[level.level]:
                level.level += 1
                config.GAME.game_message(name.name + " levels up to level" + str(level.level), constants.COLOR_BLUE)