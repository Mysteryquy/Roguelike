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
            self.level.world.remove_component(ent, PickUpAction)
            for ent_gold, gold in self.level.get_entity_component_at_position(pos, Gold):
                print(gold)
                container.gold += gold.amount
                config.GAME.game_message(name.name + " picks up " + str(gold.amount) + " Gold")
                self.level.world.delete_entity(ent_gold, immediate=True)

            for ent_item, (item, render, name_item) in \
                    self.level.get_entity_components_at_position(pos, Item, Renderable, Name, exclude_ent=ent):
                config.GAME.game_message(name.name + " picks up the " + name_item.name)
                container.inventory.append(ent_item)
                item.container = container
                self.level.world.remove_component(ent_item, Position)
                render.draw = False

