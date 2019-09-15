import tcod
import constants
import config
import generator


class Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False


class obj_Room:
    # This is a rectangle that lives on the map

    def __init__(self, coords, size):
        self.x1, self.y1 = coords
        self.w, self.h = size

        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    @property
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2

        return center_x, center_y

    def intercept(self, other):
        # return True if other obj intersects with this one
        objects_intersect = (
                self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

        return objects_intersect


def is_visible(x, y):

    return config.FOV_MAP.fov[y, x]


def get_path(start_x,start_y,goal_x,goal_y):
    return config.GAME.pathing.get_path(start_x,start_y,goal_x,goal_y)

def create():
    new_map = [[Tile(True) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    # generate new room
    list_of_rooms = []

    for i in range(constants.MAP_MAX_NUM_ROOMS):

        w = tcod.random_get_int(None, constants.ROOM_MIN_WIDTH, constants.ROOM_MAX_WIDTH)
        h = tcod.random_get_int(None, constants.ROOM_MIN_HEIGHT, constants.ROOM_MAX_HEIGHT)
        if len(list_of_rooms) == 0:
            x = 3
            y = 2
        else:
            x = tcod.random_get_int(None, 2, constants.MAP_WIDTH - w - 2)
            y = tcod.random_get_int(None, 2, constants.MAP_HEIGHT - h - 2)

        # create the room
        new_room = obj_Room((x, y), (w, h))

        failed = False

        # TODO check for interference
        for other_room in list_of_rooms:
            if new_room.intercept(other_room):
                failed = True
                break

        if not failed:

            create_room(new_map, new_room)
            current_center = new_room.center
            (x, y) = current_center
            current_center = (int(round(x)), int(round(y)))

            if len(list_of_rooms) != 0:
                previous_center = list_of_rooms[-1].center

                (x, y) = previous_center
                previous_center = (int(round(x)), int(round(y)))
                create_tunnels(current_center, previous_center, new_map)

            list_of_rooms.append(new_room)

    make_fov(new_map)

    return new_map, list_of_rooms


def create_room(new_map, new_room):
    for x in range(new_room.x1, new_room.x2):
        for y in range(new_room.y1, new_room.y2):
            new_map[x][y].block_path = False


def place_objects(room_list):

    current_level = len(config.GAME.maps_previous) + 1

    top_level = current_level == 1
    final_level = (current_level == constants.MAP_NUM_LEVELS)

    for room in room_list:

        first_room = (room == room_list[0])
        last_room = (room == room_list[-1])

        if first_room:
            x, y = room.center
            config.PLAYER.x, config.PLAYER.y = int(x), int(y)

        if first_room and top_level:
            # print(room.center)
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

        x = tcod.random_get_int(None, room.x1 + 1, room.x2 - 1)
        y = tcod.random_get_int(None, room.y1 + 1, room.y2 - 1)

        generator.gen_enemy((x, y))

        x = tcod.random_get_int(None, room.x1 + 1, room.x2 - 1)
        y = tcod.random_get_int(None, room.y1 + 1, room.y2 - 1)

        generator.gen_item((x, y))


def create_tunnels(coords1, coords2, new_map):
    coin_flip = (tcod.random_get_int(None, 0, 1) == 1)

    (x1, y1) = coords1
    (x2, y2) = coords2

    if coin_flip:
        for x in range(min(x1, x2), max(x1, x2)):
            new_map[x][y1].block_path = False
        for y in range(min(y1, y2), max(y1, y2)):
            new_map[x2][y].block_path = False

    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            new_map[x1][y].block_path = False
        for x in range(min(x1, x2), max(x1, x2) + 1):
            new_map[x][y2].block_path = False


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
    return config.FOV_MAP.walkable[y,x]


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
