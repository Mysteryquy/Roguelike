import pygame

from src import esper, config, constants, menu, casting, map_helper
from src.components.action import MovementAction, UseStairsAction, StartAutoexploreAction, SpellcastAction
from src.components.action import PickUpAction

from src.components.action import HasAction, DropAction
from src.components.autoexplore import AutoExploring
from src.components.player import Player
from src.components.position import Position
from src.resources.spells import Spells

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                goal_x, goal_y = config.CAMERA.coords_from_position(mx, my)
                if not map_helper.check_bounds(goal_x, goal_y):
                    goal_x, goal_y = config.MINI_MAP_CAMERA.coords_from_position(mx, my)
                if map_helper.check_bounds(goal_x, goal_y):
                    path = iter(config.GAME.pathing.get_path(pos.x, pos.y, goal_x, goal_y))
                    self.level.world.add_component(self.player, AutoExploring(path=path, continue_after_goal=False,
                                                                              force_one_move=True))
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
                    if self.level.world.has_component(self.player, AutoExploring):
                        self.level.world.remove_component(self.player, AutoExploring)

                if event.key == event.key == pygame.K_BACKQUOTE:
                    self.level.world.add_component(self.player, StartAutoexploreAction())

                if event.key == pygame.K_v:
                    self.level.world.add_component(self.player, SpellcastAction(spell=Spells.Heal,
                                                                                args={
                                                                                    "target": self.player,
                                                                                    "amount": 5
                                                                                }))
