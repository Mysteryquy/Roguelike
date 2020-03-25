from dataclasses import dataclass


@dataclass
class Position:
    """ Component that holds the position of an entity """
    x: int
    y: int
