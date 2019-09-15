import config
import constants
from item import Item


class Equipment(Item):

    def __init__(self, attack_bonus=None, defense_bonus=None, slot=None, equip_text=None, value=0, pickup_text=None,
                 weight=0.0, volume=0.0):
        Item.__init__(self, weight=weight, volume=volume, use_function=self.equip, value=value, pickup_text=pickup_text)
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.slot = slot
        self.equip_text = equip_text
        self.equipped = False
        self.owner = None

    def toggle_equip(self):

        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):

        # check for equ in slot
        all_equipped_items = self.owner.item.container.equipped_items

        for item in all_equipped_items:
            if item.equipment.slot and (item.equipment.slot == self.slot):
                config.GAME.game_message("Equipment slot is occupied!", constants.COLOR_RED)
                return

        # toggle self.equipped
        self.equipped = True
        if self.equip_text:
            config.GAME.game_message("Equipped the " + self.equip_text)
        else:
            config.GAME.game_message("Item equipped")

    def unequip(self):

        # toggle self.equipped
        self.equipped = False

        config.GAME.game_message("Item uneqipped")
