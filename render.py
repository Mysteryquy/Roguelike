from typing import Tuple

import pygame

from src import config, constants


def draw_text(display_surface, text_to_display, coords, text_color, back_color=None, center=False,
              font=config.ASSETS.FONT_DEBUG_MESSAGE):
    # This function takes in some text and display

    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color, font)
    if center:
        text_rect.center = coords
    else:
        text_rect.topleft = coords

    display_surface.blit(text_surf, text_rect)


def draw_tile_rect(coords: Tuple[int, int], color=constants.COLOR_WHITE, tile_alpha=200, mark=False):
    x, y = coords

    new_x = x * constants.CELL_WIDTH
    new_y = y * constants.CELL_HEIGHT

    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))

    new_surface.fill(color)

    new_surface.set_alpha(tile_alpha)

    if mark:
        draw_text(new_surface, "X", (constants.CELL_WIDTH / 2, constants.CELL_HEIGHT / 2), constants.COLOR_BLACK,
                  center=True)

    config.SURFACE_MAP.blit(new_surface, (int(new_x), int(new_y)))


def helper_text_objects(incoming_text, incoming_color, incoming_bg, font):
    if incoming_bg:
        text_surface = font.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        text_surface = font.render(incoming_text, False, incoming_color)

    return text_surface, text_surface.get_rect()





def draw_menu():
    # clear the surface
    config.SURFACE_INFO.fill(constants.COLOR_BLACK)
    config.CAMERA.update()
    # fill_surfaces()
    # draw the map

    config.GUI.update(None)
    config.GUI.draw()
    # print(CAMERA.rectangle)

    draw_debug()


def draw_game():
    # clear the surface
    config.SURFACE_INFO.fill(constants.COLOR_BLACK)
    config.CAMERA.update()
    # fill_surfaces()
    config.GUI.update(None)
    config.GUI.draw()
    # draw the map
    draw_map(config.GAME.current_map)
    draw_mini_map(config.GAME.current_map)

    for obj in sorted(config.GAME.current_objects, key=lambda x: x.depth, reverse=True):
        obj.draw()

    config.SURFACE_INFO.blit(config.SURFACE_MINI_MAP, (0, 0))
    config.SURFACE_MAIN.blit(config.SURFACE_INFO, (constants.CAMERA_WIDTH, 0))
    config.SURFACE_MAIN.blit(config.SURFACE_MAP, (0, 0), config.CAMERA.rect)
    config.GUI.update(None)
    config.GUI.draw()
    # print(CAMERA.rectangle)

    draw_debug()
    draw_messages()
    config.CONSOLE.draw()


def fill_surfaces():
    config.SURFACE_MAIN.fill(constants.COLOR_DARK_GREY)
    config.SURFACE_MAP.fill(constants.COLOR_DARK_GREY)
    config.SURFACE_MINI_MAP.fill(constants.COLOR_BLACK)
    config.SURFACE_INFO.fill(constants.COLOR_BLACK)


def draw_map(map_to_draw):
    DISPLAY_MAP_W = constants.CAMERA_WIDTH / constants.CELL_WIDTH
    DISPLAY_MAP_H = constants.CAMERA_HEIGHT / constants.CELL_HEIGHT
    cam_x, cam_y = config.CAMERA.x / constants.CELL_WIDTH, config.CAMERA.y / constants.CELL_HEIGHT

    render_w_min = int(cam_x - DISPLAY_MAP_W)
    render_h_min = int(cam_y - DISPLAY_MAP_H)
    render_w_max = int(cam_x + DISPLAY_MAP_W)
    render_h_max = int(cam_y + DISPLAY_MAP_H)

    render_w_min = max(0, render_w_min)
    render_h_min = max(0, render_h_min)
    render_w_max = min(constants.MAP_WIDTH, render_w_max)
    render_h_max = min(constants.MAP_HEIGHT, render_h_max)

    for x in range(render_w_min, render_w_max):
        for y in range(render_h_min, render_h_max):

            is_visible = config.FOV_MAP.fov[y, x]
            if is_visible and not map_to_draw[x][y].explored:
                map_to_draw[x][y].explored = True
            if map_to_draw[x][y].explored or map_to_draw[x][y].draw_on_screen:
                if is_visible:
                    map_to_draw[x][y].draw_on_screen = True
                    config.SURFACE_MAP.blit(config.ASSETS.tile_dict[map_to_draw[x][y].texture],
                                            (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                elif map_to_draw[x][y].draw_on_screen:
                    config.SURFACE_MAP.blit(config.ASSETS.tile_dict[map_to_draw[x][y].texture_explored],
                                            (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                    map_to_draw[x][y].draw_on_screen = False


def draw_debug():
    draw_text(config.SURFACE_MAIN, "FPS: " + str(int(config.CLOCK.get_fps())), (0, 0), constants.COLOR_WHITE,
              constants.COLOR_BLACK)
    draw_text(config.SURFACE_MAIN, "Turn: " + str(config.ROUND_COUNTER), (0, 20), constants.COLOR_WHITE,
              constants.COLOR_BLACK)


def draw_messages():
    if len(config.GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = config.GAME.message_history
    else:
        to_draw = config.GAME.message_history[-constants.NUM_MESSAGES:]

    _, text_height = config.ASSETS.FONT_MESSAGE_TEXT.size("A")
    start_y = (constants.CAMERA_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 50

    for i, (message, color) in enumerate(to_draw):
        draw_text(config.SURFACE_MAIN, message, (0, start_y + i * text_height), color, constants.COLOR_BLACK)


def draw_mini_map(map_to_draw):
    for x in range(constants.MAP_WIDTH):
        for y in range(constants.MAP_HEIGHT):
            is_visible = config.FOV_MAP.fov[y, x]
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

    config.SURFACE_MINI_MAP.blit(config.ASSETS.MINIMAP_RED_RECT,
                                 (config.PLAYER.x * constants.MINI_MAP_CELL_WIDTH,
                                  config.PLAYER.y * constants.MINI_MAP_CELL_HEIGHT))


def draw_info():
    pass
