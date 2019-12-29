from enum import Enum

import tcod.path as path

import config
import constants
import game_map
import render


class GameState(Enum):
    RUNNING = 1
    PAUSE = 2


class Game:
    def __init__(self):

        self.state = GameState.RUNNING

        self.message_history = []

        self.current_objects = []

        self.maps_previous = []

        self.maps_next = []

        self.current_map, self.current_rooms = game_map.create()

        tmp = config.FOV_MAP

        self.pathing = path.AStar(tmp, 0)

        self.auto_explore_path = None

        self.stairs = []

    def transition_next(self):

        config.FOV_CALCULATE = True

        for obj in self.current_objects:
            obj.animation_destroy()

        self.maps_previous.append(
            (config.PLAYER.x, config.PLAYER.y, self.current_map, self.current_rooms, self.current_objects, self.stairs))

        if len(self.maps_next) == 0:

            self.current_objects = [config.PLAYER]

            config.PLAYER.animation_init()

            self.current_map, self.current_rooms = game_map.create()

            self.pathing = path.AStar(config.FOV_MAP, 0)

            self.stairs = []

            game_map.place_objects(self.current_rooms)


        else:
            (
            config.PLAYER.x, config.PLAYER.y, self.current_map, self.current_rooms, self.current_objects, self.stairs) = \
                self.maps_next[-1]
            self.pathing = path.AStar(config.FOV_MAP, 0)

            for obj in self.current_objects:
                obj.animation_init()

            game_map.make_fov(self.current_map)

            config.FOV_CALCULATE = True

            del self.maps_next[-1]

        render.fill_surfaces()

    def transition_previous(self):

        if len(self.maps_previous) != 0:

            for obj in self.current_objects:
                obj.animation_destroy()

            self.maps_next.append(
                (config.PLAYER.x, config.PLAYER.y, self.current_map, self.current_rooms, self.current_objects,
                 self.stairs))

            (
            config.PLAYER.x, config.PLAYER.y, self.current_map, self.current_rooms, self.current_objects, self.stairs) = \
                self.maps_previous[-1]

            for obj in self.current_objects:
                obj.animation_init()

            game_map.make_fov(self.current_map)
            render.fill_surfaces()
            self.pathing = path.AStar(config.FOV_MAP, 0)
            config.FOV_CALCULATE = True

            del self.maps_previous[-1]
        else:
            self.game_message("There is no previous level", constants.COLOR_WHITE)

    def game_message(self, game_msg, msg_color=constants.COLOR_GREY):
        self.message_history.append((game_msg, msg_color))
