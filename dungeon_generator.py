import map as mp
import numpy as np
import random
import pygame
import render
from time import sleep
import config

"""
This is basically a Python version of Bob Nystrom's Dungeon Generator written in Dart.
See https://github.com/munificent/hauberk/ for his project and source code 
"""

class DungeonGenerator:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self):
        self.num_room_tries = 50
        self.extra_connector_chance = 3
        self.room_extra_size = 0
        self.winding_percent = 70
        self.rooms = []
        self.regions = []
        self.current_region = 0
        self.current_map = None
        self.current_map_width = 0
        self.current_map_height = 0

    def generate(self, map_width, map_height):
        self.current_map = [[mp.Tile(True, "S_WALL") for y in range(0, map_height)] for x in range(0, map_width)]
        self.regions = np.zeros((map_width, map_height))
        self.current_map_width = map_width
        self.current_map_height = map_height
        self.add_rooms()
        for y in range(1, self.current_map_height, 2):
            for x in range(1, self.current_map_width, 2):
                if self.current_map[x][y].block_path:
                    self.grow_maze(x, y)

        self.connect_regions()
        self.remove_dead_ends()
        mp.make_fov(self.current_map)
        return self.current_map, self.rooms

    def start_region(self):
        self.current_region = self.current_region + 1

    def carve_single(self, pos, tile):
        x, y = pos
        self.current_map[x][y].block_path = False
        self.current_map[x][y].texture = tile
        self.regions[x][y] = self.current_region

    def carve(self, rect, tile):
        for y in range(rect.height):
            for x in range(rect.width):
                self.current_map[x + rect.left][y + rect.top].block_path = False
                self.current_map[x + rect.left][y + rect.top].texture = tile
                self.regions[x + rect.left][y + rect.top] = self.current_region

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

            x = random.randint(1, int((self.current_map_width - width - 1) / 2)) * 2 + 1
            y = random.randint(1, int((self.current_map_height - height - 1) / 2)) * 2 + 1

            room = pygame.Rect(x, y, width, height)

            overlaps = room.collidelist(self.rooms) != -1

            if not overlaps:
                self.rooms.append(room)
                self.start_region()
                self.carve(room, "S_FLOOR")

    def grow_maze(self, x, y):
        cells = []
        last_dir = None
        self.start_region()
        start = (x, y)
        self.carve_single(start, "S_FLOOR")
        cells.append(start)

        while len(cells) > 0:
            cell = cells[-1]
            unmade_cells = []
            for dir in DungeonGenerator.directions:
                if self.can_carve(cell, dir):
                    unmade_cells.append(dir)

            if len(unmade_cells) > 0:
                if last_dir in unmade_cells and random.randint(0, 100) > self.winding_percent:
                    direction = last_dir
                else:
                    direction = random.choice(unmade_cells)
                c_x, c_y = cell
                d_x, d_y = direction
                double_tmp = (c_x + d_x * 2, c_y + d_y * 2)
                self.carve_single((c_x + d_x, c_y + d_y), "S_FLOOR")
                self.carve_single(double_tmp, "S_FLOOR")
                cells.append(double_tmp)
                last_dir = direction
            else:
                del cells[-1]
                last_dir = None

    def can_carve(self, pos, direction):
        x, y = pos
        di_x, di_y = direction
        if x + di_x * 3 >= self.current_map_width - 1 or x + di_x * 3 <= 0:
            return False
        elif y + di_y * 3 >= self.current_map_height - 1 or y + di_y * 3 <= 0:
            return False
        return self.current_map[x + di_x * 2][y + di_y * 2].block_path

    def connect_regions(self):
        for i,room in enumerate(self.rooms):
            x,y = room.center
            print("Raum"+ str(i) + " :"+ str(self.regions[x][y]))
        connector_regions = {}
        for y in range(0, self.current_map_height - 1):
            for x in range(0, self.current_map_width - 1):
                if self.current_map[x][y].block_path:
                    regions = set()
                    for direction in DungeonGenerator.directions:
                        dx, dy = direction
                        region = self.regions[x + dx][y + dy]
                        if region != 0:
                            regions.add(region)
                    if len(regions) >= 2:
                        connector_regions[(x, y)] = regions

        connectors = list(connector_regions)
        print("Connectors:" + str(connectors))
        merged = {}
        open_regions = set()
        for i in range(1, self.current_region + 1):
            merged[i] = i
            open_regions.add(i)

        print(open_regions)
        while len(open_regions) > 1:
            # connector = random.choice(connectors)
            connector = random.choice(connectors)
            self.add_junction(connector)

            regions = map(lambda i: merged[i], connector_regions[connector])
            dest = next(regions)
            sources = set(regions)
            if dest in sources:
                sources.remove(dest)


            for i in range(1, self.current_region + 1):
                if merged[i] in sources:
                    merged[i] = dest

            for source in sources:
                if source in open_regions:
                    open_regions.remove(source)

            for conn in connectors:
                c_x, c_y = conn
                x, y = connector
                regions = set(map(lambda reg: merged[reg], connector_regions[(c_x, c_y)]))

                if abs(c_x - x) < 2 and abs(c_y - y) < 2:
                    connectors.remove(conn)
                    continue

                if len(regions) > 1:
                    continue

                if random.randint(1, 100) < self.extra_connector_chance:
                    self.add_junction(conn)

                if conn in connectors:
                    connectors.remove(conn)

    def add_junction(self, pos):
        x, y = pos
        self.current_map[x][y].block_path = False
        self.current_map[x][y].texture = "S_FLOOR"

    def remove_dead_ends(self):
        done = False
        while not done:
            done = True
            for y in range(1, self.current_map_width):
                for x in range(1, self.current_map_height):
                    if not self.current_map[x][y].block_path:
                        exits = 0
                        for direction in DungeonGenerator.directions:
                            dx, dy = direction
                            if not self.current_map[x + dx][y + dy].block_path:
                                exits = exits + 1

                        if exits == 1:
                            done = False
                            self.current_map[x][y].block_path = True
                            self.current_map[x][y].texture = "S_WALL"
