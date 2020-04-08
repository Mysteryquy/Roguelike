import random

from src import constants
from src.components.attacker import AttackerBonus
from src.components.currency import Valuable, Gold
from src.components.equipment import Equipment, EquipSlots
from src.components.item import Item
from src.components.name import Name
from src.components.position import Position
from src.components.render import Renderable

longsword_name_dict = {
    1: "Silver Longsword",
    2: "Moonlight Sword",
    3: "Rediron Sword",
    4: "Black Sword",
    5: "Royal Sword"
}


def gen_weapon_longsword(level, coords):
    x, y = coords
    bonus = random.randint(1, 2)
    n = random.choice(list(longsword_name_dict.keys()))

    level.world.create_entity(AttackerBonus(attack=bonus),
                              Valuable(100), Item(weight=2, volume=2),
                              Equipment(equip_slot=EquipSlots.WEAPON),
                              Renderable(animation_key="S_WEP_LONGSWORD_" + str(n), depth=constants.DEPTH_ITEM, draw_explored=True),
                              Name(name=longsword_name_dict[n]), Position(x, y)
                              )


def gen_item(level, coords):
    rng = random.randint(1, 2)
    if rng == 1:
        # sword
        gen_weapon_longsword(level, coords)
    elif rng == 2:
        gen_and_append_gold(level, coords)


def gen_and_append_gold(level, coords):
    x, y = coords
    value = random.randint(1, 100)

    if value < 31:
        pic = "S_MONEY_SMALL"
    elif value < 67:
        pic = "S_MONEY_MEDIUM"
    else:
        pic = "S_MONEY_LARGE"

    level.world.create_entity(Renderable(animation_key=pic, depth=constants.DEPTH_ITEM, draw_explored=True),
                              Gold(amount=value), Position(x, y))
