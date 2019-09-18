import config
import map
import pygame
import constants
import tcod


class Creature:

    def __init__(self, name_instance, base_atk=2, base_def=0, hp=10, death_function=None, base_hit_chance=70,
                 base_evasion=0, level=1, xp_gained=0, current_xp=0, custom_death=None, death_text = " died horribly",
                 dead_animation = None,
                 dead_animation_key = None):
        self.name_instance = name_instance
        self.base_atk = base_atk
        self.base_def = base_def
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function
        self.base_hit_chance = base_hit_chance
        self.base_evasion = base_evasion
        self.level = level
        self.xp_gained = xp_gained
        self.current_xp = current_xp
        self.owner = None
        self.custom_death = custom_death
        self.death_text = death_text
        self.dead_animation = dead_animation
        self.dead_animation_key = dead_animation_key

    def move(self, dx, dy):

        tile_is_wall = not config.FOV_MAP.walkable[self.owner.y + dy, self.owner.x + dx]

        target = map.check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
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
        target.creature.take_damage(damage_dealt,self)

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
        config.GAME.game_message(self.name_instance + " leveled up! He/She/It is now Level " + str(self.level),msg_color=constants.COLOR_GREEN)
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
        if self.dead_animation:
            self.owner.animation = self.dead_animation
            self.owner.animation_key = self.dead_animation_key
        self.owner.animation_key = "S_FLESH_SNAKE"
        killer.get_xp(self.xp_gained)
        self.owner.depth = constants.DEPTH_CORPSE
        if self.custom_death:
            self.custom_death(self, killer)
        self.owner.destroy()