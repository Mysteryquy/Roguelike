from dataclasses import dataclass


@dataclass
class StaticRenderable:
    """ component for an entity that can be rendered but has no animation """
    texture: str
    depth: int = 0
    x: int = -1  # only used if the entity does not have a Position component
    y: int = -1


@dataclass
class DynamicRenderable:
    """ component for an entity that can be rendered and has an animation """
    animation_key: str
    animation_speed: float = 1.0
    depth: int = 0
    flicker_speed: float = 1.0
    flicker_timer: float = 0.0
    sprite_image: int = 0



