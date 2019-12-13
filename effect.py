# coding=utf-8
from abc import ABC, abstractmethod
import constants
import config
from creature import Creature
from actor import Actor
from creature import Status
class Effect(ABC):
    def __init__(self, owner: Actor = None, duration: int = None):
        super().__init__()
        self.owner = owner
        self.duration = duration
        self.start_turn = config.ROUND_COUNTER

    def proc(self):
        if self.duration and config.ROUND_COUNTER > self.start_turn + self.duration:
            self.stop()
            return False
        self.update()
        return True

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def stop(self):
        pass
    @abstractmethod
    def start(self):
        pass

    def copy(self):
        pass


class StatusEffect(Effect):
    def __init__(self, owner: Actor, duration: int, effect_dict, autostart=True):
        super().__init__(owner=owner, duration=duration)
        self.effect_dict = effect_dict
        for status in Status:
            if status not in effect_dict:
                effect_dict[status] = 0
        self.autostart = autostart
        if autostart:
            self.start()

    def update(self):
        pass

    def copy(self):
        return StatusEffect(owner=self.owner, duration=self.duration, effect_dict=self.effect_dict, autostart=self.autostart)

    def start(self):

        self.owner.creature.add_int(self.effect_dict[Status.INTELLIGENCE])
        self.owner.creature.add_dex(self.effect_dict[Status.DEXTERITY])
        self.owner.creature.add_str(self.effect_dict[Status.STRENGTH])
        self.owner.creature.current_mana += self.effect_dict[Status.CURRENT_MANA]
        self.owner.creature.max_mana += self.effect_dict[Status.MAX_MANA]
        self.owner.creature.maxhp += self.effect_dict[Status.MAX_HP]
        self.owner.creature.hp += self.effect_dict[Status.CURRENT_HP]
        config.GAME.game_message("You are feeling a boost your stats for " + str(self.duration) + " turns!")

    def stop(self):
        self.owner.creature.add_int(-self.effect_dict[Status.INTELLIGENCE])
        self.owner.creature.add_dex(-self.effect_dict[Status.DEXTERITY])
        self.owner.creature.add_str(-self.effect_dict[Status.STRENGTH])
        self.owner.creature.current_mana -= self.effect_dict[Status.CURRENT_MANA]
        self.owner.creature.max_mana -= self.effect_dict[Status.MAX_MANA]
        self.owner.creature.maxhp -= self.effect_dict[Status.MAX_HP]
        self.owner.creature.hp -= self.effect_dict[Status.CURRENT_HP]
        config.GAME.game_message("You feel the surge of power leaving you")


class OnHitEffect(Effect):
    def __init__(self, owner, duration, apply: Effect):
        super().__init__(owner=owner, duration=duration)
        self.apply = apply
        self.start()

    def update(self):
        pass

    def on_attack(self, target):
        effect = self.apply.copy()
        effect.owner = target
        effect.start()
        target.add_effect(effect)
        config.GAME.game_message("An effect has been applied to " + target.name_object)


    def start(self):
        pass

    def stop(self):
        pass

    def copy(self):
        return OnHitEffect(owner=self.owner, duration=self.duration, apply=self.apply)



class DamageOverTimeEffect(Effect):
    def __init__(self, applier,  duration: int, damage: int, owner:  Actor = None):
        super().__init__(owner=owner, duration=duration)
        self.damage = damage
        self.applier = applier

    def update(self):
        self.owner.creature.take_damage(self.damage, self.applier)
        config.GAME.game_message(self.owner.name_object + " takes " + str(self.damage) +" from " + self.applier.name_object, constants.COLOR_BLUE)

    def stop(self):
        pass

    def start(self):
        pass

    def copy(self):
        return DamageOverTimeEffect(applier=self.applier, duration=self.duration, damage=self.damage, owner=self.owner)
