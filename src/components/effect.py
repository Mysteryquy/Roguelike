from dataclasses import dataclass
from typing import Dict

from src import config


@dataclass
class Effect:
    duration: int
    start_turn: int = config.ROUND_COUNTER


