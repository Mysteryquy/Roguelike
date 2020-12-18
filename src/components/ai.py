from dataclasses import dataclass
from enum import Enum, auto

from src.components.position import Position


class AiType(Enum):
    AI_FLEE = auto()
    AI_CHASE = auto()
    AI_CONFUSE = auto()


@dataclass
class Ai:
    """ component for entity that has an ai """


@dataclass
class AiFlee(Ai):
    target: Position
    act_unseen: bool = False


@dataclass
class AiChase(Ai):
    target: Position
    act_unseen: bool = False


@dataclass
class AiConfuse(Ai):
    duration: int
    old_ai: Ai
    act_unseen: bool = True
