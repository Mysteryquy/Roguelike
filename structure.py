import datetime
from abc import ABC, abstractmethod

import pygame

import render
from src import config, constants


class Structure(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def use(self):
        pass

    @abstractmethod
    def update(self):
        pass


class Stairs(Structure):

    def __init__(self, leads_to, downwards):
        super().__init__()
        self.leads_to = leads_to
        self.downwards = downwards

    def use(self):

        config.GAME.transition(self.leads_to)

    def update(self):
        pass


class ExitPortal(Structure):
    def __init__(self):
        super().__init__()
        self.open_animation = "S_END_GAME_PORTAL_OPENED"
        self.end_animation = "S_END_GAME_PORTAL_CLOSED"
        self.open = False
        self.owner = None

    def update(self):

        found_item = False

        # check conditions
        portal_open = self.owner.state == "OPEN"

        for obj in config.PLAYER.container.inventory:
            if obj.name_object is constants.END_GAME_ITEM_NAME:
                found_item = True

        if found_item and not portal_open:
            self.owner.state = "OPEN"
            self.owner.animation_key = "S_END_GAME_PORTAL_OPENED"
            self.owner.animation_init()

        if not found_item and portal_open:
            self.owner.state = "CLOSED"
            self.owner.animation_key = "S_END_GAME_PORTAL_CLOSED"
            self.owner.animation_init()

    def use(self):

        print("Hans Wurst")

        if self.owner.state == "OPEN":
            config.PLAYER.state = "STATUS_WIN"

            config.SURFACE_MAIN.fill(constants.COLOR_WHITE)

            screen_center = (constants.RECT_WHOLE_SCREEN.width / 2, constants.RECT_WHOLE_SCREEN.height / 2)

            render.draw_text(config.SURFACE_MAIN, "YOU WON!", screen_center, constants.COLOR_BLACK, center=True)
            render.draw_text(config.SURFACE_MAIN, "Your win was recorded in your win file",
                             (constants.RECT_WHOLE_SCREEN.width / 2, constants.RECT_WHOLE_SCREEN.height / 2 + 100), constants.COLOR_BLUE,
                             center=True)

            pygame.display.update()

            file_name = (
                    "data/userdata/winrecord_" + config.PLAYER.creature.name_instance + "." + datetime.date.today().strftime(
                "%Y%B%d") + ".txt")

            winrecord = open(file_name, "a+")

            winrecord.write("You won on the " + datetime.date.today().strftime(
                "%Y%B%d") + " as " + config.PLAYER.creature.name_instance + "\n")

            pygame.time.wait(6000)
