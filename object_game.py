from enum import Enum

from src import config, constants
import game_map
import render
from game_map import DungeonLevel
from typing import List, Dict, Optional


class GameState(Enum):
    RUNNING = 1
    PAUSE = 2

class Game:





    def __init__(self):
        self.state: GameState = GameState.RUNNING
        self.levels: Dict[str, DungeonLevel] = {}
        self.message_history: List[str] = []
        self.create_new_level("DUNGEON1", first_level=True)
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

    def create_new_level(self, level_name, first_level=False):
        level = DungeonLevel([config.PLAYER], level_name=level_name)
        level.place_objects(first_level=first_level)
        self.levels[level_name] = level

        config.PLAYER.animation_init()

        return level

    def transition_to_level(self, level_name, new_level=False):
        self.current_level = self.levels[level_name]

        for obj in self.current_objects:
            obj.animation_init()
        if not new_level:
            config.PLAYER.x = self.current_level.player_x
            config.PLAYER.y = self.current_level.player_y
        game_map.transition_reset()
        game_map.make_fov(self.current_map)
        config.FOV_CALCULATE = True
        render.fill_surfaces()

    def transition(self, to_level):
        self.current_level.player_x, self.current_level.player_y = config.PLAYER.x, config.PLAYER.y
        constants.CURRENT_LEVEL_NAME = to_level
        make_new = to_level not in self.levels
        if make_new:
            level = self.create_new_level(level_name=to_level)
            level.place_objects()
        self.transition_to_level(to_level, new_level=make_new)
        self.current_level = self.levels[to_level]

    def game_message(self, game_msg, msg_color=constants.COLOR_GREY):
        self.message_history.append((game_msg, msg_color))
