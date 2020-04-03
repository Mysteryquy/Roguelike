from typing import List, Optional

import pygame
from tcod import path, tcod

from src import constants, config, esper, generator, map_helper
from src.components.position import Position
from src.dungeon_generator import DungeonGenerator
from src.processors.ai_processor import AiProcessor
from src.processors.attack_processor import AttackProcessor
from src.processors.autoexplore_processor import AutoExploreProcessor
from src.processors.death_processor import DeathProcessor
from src.processors.energy_processor import EnergyProcessor
from src.processors.health_processor import HealthProcessor
from src.processors.input_processor import InputProcessor
from src.processors.movement_processor import MovementProcessor
from src.processors.pickup_processor import PickUpProcessor
from src.processors.render_processor import RenderProcessor
from src.processors.roundcounter_processor import RoundCounterProcessor
from src.processors.spellcast_processor import SpellcastProcessor
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
        self.render_processor = RenderProcessor(self)
        self.world.add_processor(self, EnergyProcessor(), priority=1000)
        self.world.add_processor(self, InputProcessor(game_load=game_load, game_save=game_save), priority=999)
        self.world.add_processor(self, AutoExploreProcessor(), priority=997)
        self.world.add_processor(self, SpellcastProcessor(), priority=996)
        self.world.add_processor(self, AiProcessor(), priority=995)
        self.world.add_processor(self, MovementProcessor(), priority=990)
        self.world.add_processor(self, PickUpProcessor(), priority=950)
        self.world.add_processor(self, AttackProcessor(), priority=900)
        self.world.add_processor(self, HealthProcessor(), priority=600)
        self.world.add_processor(self, RoundCounterProcessor(), priority=11)
        self.world.add_processor(self, DeathProcessor(), priority=6)
        self.world.add_processor(self, self.render_processor, priority=5)
        self.world.add_processor(self, StairProcessor())

    def only_entities_at_position(self, pos: Position, *components, exclude_ent=None):
        """
        gives the objects at the given coordinates (= Entities with Position component with position = (x,y)
        :param pos:
        :param exclude_ent:
        :param components: if you only want entities with the specific components
        :return: the wanted entities
        """
        return (ent for ent, (p, *_) in self.world.get_components(Position, *components)
                if p == pos and (not exclude_ent or exclude_ent != ent))

    def first_entity_at_position(self, pos: Position, *components, exclude_ent=None) -> Optional[int]:
        for ent, (p, *_) in self.world.get_components(Position, *components):
            if p == pos and (not exclude_ent or exclude_ent != ent):
                return ent
        return None

    def first_entity_component_at_position(self, pos: Position, component_type, exclude_ent=None):
        for ent, (p, *comps) in self.world.get_components(Position, component_type):
            if p == pos and (not exclude_ent or exclude_ent != ent):
                return ent, comps
        return None

    def first_entity_components_at_position(self, pos: Position, *components, exclude_ent=None):
        for ent, (p, *comps) in self.world.get_components(Position, *components):
            if p == pos and (not exclude_ent or exclude_ent != ent):
                return ent, comps
        return None

    def first_component_at_position(self, pos: Position, component_type, exclude_ent=None):
        for ent, (p, comp) in self.world.get_components(Position, component_type):
            if p == pos and (not exclude_ent or exclude_ent != ent):
                return comp
        return None

    def first_components_at_position(self, pos: Position, *components, exclude_ent=None):
        for ent, (p, *comps) in self.world.get_components(Position, *components):
            if p == pos and (not exclude_ent or exclude_ent != ent):
                return comps
        return None

    def get_visible_entity_components(self, *components, exclude_ent=None):
        """
        helper method to get specific components that are visible to the player
        :param exclude_ent: exclude a specific entity
        :param components: the wanted component types
        :return: a list of (ent, components) tuples with the corresponding components,
                 note that components is a list
        """
        return ((ent, comps) for ent, (pos, *comps) in self.world.get_components(Position, *components)
                if self.is_visible_position(pos) and (not exclude_ent or exclude_ent != ent))

    def get_visible_entity_component(self, component_type, exclude_ent: Optional[int] = None):
        """
        helper method to get specific component that is visible to the player
        :param component_type: the wanted component
        :param exclude_ent: exclude a specific entity
        :return: a list of (ent, component) tuples with the corresponding component
        """
        return ((ent, comp) for ent, (pos, comp) in self.world.get_components(Position, component_type)
                if self.is_visible_position(pos) and (not exclude_ent or exclude_ent != ent))

    def only_components_at_position(self, pos: Position, *component_types, exclude_ent=None):
        """
        helper method to find specific components  at the coordinates. Note that this does not give the entities
        for tuples use
        :param pos:
        :param exclude_ent: exclude specific entity
        :return:
        """
        return (comps for ent, (p, *comps) in self.world.get_components(Position, *component_types)
                if p == pos and (not exclude_ent or ent != exclude_ent))

    def get_entity_components_at_position(self, pos: Position, *component_types, exclude_ent=None):
        return ((ent, comps) for ent, (p, *comps) in self.world.get_components(Position, *component_types)
                if p == pos and (not exclude_ent or ent != exclude_ent))

    def get_entity_component_at_position(self, pos: Position, component_type, exclude_ent=None):
        return ((ent, comp) for ent, (p, comp) in self.world.get_components(Position, component_type)
                if p == pos and (not exclude_ent or ent != exclude_ent))

    def is_visible(self, x, y):
        return self.fov_map.fov[y, x]

    def is_walkable(self, x, y):
        return self.fov_map.walkable[y, x]

    def is_explored(self, x, y):
        return self.map[x][y].explored

    def is_visible_position(self, pos: Position):
        return self.fov_map.fov[pos.y, pos.x]

    def is_walkable_position(self, pos: Position):
        return self.fov_map.walkable[pos.y, pos.x]

    def is_explored_position(self, pos: Position):
        return self.map[pos.x][pos.y].explored

    def place_objects(self, first_level=False):
        pos = self.world.component_for_player(Position)
        top_level = constants.LevelNames.is_first_level(self.name) if not first_level else True
        final_level = constants.LevelNames.is_last_level(self.name) if not first_level else False
        room_list = self.rooms

        for room in room_list:

            # Tobias room tile calculation
            cal_x = room.right - room.left
            cal_y = room.bottom - room.top

            room_size = cal_x * cal_y

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

            map_helper.how_much_to_place(self, room_size, room)
