from dataclasses import dataclass
from typing import Any


@dataclass
class Death:
    """ component for an entity that may die """
    custom_death: Any = None
