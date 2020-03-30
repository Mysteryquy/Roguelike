from typing import List

import pygame
from tcod import path, tcod

from src import constants, config, esper, generator
from src.components.position import Position
from src.dungeon_generator import DungeonGenerator
from src.processors.ai_processor import AiProcessor
from src.processors.energy_processor import EnergyProcessor
from src.processors.input_processor import InputProcessor
from src.processors.movement_processor import MovementProcessor
from src.processors.render_processor import RenderProcessor
from src.processors.roundcounter_processor import RoundCounterProcessor
from src.processors.stair_processor import StairProcessor


class DungeonLevel:

    def __init__(self, level_name, entities=None):
        self.player_x = -1
        self.player_y = -1
        gen = DungeonGenerator(level_name)
        self.map, self.rooms = gen.generate(constants.MAP_WIDTH, constants.MAP_HEIGHT)
        self.fov_map = tcod.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)
        for y in range(constants.MAP_HEIGHT):
            for x in range(constants.MAP_WIDTH):
                self.fov_map.walkable[y, x] = not self.map[x][y].block_path
                self.fov_map.transparent[y, x] = not self.map[x][y].block_path

        self.pathing = path.AStar(self.fov_map, 0)
        self.auto_explore_path = None
        self.name = level_name
        self.world = esper.World()

        if entities:
            for cs in entities:
                self.world.create_entity(cs)

    def calculate_fov(self):
        if config.FOV_CALCULATE:
            config.FOV_CALCULATE = False
            pos = config.GAME.current_level.world.component_for_player(Position)
            self.fov_map.compute_fov(pos.x, pos.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
                                     constants.FOV_ALGO)

    def init_processors(self, game_load, game_save):
        self.world.add_processor(self, EnergyProcessor(), priority=1000)
        self.world.add_processor(self, InputProcessor(game_load=game_load, game_save=game_save), priority=999)
        self.world.add_processor(self, AiProcessor(), priority=998)
        self.world.add_processor(self, MovementProcessor(), priority=997)
        self.world.add_processor(self, RoundCounterProcessor(), priority=11)
        self.world.add_processor(self, RenderProcessor(self), priority=10)
        self.world.add_processor(self, StairProcessor())

    def entities_at_coords(self, x: int, y: int, *components, **kwargs):
        """
        gives the objects at the given coordinates (= Entities with Position component with position = (x,y)
        :param exclude_ent:
        :param x: x position
        :param y: y position
        :param components: if you only want entities with the specific components
        :return: the wanted entities
        """
        objects = []
        for ent, tpl in self.world.get_components(Position, *components):
            if tpl[0].x == x and tpl[0].y == y:
                if "exclude_ent" not in kwargs or not kwargs["exclude_ent"] or kwargs["exclude_ent"] != ent:
                    objects.append(ent)
        return objects

    def is_visible(self, x, y):
        return self.fov_map.fov[y, x]

    def is_walkable(self, x, y):
        return self.fov_map.walkable[y, x]

    def is_explored(self, x, y):
        return self.map[x][y].explored

    def place_objects(self, first_level=False):
        pos = self.world.component_for_player(Position)
        top_level = constants.LevelNames.is_first_level(self.name) if not first_level else True
        final_level = constants.LevelNames.is_last_level(self.name) if not first_level else False
        room_list = self.rooms

        for room in room_list:

            # Tobias room tile calculation
            cal_x = room.right - room.left
            cal_y = room.bottom - room.top

            first_room = (room == room_list[0])
            last_room = (room == room_list[-1])

            if first_room:
                x, y = room.center
                x, y = int(x), int(y)
                pos = self.world.component_for_player(Position)
                pos.x, pos.y = x, y
                self.player_x, self.player_y = x, y
                config.FOV_CALCULATE = True

            if first_room and top_level:
                x, y = room.center
                # generator.gen_portal(self, room.center)

            if first_room and not top_level:
                generator.gen_stairs(self, (pos.x, pos.y), leads_to=constants.LevelNames.previous_level_name(self.name)
                                     , downwards=False)

            if last_room:

                if final_level:
                    print("KEK")
                    # gen_END_GAME_ITEM(room.center)
                    # gen_stairs(room.center,downwards=True)
                    # generator.gen_end_game_item(self, room.center)
                else:
                    generator.gen_stairs(self, room.center, leads_to=constants.LevelNames.next_level_name(self.name))

            # how_much_to_place(self, room_size, room)
