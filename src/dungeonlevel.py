from typing import List

import pygame
from tcod import path

from src import constants, config, esper
from src.components.position import Position
from src.dungeon_generator import DungeonGenerator


class DungeonLevel:

    def __init__(self, level_name, entities=None):
        self.player_x = -1
        self.player_y = -1
        gen = DungeonGenerator(level_name)
        self.fov_map = None
        # raise AttributeError("FOV_MAP INIT HERE")
        self.map, self.rooms = gen.generate(constants.MAP_WIDTH, constants.MAP_HEIGHT)
        self.pathing = path.AStar(config.FOV_MAP, 0)
        self.auto_explore_path = None
        self.name = level_name
        self.world = esper.World()
        if entities:
            for cs in entities:
                self.world.create_entity(cs)

    def add_processor(self, processor: esper.Processor, priority=1) -> None:
        self.world.add_processor(self, processor, priority=priority)

    def create_entity(self, *components) -> None:
        """
        creates an entity with the given components
        :param components:
        :return: nothing
        """
        self.world.create_entity(components)

    def entities_at_coords(self, x: int, y: int, exclude_ent=None, *components):
        """
        gives the objects at the given coordinates (= Entities with Position component with position = (x,y)
        :param exclude_ent:
        :param x: x position
        :param y: y position
        :param components: if you only want entities with the specific components
        :return: the wanted entities
        """
        objects = []
        for ent, pos in self.world.get_component(Position, components):
            if pos.x == x and pos.y == y:
                if not exclude_ent or exclude_ent != ent:
                    objects.append(ent)
        return objects

    def is_visible(self, x, y):
        return self.fov_map.fov[y, x]

    def is_walkable(self, x, y):
        return self.fov_map.walkable[y, x]

    def is_explored(self, x, y):
        return self.map[x][y].explored

    def place_objects(self, first_level=False):
        top_level = constants.LevelNames.is_first_level(self.name) if not first_level else True
        final_level = constants.LevelNames.is_last_level(self.name) if not first_level else False
        room_list = self.rooms

        for room in room_list:

            # Tobias room tile calculation
            cal_x = room.right - room.left
            cal_y = room.bottom - room.top
            room_size = cal_x * cal_y

            room_center = room.center
            first_room = (room == room_list[0])
            last_room = (room == room_list[-1])

            if first_room:
                x, y = room.center
                x, y = int(x), int(y)
                config.PLAYER.x, config.PLAYER.y = x, y
                self.player_x, self.player_y = x, y

            if first_room and top_level:
                x, y = room.center
                generator.gen_portal(self, room.center)

            if first_room and not top_level:
                generator.gen_stairs(self, (config.PLAYER.x, config.PLAYER.y), downwards=False)

            if last_room:

                if final_level:
                    # gen_END_GAME_ITEM(room.center)
                    # gen_stairs(room.center,downwards=True)
                    generator.gen_end_game_item(self, room.center)
                else:
                    generator.gen_stairs(self, room.center, downwards=True)

            how_much_to_place(self, room_size, room)
