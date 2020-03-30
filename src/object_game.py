from enum import Enum

from src import config, constants, map_helper, render_helper
from typing import List, Dict, Optional

from src.components.energy import Energy
from src.components.health import Health
from src.components.name import Name
from src.components.persisent import Persistent
from src.components.player import Player
from src.components.position import Position
from src.components.render import Renderable
from src.components.stats import Stats
from src.dungeonlevel import DungeonLevel


class GameState(Enum):
    RUNNING = 1
    PAUSE = 2


class Game:

    def __init__(self, game_save, game_load, player_name):
        self.state: GameState = GameState.RUNNING
        self.levels: Dict[str, DungeonLevel] = {}
        self.message_history: List[str] = []
        self.game_save = game_save
        self.game_load = game_load
        self.player_name = player_name
        self.create_new_level("DUNGEON1", first_level=True, create_player=True)
        self.current_level: Optional[DungeonLevel] = self.levels["DUNGEON1"]
        constants.CURRENT_LEVEL_NAME: str = self.current_level_name

    @property
    def current_level_name(self) -> str:
        return self.current_level.name

    @property
    def current_objects(self):
        return self.current_level.objects

    @property
    def current_rooms(self):
        return self.current_level.rooms

    @property
    def stairs(self):
        return self.current_level.stairs

    @property
    def current_map(self):
        return self.current_level.map

    @property
    def pathing(self):
        return self.current_level.pathing

    @property
    def auto_explore_path(self):
        return self.current_level.auto_explore_path

    @auto_explore_path.setter
    def auto_explore_path(self, value):
        self.current_level.auto_explore_path = value

    def create_new_level(self, level_name, first_level=False, create_player=False):
        level = DungeonLevel(level_name=level_name)
        if create_player:
            level.world.add_components_to_player(Player(), Persistent(), Position(0, 0),
                                                 Name(self.player_name), Health(100),
                                                 Stats(10, 10, 10),
                                                 Energy(100),
                                                 Renderable(animation_key="A_PLAYER", animation_speed=1.0)
                                                 )
        level.place_objects(first_level=first_level)
        level.init_processors(game_save=self.game_save, game_load=self.game_load)
        self.levels[level_name] = level
        return level

    def transition_to_level(self, level_name, new_level=False):

        for ent, _ in self.current_level.world.get_component(Persistent):
            if self.current_level.world.has_component(ent, Player):
                # player is not removed as entity, just delete its components
                for comp in self.current_level.world.components_for_entity(ent):
                    self.levels[level_name].world.add_component(ent, comp)
                    self.current_level.world.remove_component(ent, comp)
            else:
                for comp in self.current_level.world.components_for_entity(ent):
                    self.levels[level_name].world.add_component(ent, comp)
                self.current_level.world.delete_entity(ent, immediate=True)

        self.current_level = self.levels[level_name]

        map_helper.transition_reset()
        map_helper.make_fov(self.current_map)
        config.FOV_CALCULATE = True
        render_helper.fill_surfaces()

    def transition(self, to_level):
        constants.CURRENT_LEVEL_NAME = to_level
        make_new = to_level not in self.levels
        if make_new:
            level = self.create_new_level(level_name=to_level)
            level.place_objects()
        self.transition_to_level(to_level, new_level=make_new)
        self.current_level = self.levels[to_level]

    def game_message(self, game_msg, msg_color=constants.COLOR_GREY):
        self.message_history.append((game_msg, msg_color))
