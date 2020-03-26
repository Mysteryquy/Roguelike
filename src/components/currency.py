from dataclasses import dataclass
from enum import Enum, auto


class Currencies(Enum):
    GOLD = auto()
    SILVER = auto()
    COPPER = auto()

    @classmethod
    def convert_to(cls):
        # TODO implement this shit?
        pass


@dataclass
class Currency:
    """ indicate a component of an entity that """
    type: Currencies
    amount: float # maybe int instead???
