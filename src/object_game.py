from enum import Enum

from src import config, constants, map_helper, render_helper, generator
from typing import List, Dict, Optional

from src.components.action import HasAction
from src.components.attacker import Attacker
from src.components.block import BlocksMovement
from src.components.energy import Energy
from src.components.health import Health
from src.components.name import Name
from src.components.persisent import Persistent
from src.components.player import Player
from src.components.position import Position
from src.components.render import Renderable
from src.components.stairs import Stairs
from src.components.stats import Stats
from src.dungeonlevel import DungeonLevel
from src.resources.levels import Levels


class GameState(Enum):
    RUNNING = 1
    PAUSE = 2


class Game:

    def __init__(self, game_save, game_load, player_name):
        self.state: GameState = GameState.RUNNING
        self.levels: Dict[Levels, DungeonLevel] = {}
        self.message_history: List[str] = []
        self.message_history_old_length: int = 0
        self.game_save = game_save
        self.game_load = game_load
        self.player_name = player_name
        first_level = Levels.HELL1
        self.create_new_level(first_level, create_player=True)
        self.current_level: DungeonLevel = self.levels[first_level]
        config.FOV_CALCULATE = True
        self.current_level.place_stairs(place_player=True)
        self.current_level.place_objects()

    @property
    def current_level_name(self) -> str:
        return self.current_level.name

    @property
    def current_rooms(self):
        return self.current_level.rooms

    @property
    def current_map(self):
        return self.current_level.map

    @property
    def pathing(self):
        return self.current_level.pathing


    def create_new_level(self, level_name, create_player=False):
        level = DungeonLevel(level_name=level_name)
        if create_player:
            generator.gen_player(level, (0, 0), self.player_name)

        level.init_processors(game_save=self.game_save, game_load=self.game_load)
        self.levels[level_name] = level
        return level

    def _transition_to_level(self, level_name):
        # self.current_level.player_x, self.current_level.player_y = pos.x, pos.y

        for ent, _ in self.current_level.world.get_component(Persistent):
            if self.current_level.world.has_component(ent, Player):
                # player is not removed as entity, just delete its components
                for comp in self.current_level.world.all_components_for_entity(ent):
                    self.levels[level_name].world.add_component(ent, comp)
                    self.current_level.world.remove_component(ent, type(comp))
            else:
                for comp in self.current_level.world.all_components_for_entity(ent):
                    self.levels[level_name].world.add_component(ent, comp)
                self.current_level.world.delete_entity(ent, immediate=True)

        prev_level_name = self.current_level.name
        self.current_level = self.levels[level_name]
        # find the corresponding pair of stairs
        stairs_pos = None
        for ent, (pos, stairs) in self.levels[level_name].world.get_components(Position, Stairs):
            if stairs.leads_to == prev_level_name:
                stairs_pos = pos

        assert stairs_pos is not None
        pos = self.current_level.world.component_for_player(Position)
        pos.x, pos.y = stairs_pos.x, stairs_pos.y
        map_helper.transition_reset()
        config.FOV_CALCULATE = True
        self.current_level.calculate_fov()
        render_helper.fill_surfaces()
        self.current_level.render_processor.draw_mini_map()

    def transition(self, to_level):
        constants.CURRENT_LEVEL_NAME = to_level
        make_new = to_level not in self.levels
        if make_new:
            level = self.create_new_level(level_name=to_level)
            self.levels[to_level].place_stairs()
        self._transition_to_level(to_level)
        if make_new:
            self.levels[to_level].place_objects()

    def game_message(self, game_msg, msg_color=constants.COLOR_GREY):
        self.message_history.append((game_msg, msg_color))
