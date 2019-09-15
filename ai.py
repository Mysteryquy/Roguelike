import tcod.path as path
import tcod
import constants
import config
import map

class ai_Confuse:

    def __init__(self, old_ai, num_turns):

        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:
            self.owner.creature.move(tcod.random_get_int(None, -1, 1), tcod.random_get_int(None, -1, 1))

            self.num_turns -= 1

        else:
            self.owner.ai = self.old_ai

            config.GAME.game_message(self.owner.display_name + " has broken free!", constants.COLOR_GREEN)


class ai_Chase:
    # A basic AI which chases the player and tries to bump into him
    # TODO Let the creature move around walls


    def take_turn(self):
        """
        monster = self.owner

        # if tcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):

        if map.is_visible(monster.x, monster.y):
            # Move to the player if far away
            if monster.distance_to(config.PLAYER) >= 2:

                self.owner.move_towards(config.PLAYER)

            # if close enough, attack player
            elif config.PLAYER.creature.hp > 0:
                monster.creature.attack(config.PLAYER)
        """
        monster = self.owner
        if map.is_visible(monster.x,monster.y):
            pathing = map.get_path(monster.x, monster.y, config.PLAYER.x, config.PLAYER.y)

            if pathing:
                print(pathing)
                x,y = pathing[0]

                monster.move(x-monster.x,y-monster.y)


class ai_Flee:

    def take_turn(self):
        monster = self.owner

        if tcod.map_is_in_fov(config.FOV_MAP, monster.x, monster.y):
            self.owner.move_away(config.PLAYER)