from dataclasses import dataclass


@dataclass
class Attacker:
    attack: int
    defense: int
    hit_chance: float
    evasion_chance: float
