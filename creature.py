import config
import map
import pygame
import constants

class Creature:

    def __init__(self, name_instance, base_atk=2, base_def=0, hp=10, death_function=None):
        self.name_instance = name_instance
        self.base_atk = base_atk
        self.base_def = base_def
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):

        tile_is_wall = (config.GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = map.check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            # im Tuturial ist das print unten rot aber anscheined geht es trotzdem
            self.attack(target)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target):

        damage_dealt = self.power - target.creature.defense

        config.GAME.game_message(
            self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage_dealt) + " damage!",
            constants.COLOR_WHITE)
        target.creature.take_damage(damage_dealt)

        if damage_dealt > 0 and self.owner is config.PLAYER:
            pygame.mixer.Sound.play(config.RANDOM_ENGINE.choice(config.ASSETS.snd_list_hit))

    def take_damage(self, damage):
        self.hp -= damage
        config.GAME.game_message(self.name_instance + "`s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

        if self.hp <= 0:

            if self.death_function is not None:
                self.death_function(self.owner)

    def heal(self, value):

        self.hp = self.hp + value

        if self.hp > self.maxhp:
            self.hp = self.maxhp

    @property
    def power(self):

        total_power = self.base_atk

        if self.owner.container:
            object_bonuses = [obj.equipment.attack_bonus for obj in self.owner.container.equipped_items]

            for bonus in object_bonuses:
                if bonus:
                    total_power += bonus

        return total_power

    @property
    def defense(self):

        total_defense = self.base_def

        if self.owner.container:
            object_bonuses = [obj.equipment.defense_bonus for obj in self.owner.container.equipped_items]

            for bonus in object_bonuses:
                if bonus:
                    total_defense += bonus

        return total_defense

