import tcod

import config
import constants
import generator
from dungeon_generator import DungeonGenerator
import inspect
from structure import Structure, Stairs
import random
import tcod.path as path
from actor import Actor


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


class DungeonLevel:

    def __init__(self, objects, level_name):
        self.player_x = -1
        self.player_y = -1
        self.map, self.rooms = create(level_name=level_name)
        self.objects = objects
        self.pathing = path.AStar(config.FOV_MAP, 0)
        self.auto_explore_path = None
        self.stairs = []
        self.name = level_name

    def objects_at_coords(self, coords_x, coords_y):
        object_options = [obj for obj in self.objects
                          if obj.x == coords_x and obj.y == coords_y]

        return object_options

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
                self.player_x, self.player_y = x,y


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



def is_visible(x, y):
    return config.FOV_MAP.fov[y, x]


def get_path(start_x, start_y, goal_x, goal_y):
    return config.GAME.pathing.get_path(start_x, start_y, goal_x, goal_y)


def create(level_name):
    gen = DungeonGenerator(level_name)
    new_map = gen.generate(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    return new_map




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


def make_fov(incoming_map):
    config.FOV_MAP = tcod.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            # same as before, but now we have array for walkable and transparent
            config.FOV_MAP.walkable[y, x] = not incoming_map[x][y].block_path
            config.FOV_MAP.transparent[y, x] = not incoming_map[x][y].block_path


def calculate_fov():
    if config.FOV_CALCULATE:
        config.FOV_CALCULATE = False
        print(config.PLAYER.x)
        config.FOV_MAP.compute_fov(config.PLAYER.x, config.PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
                                   constants.FOV_ALGO)



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


def is_walkable(x, y):
    return config.FOV_MAP.walkable[y, x]


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
    if room_size <= 20:
        fuckingree = 3
    elif room_size <= 30:
        fuckingree = 4
    elif room_size <= 40:
        fuckingree = 5
    elif room_size <= 50:
        fuckingree = 6
    else:
        fuckingree = 2
    for i in range(0, fuckingree):
        x = tcod.random_get_int(None, room.left + 1, room.right - 1)
        y = tcod.random_get_int(None, room.top + 1, room.bottom - 1)
        if len(level.objects_at_coords(x, y)) == 0:
            generator.what_to_gen(level, (x, y))


def is_explored(x, y):
    return config.GAME.current_map[x][y].explored


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
