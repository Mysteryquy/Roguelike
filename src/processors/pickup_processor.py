from src import esper, config
from src.components.action import PickUpAction
from src.components.container import Container
from src.components.currency import Gold
from src.components.item import Item
from src.components.name import Name
from src.components.position import Position
from src.components.render import Renderable


class Render(object):
    pass


class PickUpProcessor(esper.Processor):
    def process(self):
        for ent, (pos, _, container, name) in self.level.world.get_components(Position, PickUpAction, Container, Name):
            for ent_gold, gold in self.level.world.get_component_at_coords(pos.x, pos.y, Gold):
                print(gold)
                container.gold += gold.amount
                config.GAME.game_message(name.name + " picks up " + str(gold.amount) + " Gold")
                self.level.world.delete_entity(ent_gold, immediate=True)

            items = self.level.entities_at_coords(pos.x, pos.y, Item, exclude_ent=ent)
            self.level.world.remove_component(ent, PickUpAction)
            if len(items) > 0:
                for ent_item in items:
                    name_item = self.level.world.component_for_entity(ent_item, Name)
                    config.GAME.game_message(name.name + " picks up the " + name_item.name)
                    container.inventory.append(ent_item)
                    print(self.level.world.all_components_for_entity(ent_item))
                    item, render = self.level.world.components_for_entity(ent_item, Item, Renderable)
                    item.container = container
                    self.level.world.remove_component(ent_item, Position)
                    render.draw = False


