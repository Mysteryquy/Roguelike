import pygame

from src import constants
from typing import Tuple, Generator


class Camera:
    """
    Class for the camera

    """

    def __init__(self, width: int, height: int, cell_width: int, cell_height: int, map_width: int, map_height: int,
                 screen_topleft: Tuple[int, int]):
        self._rect: pygame.Rect = pygame.Rect(0, 0, width, height)
        self.cell_width: int = cell_width
        self.cell_height: int = cell_height
        self.map_width: int = map_width
        self.map_height: int = map_height
        self.display_map_w: int = int(self.width / self.cell_width)
        self.display_map_h: int = int(self.height / self.cell_height)
        self.render_rect: pygame.Rect = pygame.Rect(0, 0, self.map_width, self.map_height)
        self.screen_topleft: Tuple[int, int] = screen_topleft

    def update(self, player_x: int, player_y: int):
        self.x = Camera.scrolling_map(player_x * self.cell_width, self.width / 2,
                                      self.width, self.map_width * self.cell_width)
        self.y = Camera.scrolling_map(player_y * self.cell_height, self.height / 2,
                                      self.height, self.map_height * self.cell_height)

        self.render_rect.left = max(0, self.x - self.display_map_w)
        self.render_rect.top = max(0, self.y - self.display_map_h)
        self.render_rect.right = min(self.map_width, self.x + self.display_map_w)
        self.render_rect.bottom = min(self.map_height, self.y + self.display_map_h)

    @property
    def render_range_w(self) -> range:
        return range(self.render_rect.left, self.render_rect.right)

    @property
    def render_range_h(self) -> range:
        return range(self.render_rect.top, self.render_rect.bottom)

    @property
    def width(self) -> int:
        return self._rect.width

    @property
    def height(self) -> int:
        return self._rect.height

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
        :return: the y coordinate of the position of the camera
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
        return int(self.x / self.cell_width), int(self.y / self.cell_height)

    def coords_from_position(self, x: int, y: int) -> Tuple[int, int]:
        """
        gives the coordinate from a given position on the screen
        :param x: x part of position
        :param y: y part of position
        :return: corresponding coordinate on the map
        """
        dx, dy = self.screen_topleft
        n_x, n_y = x + self.x - dx, y + self.y - dy
        map_x, map_y = int(n_x / self.cell_width), int(n_y / self.cell_height)
        return map_x, map_y

    def position_from_coords(self, x: int, y: int) -> Tuple[int, int]:
        """
        gives the screen position of the given coordinate (topleft corner of the coordinate)
        :param x: x part of coordinate
        :param y: y part of coordinate
        :return: topleft corner of corresponding position on the screen
        """
        dx, dy = self.screen_topleft
        n_x, n_y = x * self.cell_width, y * self.cell_height
        return n_x - self.x + dx, n_y - self.y + dy
