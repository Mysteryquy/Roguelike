from collections import Callable
from enum import Enum
from typing import Any, Dict

from src import casting


class Spells(Enum):
    Heal = 0


spell_dict = \
    {
        Spells.Heal: casting.cast_heal

    }

spell_targeting_dict = \
    {
        Spells.Heal: None
    }
