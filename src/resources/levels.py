from enum import Enum
from typing import Dict, List


class Levels(Enum):
    WATER1 = 0
    DUNGEON1 = 1
    DUNGEON2 = 2

    def __str__(self):
        if self == Levels.WATER1:
            return "Water Dungeon"
        elif self == Levels.DUNGEON1:
            return "Deepest Dungeon 1"
        elif self == Levels.DUNGEON2:
            return "Deepest Dungeon 2"


successor_levels: Dict[Levels, List[Levels]] = {
    Levels.WATER1: [Levels.DUNGEON1],
    Levels.DUNGEON1: [Levels.DUNGEON2],
    Levels.DUNGEON2: []
}

predecessor_levels: Dict[Levels, List[Levels]] = {
    Levels.WATER1: [],
    Levels.DUNGEON1: [Levels.WATER1],
    Levels.DUNGEON2: [Levels.DUNGEON1]
}

