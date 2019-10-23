import pygame

import config
import constants
from numpy import sign


class Camera:


    map_cell_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    map_cell_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    def __init__(self):
        self._rect = pygame.Rect(0, 0, constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT)




    def update(self):
        self.x = self.scrolling_map(config.PLAYER.x * constants.CELL_WIDTH, constants.CAMERA_WIDTH /2, constants.CAMERA_WIDTH  , constants.MAP_WIDTH * constants.CELL_WIDTH)
        self.y = self.scrolling_map(config.PLAYER.y * constants.CELL_HEIGHT, constants.CAMERA_HEIGHT /2, constants.CAMERA_HEIGHT, constants.MAP_HEIGHT * constants.CELL_HEIGHT)

    @property
    def x(self):
        return self._rect.left

    @property
    def y(self):
        return self._rect.top

    @x.setter
    def x(self, val):
        self._rect.left = val

    @y.setter
    def y(self, val):
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
            return max(p - (m-hs),0)
        else:
            return max(p - hs,0)

    @property
    def rect(self):
        return self._rect

    @property
    def map_address(self):
        x,y = self.rect.center
        map_x = x / constants.CELL_WIDTH
        map_y = y / constants.CELL_HEIGHT

        return map_x, map_y

    def win_to_map(self, coords):
        tar_x, tar_y = coords

        # convert window coords to distance from camera
        cam_d_x, cam_d_y = self.cam_dist((tar_x, tar_y))

        # distance from cam -> map cords
        map_p_x = self.x + cam_d_x
        map_p_y = self.y + cam_d_y

        return map_p_x, map_p_y

    def map_dist(self, coords):
        new_x, new_y = coords

        dist_x = new_x - self.x
        dist_y = new_y - self.y

        return dist_x, dist_y

    def cam_dist(self, coords):
        win_x, win_y = coords

        dist_x = win_x - (self.rect.width / 2)
        dist_y = win_y - (self.rect.height / 2)

        return dist_x, dist_y

