from dataclasses import dataclass
from typing import Tuple

from container import Container


@dataclass
class Item:
    weight: float
    volume: float
    value: Tuple[int, int, int] = (0, 0, 0)  # gold, silver, copper
    container: Container = None
