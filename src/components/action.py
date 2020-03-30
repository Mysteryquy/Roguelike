from dataclasses import dataclass

from src.components.item import Item


@dataclass
class HasAction:
    """ component of an entity which has an action this turn """
    pass


@dataclass
class Action:
    pass


@dataclass
class MovementAction(Action):
    dx: int
    dy: int


@dataclass
class PickUpAction(Action):
    pass


@dataclass
class DropAction(Action):
    item: Item = None  # if a specific item should be dropped, else drop the last element in the inventory


@dataclass
class UseStairsAction(Action):
    pass


@dataclass
class MeleeAttackAction(Action):
    target: int


@dataclass
class StartAutoexploreAction(Action):
    pass
