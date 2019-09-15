
class Container(object):

    def __init__(self, volume=10.0, inventory=None):
        if inventory is None:
            inventory = []
        self.inventory = inventory
        self.max_volume = volume
        self._volume = 0.0
        self.owner = None

    @property
    def volume(self):
        return self._volume

    ## TODO Get Names of everything in inventory

    @property
    def equipped_items(self):
        list_of_equipped_items = [obj for obj in self.inventory if obj.equipment and obj.equipment.equipped]

        return list_of_equipped_items

    ## TODO Get weight of everything in cointainer
