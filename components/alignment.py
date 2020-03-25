from dataclasses import dataclass
from enum import Enum


class CreatureAlignment(Enum):
    FRIEND = 1
    NEUTRAL = 2
    FOE = 3
    PLAYER = 4

    @classmethod
    def can_bump(cls, c1, c2):
        if c1.alignment == cls.FRIEND:
            return c2.alignment == cls.FOE
        elif c1.alignment == cls.FOE:
            return c2.alignment == cls.FRIEND or c2.alignment == cls.PLAYER
        elif c1.alignment == cls.PLAYER:
            return c2.alignment == cls.FOE

    @classmethod
    def can_swap(cls, c1, c2):
        return c1.alignment == cls.PLAYER and c2.alignment == cls.FRIEND


@dataclass
class Alignment:
    alignment: CreatureAlignment
