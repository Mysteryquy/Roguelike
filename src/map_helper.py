import tcod

from src import config, constants, generator
import random

from src.components.position import Position


def transition_reset():
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if config.GAME.current_map[x][y].explored:
                config.GAME.current_map[x][y].draw_on_minimap = True
                config.GAME.current_map[x][y].draw_on_screen = True
                config.GAME.current_map[x][y].was_drawn = False


class Tile:
    def __init__(self, block_path, texture):
        self.block_path = block_path
        self.explored = False
        self._texture = texture
        self._texture_explored = self._texture + "_EXPLORED"
        self.draw_on_minimap = False
        self.draw_on_screen = False
        self.was_drawn = False

    @property
    def texture(self):
        return self._texture

    @property
    def texture_explored(self):
        return self._texture_explored

    @texture.setter
    def texture(self, value):
        self._texture = value
        self._texture_explored = value + "_EXPLORED"


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
        if len(level.only_entities_at_coords(x, y)) == 0:
            generator.what_to_gen(level, (x, y))


def is_explored(x, y):
    return config.GAME.current_map[x][y].explored

"""
def get_path_from_player(goal_x: int, goal_y: int):
    return config.GAME.pathing.get_path(config.PLAYER.x, config.PLAYER.y, goal_x, goal_y)


def start_auto_explore(new_goal=True):
    # check if every room was explored

    for obj in config.GAME.current_objects:
        if obj.creature and is_visible(obj.x, obj.y) and obj.creature.is_foe():
            config.GAME.game_message("ENEMY NEARBY! Cannot explore", constants.COLOR_RED_LIGHT)
            return
    if new_goal:
        autoexplore_new_goal()


def get_path_to_player(start_x, start_y):
    return config.GAME.pathing.get_path(start_x, start_y, config.PLAYER.x, config.PLAYER.y)


def check_contine_autoexplore():
    for obj in config.GAME.current_objects:
        if obj.creature and is_visible(obj.x, obj.y) and obj.creature.is_foe():
            config.GAME.game_message("ENEMY NEARBY! Stopped exploring", constants.COLOR_RED_LIGHT)
            return False
    return True


def autoexplore_new_goal():
    goal_x, goal_y = config.PLAYER.x, config.PLAYER.y

    for room in config.GAME.current_rooms:
        x, y = room.center
        if not is_explored(x, y):
            print("HALlo")
            goal_x, goal_y = x, y

    # maybe do some more stuff here
    config.AUTO_EXPLORING = goal_x != config.PLAYER.x or goal_y != config.PLAYER.y

    if not config.AUTO_EXPLORING:
        for x in range(0, constants.MAP_WIDTH):
            for y in range(0, constants.MAP_HEIGHT):
                if not is_explored(x, y) and is_walkable(x, y):
                    goal_x, goal_y = x, y

    config.AUTO_EXPLORING = goal_x != config.PLAYER.x or goal_y != config.PLAYER.y

    if config.AUTO_EXPLORING:
        print((goal_x, goal_y))
        config.GAME.auto_explore_path = iter(get_path_from_player(goal_x, goal_y))
        return True
    else:
        if config.CANNOT_AUTOEXPLORE_FURTHER:
            config.CANNOT_AUTOEXPLORE_FURTHER = False
            for obj in sorted(config.GAME.stairs, key=lambda x: x.structure.downwards, reverse=True):
                if obj.structure and isinstance(obj.structure, Structure) and not (
                        obj.x == config.PLAYER.x and obj.y == config.PLAYER.y):
                    goal_x, goal_y = obj.x, obj.y
                    print((goal_x, goal_y))
                    config.GAME.auto_explore_path = iter(get_path_from_player(goal_x, goal_y))
                    config.AUTO_EXPLORING = True
                    return True
        config.GAME.game_message("Cannot autoexplore further", constants.COLOR_BLUE_LIGHT)
        config.CANNOT_AUTOEXPLORE_FURTHER = True
        return False

"""
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
