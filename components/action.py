from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class Actions(Enum):
    MOVE = auto()
    ATTACK = auto()
    USE = auto()
    # TODO add everything else

@dataclass
class Action:
    action: Actions
    args: Any  # used for arguments to the action. E.g. (dx,dy) for movement

