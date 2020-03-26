from dataclasses import dataclass
from enum import Enum, auto


class AiType(Enum):
    AI_FLEE = auto()
    AI_CHASE = auto()
    AI_CONFUSE = auto()


@dataclass
class Ai:
    """ component holds the AI of an entity"""
    type: AiType
    args = None  # for arguments to the AI type (e.g. AI_CHASE who is the AI chasing?)
