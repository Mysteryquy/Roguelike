from dataclasses import dataclass
from typing import List, Tuple, Iterable


@dataclass
class AutoExploring:
    path: Iterable[Tuple[int, int]]
    stairs_goal: bool = False
    pass
