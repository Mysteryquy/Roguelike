import tcod

from src import config, constants, generator
import random

from src.components.name import Name
from src.components.position import Position
from src.components.render import Renderable


def transition_reset():
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if config.GAME.current_map[x][y].explored:
                config.GAME.current_map[x][y].draw_on_minimap = True
                config.GAME.current_map[x][y].draw_on_screen = True
                config.GAME.current_map[x][y].was_drawn = False

def get_path(start_x, start_y, goal_x, goal_y):
    return config.GAME.pathing.get_path(start_x, start_y, goal_x, goal_y)


def check_for_creature(x, y, exclude_object=None):
    target = None

    if exclude_object:
        # ceck objectlist to find creature at that location that isnt excluded
        for obj in config.GAME.current_objects:
            if (obj is not exclude_object and
                    obj.x == x and
                    obj.y == y and
                    obj.creature):
                target = obj

            if target:
                return target

    else:
        # ceck objectlist to find any creature at that location
        for obj in config.GAME.current_objects:
            if (obj.x == x and
                    obj.y == y and
                    obj.creature):
                target = obj

            if target:
                return target


def find_line(coords1, coords2, include_origin=False):
    """Converts who x,y coords into a list of tiles. coords1 = (x1, y1) coords2 = (x2, y2)"""

    x1, y1 = coords1
    x2, y2 = coords2

    if x1 == x2 and y1 == y2:
        return [(x1, y1)]

    if include_origin:
        return list(tcod.line_iter(x1, y1, x2, y2))
    else:
        tmp = tcod.line_iter(x1, y1, x2, y2)
        tmp.__next__()
        return list(tmp)


def find_radius(coords, radius):
    center_x, center_y = coords

    tile_list = []

    start_x = (center_x - radius)
    end_x = (center_x + radius + 1)

    start_y = (center_y - radius)
    end_y = (center_y + radius + 1)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            tile_list.append((x, y))

    return tile_list


def how_much_to_place(level, room_size, room):
    count = 2
    for i in range(0, count):
        x = tcod.random_get_int(None, room.left + 1, room.right - 1)
        y = tcod.random_get_int(None, room.top + 1, room.bottom - 1)
        ent = level.first_entity_at_position(Position(x, y))
        if not ent:
            generator.what_to_gen(level, (x, y))


def is_explored(x, y):
    return config.GAME.current_map[x][y].explored



def search_empty_tile(origin_x: int, origin_y: int, radius_x: int, radius_y: int, exclude_origin: bool = False):
    tiles = []
    for i in list(range(-radius_x, radius_x + 1)):
        for j in list(range(-radius_y, radius_y + 1)):
            if not (exclude_origin and i == 0 and j == 0):
                tiles.append((i, j))
    random.shuffle(tiles)
    for i, j in tiles:
        x, y = origin_x + i, origin_y + j
        if x < constants.MAP_WIDTH and y < constants.MAP_HEIGHT and is_walkable(x, y) and is_visible(x, y) and len(
                objects_at_coords(x, y)) == 0:
            return x, y

    return None


def place_map_specific(level):
    if level.name == "WATER1":
        for room in level.rooms:
            for i in range(2):
                x = tcod.random_get_int(None, room.left + 1, room.right - 1)
                y = tcod.random_get_int(None, room.top + 1, room.bottom - 1)
                ent = level.first_entity_at_position(Position(x, y))
                if not ent:
                    level.world.create_entity(Position(x, y), Name("Bubble"),
                                              Renderable(animation_key="DECOR_STATUE_01",
                                                         depth=constants.DEPTH_STRUCTURES))
