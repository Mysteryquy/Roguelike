from dataclasses import dataclass
from enum import Enum, auto


class EquipSlots(Enum):
    ACCESSORY = auto()
    ARMOR = auto()
    HELMET = auto()
    WEAPON = auto()
    SHIELD = auto()


@dataclass
class Equipment:
    equip_slot: EquipSlots
