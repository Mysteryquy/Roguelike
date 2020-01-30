from enum import Enum

import tcod.path as path

import config
import constants
import game_map
import render
from game_map import DungeonLevel


class GameState(Enum):
    RUNNING = 1
    PAUSE = 2


class Game:
    def __init__(self):

        self.state = GameState.RUNNING

        self.message_history = []


        self.current_level = None
        self.create_new_level("1", place_objects=False)


        self.maps_previous = []

        self.maps_next = []

    @property
    def current_floor_number(self):
        return len(self.maps_previous) +1

    @property
    def current_floor(self):
        return self.current_level.floor

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


    def transition_init(self, next = True):
        self.current_level.player_x, self.current_level.player_y = config.PLAYER.x, config.PLAYER.y

        for obj in self.current_objects:
            obj.animation_destroy()

        if next:
            self.maps_previous.append(self.current_level)
        else:
            self.maps_next.insert(0, self.current_level)



    def create_new_level(self, level_code="1", initial_stairs=True, place_objects=True):
        self.current_level = DungeonLevel([config.PLAYER], level_code=level_code)
        if place_objects:
            print(self.current_level.rooms)
            game_map.place_objects(self.current_level.rooms)
        config.PLAYER.animation_init()




    def transition_to_level(self, level, new_level=False):
        self.current_level = level

        for obj in self.current_objects:
            obj.animation_init()
        if not new_level:
            config.PLAYER.x = self.current_level.player_x
            config.PLAYER.y = self.current_level.player_y
        game_map.transition_reset()
        game_map.make_fov(self.current_map)
        config.FOV_CALCULATE = True
        render.fill_surfaces()

    def transition_next(self):
        self.transition_init(next=True)


        if len(self.maps_next) == 0:
            self.create_new_level()
            self.transition_to_level(self.current_level, new_level=True)

        else:
            self.transition_to_level(self.maps_next[0])
            del self.maps_next[0]


    def transition_previous(self):
        if len(self.maps_previous) > 0:
            self.transition_init(next=False)
            self.transition_to_level(self.maps_previous[-1])
            del self.maps_previous[-1]

        else:
            self.game_message("There is no previous level", constants.COLOR_WHITE)

    def game_message(self, game_msg, msg_color=constants.COLOR_GREY):
        self.message_history.append((game_msg, msg_color))
