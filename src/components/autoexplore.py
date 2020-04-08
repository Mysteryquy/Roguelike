from dataclasses import dataclass
from typing import List, Tuple, Iterable


@dataclass
class AutoExploring:
    path: Iterable[Tuple[int, int]]
    continue_after_goal: bool = False
    force_one_move: bool = False
    pass
