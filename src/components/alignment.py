from dataclasses import dataclass
from enum import Enum


class CreatureAlignment(Enum):
    FRIEND = 1
    NEUTRAL = 2
    FOE = 3
    PLAYER = 4

    @classmethod
    def can_bump(cls, a1, a2):
        if a1 == cls.FRIEND:
            return a2 == cls.FOE
        elif a1 == cls.FOE:
            return a2 == cls.FRIEND or a2 == cls.PLAYER
        elif a1 == cls.PLAYER:
            return a2 == cls.FOE

    @classmethod
    def can_swap(cls, a1, a2):
        return a1 == cls.PLAYER and a2 == cls.FRIEND


@dataclass
class Alignment:
    alignment: CreatureAlignment
