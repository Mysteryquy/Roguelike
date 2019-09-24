import map
import numpy as np
import random
import pygame


class DungeonGenerator:
    def __init__(self):
        self.num_room_tries = 200
        self.extra_connector_chance = 20
        self.room_extra_size = 0
        self.winding_percent = 0
        self.rooms = []
        self.regions = []
        self.current_region = 1
        self.map = None
        self.map_width = 0
        self.map_height = 0

    def generate(self, map_width, map_height):
        self.map = [[map.Tile(True, "S_WALL") for y in range(0, map_height)] for x in range(0, map_width)]
        self.regions = np.zeros((map_width, map_height))
        self.map_width = map_width - 1
        self.map_height = map_height - 1
        self.add_rooms()
        map.make_fov(self.map)
        print(self.map)
        return self.map, self.rooms

    def start_region(self):
        self.current_region = self.current_region + 1

    def carve(self, rect, tile):
        for y in range(rect.height):
            for x in range(rect.width):
                self.map[x + rect.left][y + rect.top].block_path = False
                self.map[x + rect.left][y + rect.top].texture = tile

    def add_rooms(self):
        for i in range(self.num_room_tries):
            size = random.randint(1, 3 + self.room_extra_size) * 2 + 1
            rectangularity = random.randint(0, int(1 + size / 2)) * 2
            width = size
            height = size
            if random.randint(1, 3) == 1:
                width += rectangularity
            else:
                height += rectangularity

            x = random.randint(1, int((self.map_width - width - 1) / 2)) * 2 + 1
            y = random.randint(1, int((self.map_height - height - 1) / 2)) * 2 + 1

            room = pygame.Rect(x, y, width, height)

            overlaps = room.collidelist(self.rooms) != -1

            if not overlaps:
                self.rooms.append(room)
                self.start_region()
                self.carve(room, "S_FLOOR")
