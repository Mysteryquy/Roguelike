from dataclasses import dataclass

from src.resources.levels import Levels


@dataclass
class Stairs:
    """ indicate an entity that is staircase """
    leads_to: Levels
    downwards: bool
