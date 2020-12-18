from enum import Enum
from typing import Dict, List


class Levels(Enum):
    HELL1 = 0
    WATER1 = 1
    DUNGEON1 = 2

    def __str__(self):
        if self == Levels.WATER1:
            return "Water Dungeon"
        elif self == Levels.HELL1:
            return "Hell"
        elif self == Levels.DUNGEON1:
            return "Deepest Dungeon 1"


successor_levels: Dict[Levels, List[Levels]] = {
    Levels.HELL1: [Levels.WATER1],
    Levels.WATER1: [Levels.DUNGEON1],
    Levels.DUNGEON1: []
}

predecessor_levels: Dict[Levels, List[Levels]] = {
    Levels.HELL1: [],
    Levels.WATER1: [Levels.HELL1],
    Levels.DUNGEON1: [Levels.WATER1]
}

