
"""
    def attack(self, target):

        chance_to_hit = self.base_hit_chance - target.creature.base_evasion

        if (chance_to_hit + tcod.random_get_int(None, 1, 100)) >= 100:
            self.hit(target)
        else:
            config.GAME.game_message(self.name_instance + " misses " + target.creature.name_instance)

    def hit(self, target: Actor):

        damage_dealt = self.power - target.creature.defense

        config.GAME.game_message(
            self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage_dealt) + " damage!",
            constants.COLOR_WHITE)

        target.creature.take_damage(damage_dealt, self.owner)

        for effect in self.onhit_effects:
            effect.on_attack(target)

        if damage_dealt > 0 and self.owner is config.PLAYER:
            pygame.mixer.Sound.play(config.RANDOM_ENGINE.choice(config.ASSETS.snd_list_hit))

    def take_damage(self, damage, attacker):
        self.hp -= damage
        config.GAME.game_message(self.name_instance + "`s health is " + str(self.hp) + "/" + str(self.maxhp),
                                 constants.COLOR_RED)

        if self.hp <= 0:
            self.death(killer=attacker)

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
        self.level += 1
        config.GAME.game_message(self.name_instance + " leveled up! He/She/It is now Level " + str(self.level),
                                 msg_color=constants.COLOR_GREEN)
        self.hp = max(self.hp, self.maxhp)
        self.current_mana = max(self.current_mana, self.max_mana)
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

    def death(self, killer: Actor):
        if self.death_text:
            config.GAME.game_message(self.name_instance + self.death_text,
                                     constants.COLOR_GREY)
        # print (monster.creature.name_instance + " is slaughtered into ugly bits of flesh!")
        if self.dead_animation_key:
            self.owner.set_animation(self.dead_animation_key)
        killer.creature.get_xp(self.xp_gained)
        self.owner.depth = constants.DEPTH_CORPSE
        if self.custom_death:
            self.custom_death(self, killer)


"""