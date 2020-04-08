import pygame

from src import esper, constants, config, render_helper
from src.components.name import Name
from src.components.position import Position
from src.components.render import Renderable


class RenderProcessor(esper.Processor):
    def __init__(self, level):
        super().__init__(level=level)
        self.message_rect = pygame.Rect(0, constants.CAMERA_HEIGHT - 140, 400, 100)
        self.message_history_old_length = 0
        _, self.text_height = config.ASSETS.FONT_MESSAGE_TEXT.size("A")
        self.map_rect_messages = pygame.Rect(0, constants.CAMERA_HEIGHT, 400, 100)

    def process(self):
        # clear the surface
        # TODO maybe add back in?
        # config.SURFACE_INFO.fill(constants.COLOR_BLACK)
        pos = self.level.world.component_for_player(Position)
        config.CAMERA.update(pos.x, pos.y)
        config.MINI_MAP_CAMERA.update(pos.x, pos.y)
        config.GUI.update(None)
        config.GUI.draw()
        self.level.calculate_fov()
        # draw the map
        self.draw_map()
        self.draw_mini_map()
        self.draw_entities()
        self.draw_messages()

        config.SURFACE_INFO.blit(config.SURFACE_MINI_MAP, config.MINI_MAP_CAMERA.rect)
        config.SURFACE_MAIN.blit(config.SURFACE_INFO, (constants.CAMERA_WIDTH, 0))
        config.SURFACE_MAIN.blit(config.SURFACE_MAP, (0, 0), config.CAMERA.rect)
        config.SURFACE_MAIN.blit(config.SURFACE_MESSAGES, self.message_rect, special_flags=pygame.BLEND_RGBA_ADD)
        config.GUI.update(None)
        config.GUI.draw()
        render_helper.draw_debug()
        config.CONSOLE.draw()

    def draw_entities(self):
        for ent, (render, pos) in sorted(self.level.world.get_components(Renderable, Position),
                                         key=lambda t: t[1][0].depth, reverse=True):
            is_visible = self.level.is_visible(pos.x, pos.y)
            explored_draw = render.draw_explored and self.level.is_explored(pos.x, pos.y) and not is_visible

            if render.draw:
                animation = None
                if is_visible:
                    animation = config.ASSETS.animation_dict[render.animation_key]
                elif explored_draw:
                    animation = config.ASSETS.animation_dict_explored[render.animation_key]
                if animation:
                    img = animation[0]
                    if len(animation) > 1:
                        if config.CLOCK.get_fps() > 0.0:
                            render.flicker_timer += 1 / config.CLOCK.get_fps()

                        if render.flicker_timer >= render.flicker_speed:
                            render.flicker_timer = 0.0
                            render.sprite_image = (render.sprite_image + 1) % len(animation)
                        img = animation[render.sprite_image]

                    config.SURFACE_MAP.blit(img,
                                            (pos.x * constants.CELL_WIDTH, pos.y * constants.CELL_HEIGHT),
                                            special_flags=render.special_flags)

    def draw_map(self):
        map_to_draw = self.level.map
        for x in config.CAMERA.render_range_w:
            for y in config.CAMERA.render_range_h:
                is_visible = self.level.is_visible(x, y)
                if is_visible and not map_to_draw[x][y].explored:
                    map_to_draw[x][y].explored = True
                if map_to_draw[x][y].explored or map_to_draw[x][y].draw_on_screen:
                    if is_visible:
                        map_to_draw[x][y].draw_on_screen = True
                        config.SURFACE_MAP.blit(config.ASSETS.tile_dict[map_to_draw[x][y].texture],
                                                (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                    elif map_to_draw[x][y].draw_on_screen:
                        config.SURFACE_MAP.blit(config.ASSETS.tile_dict_explored[map_to_draw[x][y].texture],
                                                (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                        map_to_draw[x][y].draw_on_screen = False

    def draw_mini_map(self):
        map_to_draw = self.level.map
        for x in config.MINI_MAP_CAMERA.render_range_w:
            for y in config.MINI_MAP_CAMERA.render_range_h:
                is_visible = self.level.is_visible(x, y)
                if map_to_draw[x][y].explored and not map_to_draw[x][y].block_path:
                    if is_visible:
                        map_to_draw[x][y].draw_on_minimap = True
                        config.SURFACE_MINI_MAP.blit(config.ASSETS.MINIMAP_YELLOW_RECT,
                                                     (
                                                         x * constants.MINI_MAP_CELL_WIDTH,
                                                         y * constants.MINI_MAP_CELL_HEIGHT))
                        map_to_draw[x][y].was_drawn = True
                    elif map_to_draw[x][y].draw_on_minimap:
                        config.SURFACE_MINI_MAP.blit(config.ASSETS.MINIMAP_GOLD_RECT,
                                                     (
                                                         x * constants.MINI_MAP_CELL_WIDTH,
                                                         y * constants.MINI_MAP_CELL_HEIGHT))
                        map_to_draw[x][y].draw_on_minimap = False
                        map_to_draw[x][y].was_drawn = True

        pos = self.level.world.component_for_player(Position)
        config.SURFACE_MINI_MAP.blit(config.ASSETS.MINIMAP_RED_RECT,
                                     (pos.x * constants.MINI_MAP_CELL_WIDTH,
                                      pos.y * constants.MINI_MAP_CELL_HEIGHT))

    def draw_messages(self):
        history_length = len(config.GAME.message_history)
        if history_length != self.message_history_old_length:
            config.SURFACE_MESSAGES.fill((0, 0, 0))
            to_draw = config.GAME.message_history[-constants.NUM_MESSAGES:]
            for i, (message, color) in enumerate(to_draw):
                render_helper.draw_text(config.SURFACE_MESSAGES, message, (0, i * self.text_height), color)
            config.GAME.message_history_old_length = history_length
