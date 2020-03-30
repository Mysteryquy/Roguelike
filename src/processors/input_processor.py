import pygame

from src import esper, config, constants, menu
from src.components.action import MovementAction, UseStairsAction, StartAutoexploreAction
from src.components.action import PickUpAction

from src.components.action import HasAction, DropAction
from src.components.player import Player
from src.components.position import Position

MOVEMENT_DICT = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_KP1: (-1, 1),
    pygame.K_KP2: (0, 1),
    pygame.K_KP3: (1, 1),
    pygame.K_KP4: (-1, 0),
    pygame.K_KP5: (0, 0),
    pygame.K_KP6: (1, 0),
    pygame.K_KP7: (-1, -1),
    pygame.K_KP8: (0, -1),
    pygame.K_KP9: (1, -1),
}


class InputProcessor(esper.Processor):
    def __init__(self, game_save, game_load, level=None):
        super().__init__(level)
        self.game_save = game_save
        self.game_load = game_load

    def process(self):
        pos = self.level.world.component_for_player(Position)
        x, y = pos.x, pos.y
        # there is only one player
        keys_pressed = pygame.key.get_pressed()
        events = pygame.event.get()
        mod_key = (keys_pressed[pygame.K_RSHIFT] or keys_pressed[pygame.K_LSHIFT])

        for event in events:
            """
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x, y = config.CAMERA.coords_from_position(x, y)
                if game_map.is_explored(x, y):
                    config.GAME.auto_explore_path = iter(game_map.get_path_from_player(x, y))
            """
            """
            if config.CONSOLE.active:
                if config.CONSOLE.react(event):
                    command = config.CONSOLE.text_ready
                    console.invoke_command(command)
                    return
            if event.type == pygame.QUIT:
                return ACTIONS.QUIT
            """
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key in MOVEMENT_DICT.keys():
                    dx, dy = MOVEMENT_DICT[event.key]
                    self.level.world.add_component(self.player, MovementAction(dx, dy))
                    self.level.world.remove_component(self.player, HasAction)

                if event.key == pygame.K_g:
                    self.level.world.add_component(self.player, PickUpAction())
                    self.level.world.remove_component(self.player, HasAction)

                if event.key == pygame.K_d:
                    self.level.world.add_component(self.player, DropAction())
                    self.level.world.remove_component(self.player, HasAction)

                if event.key == pygame.K_p:
                    config.GAME.game_message("Game resumed", constants.COLOR_WHITE)
                    menu.menu_pause()

                if event.key == pygame.K_i:
                    pygame.mixer.Channel(1).play(
                        pygame.mixer.Sound("data/audio/soundeffects/leather_inventory.wav"))
                    menu.menu_inventory()

                if event.key == pygame.K_l:
                    menu.menu_tile_select(self.level)

                if event.key == pygame.K_x:
                    menu.debug_tile_select(self.level)

                if event.key == pygame.K_s:
                    config.GAME.transition_next()

                if event.key == pygame.K_1:
                    config.GAME.game_message("Player position: " + str((x, y)))

                if event.key == pygame.K_2:
                    config.GAME.game_message("Camera position: " + str(config.CAMERA.cam_map_coord))

                if event.key == pygame.K_b:
                    self.game_save(display_message=True)
                    self.game_load()

                if mod_key and event.key == pygame.K_PERIOD:
                    self.level.world.add_component(self.player, UseStairsAction())

                if event.key == pygame.K_BACKQUOTE:
                    self.level.world.add_component(self.player, StartAutoexploreAction())

                if event.key == pygame.K_v:
                    pass
                    # TODO CHANGE THIS
                    # cast_buffstats(config.PLAYER, 10)
                    # return ACTIONS.SPELL
