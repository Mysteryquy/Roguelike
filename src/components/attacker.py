from dataclasses import dataclass
from enum import Enum

import math


@dataclass
class Attacker:
    attack: int
    defense: int
    hit_chance: float
    evasion_chance: float


class DamageType(Enum):
    Physical = 0
    Fire = 1


@dataclass
class DealDamageEvent:
    damage: int
    type: DamageType = DamageType.Physical


@dataclass
class AttackerBonus:
    attack: int = 0
    defense: int = 0
    hit_chance: float = 0
    evasion_chance: float = 0
    duration: int = math.inf
