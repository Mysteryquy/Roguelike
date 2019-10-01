from __future__ import annotations

from typing import Optional
import math

import config
import constants
import game_map
from ai import Ai
from container import Container
from equipment import Equipment
from item import Item
from structure import Structure


class Actor:

    def __init__(self, x: int, y: int, name_object: str, animation_key: str,
                 animation_speed: float = 1.0, depth: int = 0,
                 creature=None, ai: Optional[Ai] = None, container: Optional[Container] = None,
                 item: Optional[Item] = None, equipment: Optional[Equipment] = None,
                 state: Optional[str] = None, structure: Optional[Structure] =None,
                 draw_explored: bool = False):
        self.x = round(x)
        self.y = round(y)
        self.name_object = name_object
        self.animation_key = animation_key
        self.animation = config.ASSETS.animation_dict[self.animation_key]  # number of images
        self.animation_speed = animation_speed / 1.0  # in seconds
        self.depth = depth

        self.draw_explored = draw_explored

        # animation flicker speed
        self.flicker_speed = self.animation_speed / len(self.animation)
        self.flicker_timer = 0.0
        self.sprite_image = 0  # s

        self.creature = creature
        if self.creature:
            self.creature.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:
            self.container.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

        self.structure = structure
        if self.structure:
            self.structure.owner = self


        self.state = state
        if self.state:
            self.state.owner = self



    @property
    def display_name(self):

        if self.creature:
            return self.creature.name_instance + " the " + self.name_object

        if self.item:
            if self.equipment and self.equipment.equipped:
                return self.name_object + "(equipped)"
            else:
                return self.name_object

    def draw(self):
        is_visible = config.FOV_MAP.fov[self.y, self.x]

        explored_draw = self.draw_explored and game_map.is_explored(self.x, self.y) and not is_visible
        special_flags = constants.EXPLORED_DRAW_FLAGS if explored_draw else 0

        if is_visible or explored_draw:
            if len(self.animation) == 1:
                config.SURFACE_MAP.blit(self.animation[0],
                                        (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT),
                                        special_flags=special_flags)

            elif len(self.animation) > 1:
                if config.CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1 / config.CLOCK.get_fps()

                if self.flicker_timer >= self.flicker_speed:
                    self.flicker_timer = 0.0

                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0

                    else:
                        self.sprite_image += 1

                config.SURFACE_MAP.blit(self.animation[self.sprite_image],
                                        (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT),
                                        special_flags=special_flags)

    def distance_to(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def move_towards(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)

    def move_towards_point(self, x, y):
        dx = x - self.x
        dy = y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)

    def move(self, dx, dy):
        self.creature.move(dx, dy)

    def move_away(self, other):

        dx = self.x - other.x
        dy = self.y - other.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)

    def animation_destroy(self):

        self.animation = None

    def animation_init(self):

        self.animation = config.ASSETS.animation_dict[self.animation_key]  # number of images

    def destroy(self):
        self.creature = None
        self.ai = None

    def set_animation(self, new_key):
        self.animation_key = new_key
        self.animation = config.ASSETS.animation_dict[self.animation_key]


