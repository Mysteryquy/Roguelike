from src import esper, constants, config, render_helper
from src.components.position import Position
from src.components.render import Renderable


class RenderProcessor(esper.Processor):
    def __init__(self, level):
        super().__init__(level=level)
        self.display_map_w = constants.CAMERA_WIDTH / constants.CELL_WIDTH
        self.display_map_h = constants.CAMERA_HEIGHT / constants.CELL_HEIGHT

    def process(self):
        # clear the surface
        config.SURFACE_INFO.fill(constants.COLOR_BLACK)
        pos = self.level.world.component_for_player(Position)
        config.CAMERA.update(pos.x, pos.y)
        config.GUI.update(None)
        config.GUI.draw()
        self.level.calculate_fov()
        # draw the map
        self.draw_map()
        self.draw_mini_map()

        self.draw_entities()

        config.SURFACE_INFO.blit(config.SURFACE_MINI_MAP, (0, 0))
        config.SURFACE_MAIN.blit(config.SURFACE_INFO, (constants.CAMERA_WIDTH, 0))
        config.SURFACE_MAIN.blit(config.SURFACE_MAP, (0, 0), config.CAMERA.rect)
        config.GUI.update(None)
        config.GUI.draw()
        render_helper.draw_debug()
        render_helper.draw_messages()
        config.CONSOLE.draw()

    def draw_entities(self):
        for ent, (render, pos) in sorted(self.level.world.get_components(Renderable, Position),
                                         key=lambda t: t[1][0].depth, reverse=True):

            is_visible = self.level.is_visible(pos.x, pos.y)
            explored_draw = render.draw_explored and self.level.is_explored(pos.x, pos.y) and not is_visible

            if render.draw and is_visible:
                animation = config.ASSETS.animation_dict[render.animation_key]
                if len(animation) == 1:
                    config.SURFACE_MAP.blit(animation[0],
                                            (pos.x * constants.CELL_WIDTH, pos.y * constants.CELL_HEIGHT))

                else:
                    if config.CLOCK.get_fps() > 0.0:
                        render.flicker_timer += 1 / config.CLOCK.get_fps()

                    if render.flicker_timer >= render.flicker_speed:
                        render.flicker_timer = 0.0
                        render.sprite_image = (render.sprite_image + 1) % len(animation)

                    config.SURFACE_MAP.blit(animation[render.sprite_image],
                                            (pos.x * constants.CELL_WIDTH, pos.y * constants.CELL_HEIGHT))

            if render.draw and explored_draw:
                animation = config.ASSETS.animation_dict_explored[render.animation_key]
                if len(animation) == 1:
                    config.SURFACE_MAP.blit(animation[0],
                                            (pos.x * constants.CELL_WIDTH, pos.y * constants.CELL_HEIGHT))

                else:
                    if config.CLOCK.get_fps() > 0.0:
                        render.flicker_timer += 1 / config.CLOCK.get_fps()

                    if render.flicker_timer >= render.flicker_speed:
                        render.flicker_timer = 0.0
                        render.sprite_image = (render.sprite_image + 1) % len(animation)

                    config.SURFACE_MAP.blit(animation[render.sprite_image],
                                            (pos.x * constants.CELL_WIDTH, pos.y * constants.CELL_HEIGHT))

    def draw_map(self):
        cam_x, cam_y = config.CAMERA.x / constants.CELL_WIDTH, config.CAMERA.y / constants.CELL_HEIGHT
        render_w_min = max(0, int(cam_x - self.display_map_w))
        render_h_min = max(0, int(cam_y - self.display_map_h))
        render_w_max = min(constants.MAP_WIDTH, int(cam_x + self.display_map_w))
        render_h_max = min(constants.MAP_HEIGHT, int(cam_y + self.display_map_h))
        map_to_draw = self.level.map

        for x in range(render_w_min, render_w_max):
            for y in range(render_h_min, render_h_max):
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
        for x in range(constants.MAP_WIDTH):
            for y in range(constants.MAP_HEIGHT):
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

