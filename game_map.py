import tcod
import constants
import config
import generator
from dungeon_generator import DungeonGenerator


class Tile:
    def __init__(self, block_path, texture):
        self.block_path = block_path
        self.explored = False
        self._texture = texture
        self._texture_explored = self._texture + "_EXPLORED"

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        self._texture = value
        self._texture_explored = value + "_EXPLORED"

    def get_texture(self, visible):
        if visible:
            return self._texture
        else:
            return self._texture_explored


def is_visible(x, y):
    return config.FOV_MAP.fov[y, x]


def get_path(start_x, start_y, goal_x, goal_y):
    return config.GAME.pathing.get_path(start_x, start_y, goal_x, goal_y)

def create():
    gen = DungeonGenerator()
    new_map = gen.generate(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    return new_map



def place_objects(room_list):
    current_level = len(config.GAME.maps_previous) + 1

    top_level = current_level == 1
    final_level = (current_level == constants.MAP_NUM_LEVELS)

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
            config.PLAYER.x, config.PLAYER.y = int(x), int(y)

        if first_room and top_level:
            x, y = room.center
            generator.gen_portal(room.center)

        if first_room and not top_level:
            generator.gen_stairs((config.PLAYER.x, config.PLAYER.y), downwards=False)

        if last_room:

            if final_level:
                # gen_END_GAME_ITEM(room.center)
                # gen_stairs(room.center,downwards=True)
                generator.gen_end_game_item(room.center)
            else:
                generator.gen_stairs(room.center, downwards=True)


        how_much_to_place(room_size,room)
        #x = tcod.random_get_int(None, room.left + 1, room.right - 1)
        #y = tcod.random_get_int(None, room.top + 1, room.bottom - 1)

        #generator.amount_to_gen(room_size)

        #generator.gen_enemy((x, y))

        #x = tcod.random_get_int(None, room.left + 1, room.right - 1)
        #y = tcod.random_get_int(None, room.top + 1, room.bottom - 1)

        #if x and y != room_center:
            #generator.gen_item((x, y))


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
        config.FOV_MAP.compute_fov(config.PLAYER.x, config.PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
                                   constants.FOV_ALGO)


def objects_at_coords(coords_x, coords_y):
    object_options = [obj for obj in config.GAME.current_objects
                      if obj.x == coords_x and obj.y == coords_y]

    return object_options


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


def how_much_to_place(room_size,room):

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

        generator.what_to_gen((x,y))


def is_explored(x, y):
    return config.GAME.current_map[x][y].explored


#def auto_explore():

    #if room.center in room_list is not is_explored():

        # find a path from current position to any unexplored center of every room
        # tcod.get_path(PLAYER.x, PLAYER.y, room.center)

        # Actually move the player there

        # Stop if the player encounters a enemy (or item) for example it could stop if something from the actor class is drawn that the player can define.