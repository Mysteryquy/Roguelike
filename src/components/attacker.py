from dataclasses import dataclass
from enum import Enum



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
