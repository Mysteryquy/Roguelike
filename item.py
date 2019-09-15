import config


class Item:

    def __init__(self, weight=0.0, volume=0.0, use_function=None, value=None, pickup_text=None):
        self.weight = weight
        self.volume = volume
        self.value = value
        self.use_function = use_function
        self.pickup_text = pickup_text
        self.container = None

    ## Pick up this item
    def pick_up(self, actor):

        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
                config.GAME.game_message("Not enough room to pick up")

            else:
                if self.pickup_text:
                    config.GAME.game_message("Picked up " + self.pickup_text)
                else:
                    config.GAME.game_message("Picked up")
                actor.container.inventory.append(self.owner)
                self.owner.animation_destroy()
                config.GAME.current_objects.remove(self.owner)
                self.container = actor.container

    ## Drop Item
    def drop(self, new_x, new_y):
        config.GAME.current_objects.append(self.owner)
        self.owner.animation_init()
        self.container.inventory.remove(self.owner)
        self.owner.x = new_x
        self.owner.y = new_y
        config.GAME.game_message("Item dropped")

    ##  Use item
    def use(self):

        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.use_function:
            result = self.use_function(self.container.owner, self.value)

            if result is not None:
                print("use function failed")

            else:
                self.container.inventory.remove(self.owner)
