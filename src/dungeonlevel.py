from tcod import path

from src import constants, config, esper
from src.components.position import Position
from src.dungeon_generator import DungeonGenerator


class DungeonLevel:

    def __init__(self, entities, level_name):
        self.player_x = -1
        self.player_y = -1
        gen = DungeonGenerator(level_name)
        self.map, self.rooms = gen.generate(constants.MAP_WIDTH, constants.MAP_HEIGHT)
        self.pathing = path.AStar(config.FOV_MAP, 0)
        self.auto_explore_path = None
        self.name = level_name
        self.world = esper.World()
        for components_of_entity in entities:
            self.world.create_entity(components_of_entity)  # create entity with given components

    def create_entity(self, *components):
        """
        creates an entity with the given components
        :param components: 
        :return:
        """
        self.world.create_entity(components)

    def entities_at_coords(self, x: int, y: int, *components):
        """
        gives the objects at the given coordinates (= Entities with Position component with position = (x,y)
        :param x: x position
        :param y: y position
        :param components: if you only want entities with the specific components
        :return: the wanted entities
        """
        objects = []
        for ent, pos in self.world.get_component(Position, components):
            if pos.x == x and pos.y == y:
                objects.append(ent)
        return objects

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
                self.player_x, self.player_y = x, y

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
