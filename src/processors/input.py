import pygame

import game_map
from src import esper, config, console
from src.components.player import Player


class InputProcessor(esper.Processor):
    def process(self):
        for ent in self.world.get_component(Player):
            # there is only one player
            keys_pressed = pygame.key.get_pressed()
            events = pygame.event.get()
            mod_key = (keys_pressed[pygame.K_RSHIFT] or keys_pressed[pygame.K_LSHIFT])

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x, y = config.CAMERA.coords_from_position(x, y)
                    if game_map.is_explored(x, y):
                        config.GAME.auto_explore_path = iter(game_map.get_path_from_player(x, y))

                if config.CONSOLE.active:
                    if config.CONSOLE.react(event):
                        command = config.CONSOLE.text_ready
                        console.invoke_command(command)
                        return
                if event.type == pygame.QUIT:
                    return ACTIONS.QUIT

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return ACTIONS.QUIT

                    if event.key in constants.MOVEMENT_DICT.keys():
                        dx, dy = constants.MOVEMENT_DICT[event.key]
                        if game_map.is_walkable(config.PLAYER.x + dx, config.PLAYER.y + dy):
                            config.PLAYER.move(dx, dy)
                            config.FOV_CALCULATE = True
                            return ACTIONS.MOVED
                        else:
                            return ACTIONS.NO_ACTION

                    if event.key == pygame.K_g:
                        objects_at_player = config.GAME.current_level.objects_at_coords(config.PLAYER.x,
                                                                                        config.PLAYER.y)

                        for obj in objects_at_player:
                            if obj.item:
                                print(obj.name_object)
                                obj.item.pick_up(config.PLAYER)
                        return ACTIONS.PICKED_UP

                    if event.key == pygame.K_d:
                        if len(config.PLAYER.container.inventory) > 0:
                            config.PLAYER.container.inventory[-1].item.drop(config.PLAYER.x, config.PLAYER.y)
                        return ACTIONS.DROP

                    if event.key == pygame.K_p:
                        config.GAME.game_message("Game resumed", constants.COLOR_WHITE)
                        menu.menu_pause()
                        return ACTIONS.PAUSE

                    if event.key == pygame.K_i:
                        pygame.mixer.Channel(1).play(
                            pygame.mixer.Sound("data/audio/soundeffects/leather_inventory.wav"))
                        menu.menu_inventory()
                        return ACTIONS.INVENTORY

                    if event.key == pygame.K_l:
                        menu.menu_tile_select()
                        return ACTIONS.TILE_SELECT

                    if event.key == pygame.K_x:
                        menu.debug_tile_select()
                        return ACTIONS.DEBUG

                    if event.key == pygame.K_s:
                        config.GAME.transition_next()
                        return ACTIONS.DEBUG

                    if event.key == pygame.K_1:
                        config.GAME.game_message("Player position: " + str((config.PLAYER.x, config.PLAYER.y)))
                        return ACTIONS.DEBUG

                    if event.key == pygame.K_2:
                        config.GAME.game_message("Camera position: " + str(config.CAMERA.cam_map_coord))
                        return ACTIONS.DEBUG

                    if event.key == pygame.K_b:
                        game_save(display_message=True)
                        game_load()
                        return ACTIONS.DEBUG

                    if event.key == pygame.K_r:
                        cast_raisedead(config.PLAYER, 10)
                        return ACTIONS.SPELL

                    if MOD_KEY and event.key == pygame.K_PERIOD:
                        list_of_objs = config.GAME.current_level.objects_at_coords(config.PLAYER.x, config.PLAYER.y)
                        for obj in list_of_objs:
                            if obj.structure:
                                obj.structure.use()
                        return ACTIONS.USED

                    if event.key == pygame.K_BACKQUOTE:
                        game_map.start_auto_explore()
                        return ACTIONS.AUTOEXPLORED

                    if event.key == pygame.K_v:
                        cast_buffstats(config.PLAYER, 10)
                        return ACTIONS.SPELL

        pass
