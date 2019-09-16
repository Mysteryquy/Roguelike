import tcod
import constants
import config
import map
import tcod

import config
import constants
import map


class AiConfuse:

    def __init__(self, old_ai, num_turns):
        self.owner = None
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:
            self.owner.creature.move(tcod.random_get_int(None, -1, 1), tcod.random_get_int(None, -1, 1))

            self.num_turns -= 1

        else:
            self.owner.ai = self.old_ai

            config.GAME.game_message(self.owner.display_name + " has broken free!", constants.COLOR_GREEN)


class AiChase:
    # A basic AI which chases the player and tries to bump into him
    # TODO Let the creature move around walls
    def __init__(self):
        self.owner = None

    def take_turn(self):
        monster = self.owner
        x,y = monster.x, monster.y
        if map.is_visible(x,y):
            player_x, player_y = config.PLAYER.x, config.PLAYER.y
            dx = player_x - x
            dy = player_y - y
            if dx > 0 and map.is_walkable(x+1,y):
                monster.move(1,0)
            elif dx < 0 and map.is_walkable(x-1,y):
                monster.move(-1,0)
            elif dy > 0 and map.is_walkable(x,y+1):
                monster.move(0,1)
            elif dy < 0 and map.is_walkable(x,y-1):
                monster.move(0,-1)


class AiFlee:

    def __init__(self):
        self.owner = None

    def take_turn(self):
        monster = self.owner
        x, y = monster.x, monster.y
        if map.is_visible(x, y):
            player_x, player_y = config.PLAYER.x, config.PLAYER.y
            dx = player_x - x
            dy = player_y - y

            if dx > 0 and map.is_walkable(x - 1, y):
                monster.move(-1, 0)
            elif dx < 0 and map.is_walkable(x + 1, y):
                monster.move(1, 0)
            elif dy > 0 and map.is_walkable(x, y - 1):
                monster.move(0, -1)
            elif dy < 0 and map.is_walkable(x, y + 1):
                monster.move(0, 1)
