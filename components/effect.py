from dataclasses import dataclass
from typing import Dict

import config
from creature import Status


@dataclass
class Effect:
    duration: int
    start_turn: int = config.ROUND_COUNTER


class OnHitEffect:
    apply_attacked: Effect
    apply_attacker: Effect


class StatusEffect:
    stat_dict: Dict[Status, int] = None


