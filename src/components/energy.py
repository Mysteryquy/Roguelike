from dataclasses import dataclass


@dataclass
class Energy:
    energy: int
    increment: int = 100
    max_energy: int = 100
