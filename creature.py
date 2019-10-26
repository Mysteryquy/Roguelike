import pygame
import tcod

import config
import constants
import game_map
from enum import Enum



class Creature:

    class CreatureAlignment(Enum):
        FRIEND = 1
        NEUTRAL = 2
        FOE = 3
        PLAYER = 4


        @classmethod
        def can_bump(cls, c1, c2):
            if c1.alignment == cls.FRIEND:
                return c2.alignment == cls.FOE
            elif c1.alignment == cls.FOE:
                return c2.alignment == cls.FRIEND or c2.alignment == cls.PLAYER
            elif c1.alignment == cls.PLAYER:
                return c2.alignment == cls.FOE




    def __init__(self, name_instance: str, base_atk: int = 2, base_def: int = 0, hp: int = 10, base_hit_chance: int = 70,
                 base_evasion: int = 0, level: int = 1, xp_gained: int = 0, current_xp: int = 0, custom_death=None, death_text=" died horribly",
                 dead_animation_key=None, max_mana: int = 100, current_mana: int = 10, alignment: CreatureAlignment = CreatureAlignment.FOE,
                 strength = 0,
                 dexterity = 0,
                 intelligence = 0
                 ):
        self._intelligence = 0
        self._strength = 0
        self._dexterity = 0
        self.name_instance = name_instance
        self.base_atk = base_atk
        self.base_def = base_def
        self.maxhp = hp
        self.hp = hp
        self.base_hit_chance = base_hit_chance
        self.base_evasion = base_evasion
        self.level = level
        self.xp_gained = xp_gained
        self.current_xp = current_xp
        self.owner = None
        self.alignment = alignment
        self.custom_death = custom_death
        self.death_text = death_text
        self.dead_animation_key = dead_animation_key
        self.max_mana = max_mana
        self.current_mana = current_mana

        self.intelligence = intelligence
        self.dexterity = dexterity
        self.strength = strength


    @property
    def dexterity(self):
        return self._dexterity

    @dexterity.setter
    def dexterity(self, value):
        self._dexterity = value
        self.base_evasion += value*2
        self.base_hit_chance += value*2
        #rechne rest...

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        self._strength = value
        self.base_atk += value
        #rechne rest aus

    @property
    def intelligence(self):
        return self._intelligence


    @intelligence.setter
    def intelligence(self, value):
        self._intelligence = value
        self.max_mana += value*2
        #rechne rest...





    def is_foe(self):
        return self.alignment == Creature.CreatureAlignment.FOE

    def move(self, dx, dy):

        tile_is_wall = not config.FOV_MAP.walkable[self.owner.y + dy, self.owner.x + dx]

        target = game_map.check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target and Creature.CreatureAlignment.can_bump(self, target.creature) :
            # im Tuturial ist das print unten rot aber anscheined geht es trotzdem
            self.attack_new(target)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack_new(self, target):

        chance_to_hit = self.base_hit_chance - target.creature.base_evasion

        if (chance_to_hit + tcod.random_get_int(None, 1, 100)) >= 100:
            self.attack(target)
        else:
            config.GAME.game_message(self.name_instance + " misses " + target.creature.name_instance)

    def attack(self, target):

        damage_dealt = self.power - target.creature.defense

        config.GAME.game_message(
            self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage_dealt) + " damage!",
            constants.COLOR_WHITE)
        target.creature.take_damage(damage_dealt, self)

        if damage_dealt > 0 and self.owner is config.PLAYER:
            pygame.mixer.Sound.play(config.RANDOM_ENGINE.choice(config.ASSETS.snd_list_hit))

    def take_damage(self, damage, attacker):
        self.hp -= damage
        config.GAME.game_message(self.name_instance + "`s health is " + str(self.hp) + "/" + str(self.maxhp),
                                 constants.COLOR_RED)

        if self.hp <= 0:
            self.death(attacker)

    def heal(self, value):

        self.hp = self.hp + value
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_xp(self, xp):
        self.current_xp = self.current_xp + xp
        if self.level is not constants.MAX_LEVEL:
            xp_needed = constants.XP_NEEDED[self.level]
            if self.current_xp >= xp_needed:
                self.level_up()

    def level_up(self):
        self.level = self.level + 1
        config.GAME.game_message(self.name_instance + " leveled up! He/She/It is now Level " + str(self.level),
                                 msg_color=constants.COLOR_GREEN)
        # Here comes the things we eventually add upon level up

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

    def death(self, killer):
        if self.death_text:
            config.GAME.game_message(self.name_instance + self.death_text,
                                     constants.COLOR_GREY)
        # print (monster.creature.name_instance + " is slaughtered into ugly bits of flesh!")
        if self.dead_animation_key:
            self.owner.set_animation(self.dead_animation_key)
        killer.get_xp(self.xp_gained)
        self.owner.depth = constants.DEPTH_CORPSE
        if self.custom_death:
            self.custom_death(self, killer)

        self.owner.is_corpse = True

        self.owner.destroy()
