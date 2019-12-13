# coding=utf-8
from abc import ABC, abstractmethod
import config
class Effect(ABC):
    def __init__(self, owner=None, duration=None):
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


class StatusEffect(Effect):
    def __init__(self, owner, dstr, ddex, dint, duration):
        super().__init__(owner=owner, duration=duration)
        self.ddex = ddex
        self.dstr = dstr
        self.dint = dint
        self.start()


    def update(self):
        pass

    def start(self):
        self.owner.add_int(self.dint)
        self.owner.add_dex(self.ddex)
        self.owner.add_str(self.dstr)
        self.owner.hp = self.owner.hp + self.owner.strength
        self.owner.current_mana = self.owner.current_mana + self.owner.intelligence * 2
        config.GAME.game_message("You are feeling a boost of all your stats for " + str(self.duration) + " turns!")

    def stop(self):
        self.owner.add_int(-self.dint)
        self.owner.add_dex(-self.ddex)
        self.owner.add_str(-self.dstr)
        config.GAME.game_message("You feel the surge of power leaving you")


class Debuff(Effect):
    def __init__(self, owner, damage, duration):
        super().__init__(owner=owner, duration=duration)
        self.damage = damage
        self.start()


    def update(self):
        pass

    def start(self):
        self.owner.hp = self.owner.hp - self.damage
        config.GAME.game_message("You are covered in flames that deal " + str(self.damage)+ " for " + str(self.duration) + " turns!")

    def stop(self):
        config.GAME.game_message("You feel that the flames stopped burning your beautiful body.")