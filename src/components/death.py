from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Death:
    """ component for an entity that may die """
    killer: int = None
    animation_key: str = None  # signals whether the entity should remain on the ground or be deleted
    custom_death: Callable[[int, int], Any] = None


@dataclass
class Dead:
    """ component for dead entity """
    pass