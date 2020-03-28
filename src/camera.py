import pygame

from src import constants
from typing import Tuple


class Camera:
    """
    Class for the camera

    """
    map_cell_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    map_cell_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    def __init__(self):
        self._rect = pygame.Rect(0, 0, constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT)

    def update(self, player_x, player_y):
        self.x = Camera.scrolling_map(player_x * constants.CELL_WIDTH, constants.CAMERA_WIDTH / 2,
                                      constants.CAMERA_WIDTH, constants.MAP_WIDTH * constants.CELL_WIDTH)
        self.y = Camera.scrolling_map(player_y* constants.CELL_HEIGHT, constants.CAMERA_HEIGHT / 2,
                                      constants.CAMERA_HEIGHT, constants.MAP_HEIGHT * constants.CELL_HEIGHT)

    @property
    def pos(self) -> Tuple[int, int]:
        """
        gives the position of the camera
        :return: the position of the camera
        """
        return self.x, self.y

    @property
    def x(self) -> int:
        """
        :return: the x coordinate of the position of the camera
        """
        return self._rect.left

    @property
    def y(self) -> int:
        """

        :return: the y corrdinate of the position of the camera
        """
        return self._rect.top

    @x.setter
    def x(self, val: int) -> None:
        self._rect.left = val

    @y.setter
    def y(self, val: int) -> None:
        self._rect.top = val

    @staticmethod
    def scrolling_map(p, hs, s, m):
        """
        Get the position of the camera in a scrolling map:

         - p is the position of the player.
         - hs is half of the screen size, and s is the full screen size.
         - m is the size of the map.
        """
        if p < hs:
            return 0
        elif p >= m - hs:
            return max(m - s, 0)
        else:
            return max(p - hs, 0)

    @property
    def rect(self) -> pygame.rect.Rect:
        """

        :return: the underlying rectangle of the camera
        """
        return self._rect

    @property
    def cam_map_coord(self) -> Tuple[int, int]:
        """
        gives the coordinate on the map of the topleft of the map
        :return: map coordinate of topleft
        """
        return int(self.x / constants.CELL_WIDTH), int(self.y / constants.CELL_HEIGHT)

    def coords_from_position(self, x: int, y: int) -> Tuple[int, int]:
        """
        gives the coordinate from a given position on the screen
        :param x: x part of position
        :param y: y part of position
        :return: corresponding coordinate on the map
        """
        n_x, n_y = x + self.x, y + self.y
        map_x, map_y = int(n_x / constants.CELL_WIDTH), int(n_y / constants.CELL_HEIGHT)
        return map_x, map_y

    def position_from_coords(self, x: int, y: int) -> Tuple[int, int]:
        """
        gives the screen position of the given coordinate (topleft corner of the coordinate)
        :param x: x part of coordinate
        :param y: y part of coordinate
        :return: topleft corner of corresponding position on the screen
        """
        n_x, n_y = x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT
        return n_x - self.x, n_y - self.y
