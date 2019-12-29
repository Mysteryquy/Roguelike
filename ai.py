# coding=utf-8
from abc import ABC, abstractmethod

import tcod

import casting
import config
import constants
import game_map


class Ai(ABC):
    def __init__(self):
        self.owner = None
        super().__init__()

    @abstractmethod
    def take_turn(self) -> None:
        """
        method where the AI takes its turn
        """
        pass


class AiConfuse(Ai):
    """
    AI that is moving randomly
    """

    def __init__(self, old_ai: Ai, num_turns: int):
        super().__init__()
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self) -> None:
        if self.num_turns > 0:
            self.owner.creature.move(tcod.random_get_int(None, -1, 1), tcod.random_get_int(None, -1, 1))

            self.num_turns -= 1

        else:
            self.owner.ai = self.old_ai

            config.GAME.game_message(self.owner.display_name + " has broken free!", constants.COLOR_GREEN)


class AiChase(Ai):
    """
    This AI chases and bumps into the player
    """

    def __init__(self):
        super().__init__()

    def take_turn(self) -> None:
        """
        this ai takes its turn by chasing the player if he is in vision
        """
        monster = self.owner
        x, y = monster.x, monster.y
        if game_map.is_visible(x, y):
            path = iter(game_map.get_path_to_player(x, y))
            next_x, next_y = next(path, (0, 0))
            monster.move(next_x - x, next_y - y)


class AiFlee(Ai):
    """
    This AI flees from the player
    """

    def __init__(self):
        super().__init__()

    def take_turn(self):
        """
        if visible this ai tries to increase the distance between the player and itself
        """
        """
        monster = self.owner
        x, y = monster.x, monster.y
        if game_map.is_visible(x, y):
            player_x, player_y = config.PLAYER.x, config.PLAYER.y
            dx = player_x - x
            dy = player_y - y

            if dx > 0 and game_map.is_walkable(x - 1, y):
                monster.move(-1, 0)
            elif dx < 0 and game_map.is_walkable(x + 1, y):
                monster.move(1, 0)
            elif dy > 0 and game_map.is_walkable(x, y - 1):
                monster.move(0, -1)
            elif dy < 0 and game_map.is_walkable(x, y + 1):
                monster.move(0, 1)
            elif dx == 0 and dy != 0 and game_map.is_walkable(x + 1, y):
                monster.move(1, 0)
            elif dx == 0 and dy != 0 and game_map.is_walkable(x - 1, y):
                monster.move(-1, 0)
            elif dy == 0 and dx != 0 and game_map.is_walkable(x, y + 1):
                monster.move(0, 1)
            elif dy == 0 and dx != 0 and game_map.is_walkable(x, y - 1):
                monster.move(0, -1)
        """


class AiCaster(Ai):

    def __init__(self):
        super().__init__()
        self.owner = None

    def take_turn(self):
        monster = self.owner
        x, y = monster.x, monster.y
        if game_map.is_visible(x, y):
            player_x, player_y = config.PLAYER.x, config.PLAYER.y
            print(monster)
            casting.cast_lightning(monster, (1, 3), (player_x, player_y))


class AiFriend(Ai):

    def __init__(self):
        super().__init__()
        self.owner = None

    def take_turn(self):
        monster = self.owner
        x, y = monster.x, monster.y
