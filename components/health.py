from dataclasses import dataclass


@dataclass
class Health:
    def __init__(self, max_health: int):
        self.max_health: int = max_health
        self.current_health: int = self.max_health
