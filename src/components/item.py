from dataclasses import dataclass
from typing import Tuple

from src.components.container import Container


@dataclass
class Item:
    weight: float
    volume: float
    container: Container = None
