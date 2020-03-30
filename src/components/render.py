from dataclasses import dataclass

from src import config
from src.assets import Assets


@dataclass
class Renderable:
    """ component for an entity that can be rendered and has an animation """
    animation_key: str
    animation_speed: float = 1.0
    depth: int = 0
    flicker_speed: float = 1.0
    flicker_timer: float = 0.0
    sprite_image: int = 0
    draw_explored: bool = False
