from dataclasses import dataclass


@dataclass
class Stairs:
    """ indicate an entity that is staircase """
    leads_to: str
    downwards: bool
