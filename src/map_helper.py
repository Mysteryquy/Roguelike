from typing import Tuple, Iterator

import pygame
import tcod

from src import config, constants, generator
import random

from src.components.name import Name
from src.components.position import Position
from src.components.render import Renderable
from src.resources.levels import Levels


def transition_reset():
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if config.GAME.current_map[x][y].explored:
                config.GAME.current_map[x][y].draw_on_minimap = True
                config.GAME.current_map[x][y].draw_on_screen = True
                config.GAME.current_map[x][y].was_drawn = False

    config.FOV_CALCULATE = True


def find_line(coords1: Tuple[int, int], coords2: Tuple[int, int], include_origin: bool = False) -> Iterator[
            Tuple[int, int]]:
    """Converts who x,y coords into a list of tiles. coords1 = (x1, y1) coords2 = (x2, y2)"""
    x1, y1 = coords1
    x2, y2 = coords2
    rtn = tcod.line_iter(x1, y1, x2, y2)
    if not include_origin:
        next(rtn)

    return rtn


def find_radius(coords: Tuple[int, int], radius: int) -> Iterator[Tuple[int, int]]:
    c_x, c_y = coords
    return ((c_x + x, c_y + y) for x in range(-radius, radius + 1) for y in range(-radius, radius + 1))


def how_much_to_place(level, room_size: int, room: pygame.Rect) -> None:
    count = 2
    for i in range(0, count):
        x = tcod.random_get_int(None, room.left + 1, room.right - 1)
        y = tcod.random_get_int(None, room.top + 1, room.bottom - 1)
        ent = level.first_entity_at_position(Position(x, y))
        if not ent:
            generator.what_to_gen(level, (x, y))


def search_empty_tile(level, origin_x: int, origin_y: int, radius_x: int, radius_y: int, exclude_origin: bool = False):
    tiles = [(origin_x + dx, origin_y + dy) for dx in range(-radius_x, radius_x + 1)
             for dy in range(-radius_y, radius_y + 1)]
    random.shuffle(tiles)
    for x, y in tiles:
        if x < constants.MAP_WIDTH and y < constants.MAP_HEIGHT and level.is_walkable(x, y) and level.is_visible(x, y) \
                and not level.first_entity_at_coords(x, y):
            return x, y

    return None


def place_map_specific(level):
    if level.name == Levels.WATER1:
        for room in level.rooms:
            for i in range(2):
                x = tcod.random_get_int(None, room.left + 1, room.right - 1)
                y = tcod.random_get_int(None, room.top + 1, room.bottom - 1)
                ent = level.first_entity_at_position(Position(x, y))
                if not ent:
                    level.world.create_entity(Position(x, y), Name("Bubble"),
                                              Renderable(animation_key="DECOR_STATUE_01",
                                                         depth=constants.DEPTH_STRUCTURES,
                                                         special_flags=pygame.BLEND_RGBA_ADD))


def random_point_in_rect(rect: pygame.Rect):
    return random.choice(range(rect.left, rect.right)), random.choice(range(rect.top, rect.bottom))


def check_bounds(x: int, y: int) -> bool:
    return 0 <= x <= constants.MAP_WIDTH and 0 <= y <= constants.MAP_HEIGHT
