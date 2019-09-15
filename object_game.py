import config
import map
import constants


class Game:
    def __init__(self):

        self.message_history = []

        self.current_objects = []

        self.maps_previous = []

        self.maps_next = []

        self.current_map, self.current_rooms = map.create()

    def transition_next(self):


        config.FOV_CALCULATE = True

        for obj in self.current_objects:
            obj.animation_destroy()

        self.maps_previous.append((config.PLAYER.x, config.PLAYER.y, self.current_map, self.current_rooms, self.current_objects))

        if len(self.maps_next) == 0:

            self.current_objects = [config.PLAYER]

            config.PLAYER.animation_init()

            self.current_map, self.current_rooms = map.create()

            map.place_objects(self.current_rooms)

        else:
            (config.PLAYER.x, config.PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_next[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map.make_fov(self.current_map)

            FOV_CALCULATE = True

            del self.maps_next[-1]

    def transition_previous(self):

        if len(self.maps_previous) != 0:

            for obj in self.current_objects:
                obj.animation_destroy()

            self.maps_next.append((config.PLAYER.x, config.PLAYER.y, self.current_map, self.current_rooms, self.current_objects))

            (config.PLAYER.x, config.PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.maps_previous[-1]

            for obj in self.current_objects:
                obj.animation_init()

            map.make_fov(self.current_map)
            config.FOV_CALCULATE = True

            del self.maps_previous[-1]
        else:
            self.game_message("There is no previous level", constants.COLOR_WHITE)

    def game_message(self, game_msg, msg_color=constants.COLOR_GREY):
        self.message_history.append((game_msg, msg_color))
