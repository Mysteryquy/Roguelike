from src import esper, constants, config
from src.components.position import Position
from src.components.render import Renderable


class RenderProcessor(esper.Processor):
    def process(self):
        for ent, (render, pos) in sorted(self.world.get_components(Renderable, Position),
                                         key=lambda t: t[1][1].depth, reverse=True):
            x, y = pos
            is_visible = self.level.is_visible(x, y)
            explored_draw = render.draw_explored and self.level.is_explored(x, y) and not is_visible
            special_flags = constants.EXPLORED_DRAW_FLAGS if explored_draw else 0

            if is_visible or explored_draw:
                if len(render.animation) == 1:
                    config.SURFACE_MAP.blit(render.animation[0],
                                            (pos.x * constants.CELL_WIDTH, pos.y * constants.CELL_HEIGHT),
                                            special_flags=special_flags)

                elif len(render.animation) > 1:
                    if config.CLOCK.get_fps() > 0.0:
                        render.flicker_timer += 1 / config.CLOCK.get_fps()

                    if render.flicker_timer >= render.flicker_speed:
                        render.flicker_timer = 0.0
                        render.sprite_image = (render.sprite_image + 1) % len(render.animation)

                    config.SURFACE_MAP.blit(render.animation[render.sprite_image],
                                            (pos.x * constants.CELL_WIDTH, pos.y * constants.CELL_HEIGHT),
                                            special_flags=special_flags)
