from dataclasses import dataclass


@dataclass
class Position:
    """ Component that holds the position of an entity """
    x: int
    y: int

    def __eq__(self, other):
        if type(other) != Position:
            return False
        return other.x == self.x and other.y == self.y
