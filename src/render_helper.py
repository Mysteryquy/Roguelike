from typing import Tuple

import pygame

from src import config, constants, map_helper, assets
from src.components.position import Position


def draw_text(display_surface, text_to_display, coords, text_color, back_color=None, center=False,
              font=None):
    # This function takes in some text and display
    if not font:
        font = config.ASSETS.FONT_DEBUG_MESSAGE
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


def draw_messages():
    history_length = len(config.GAME.message_history)

    rect = pygame.Rect(0, constants.CAMERA_HEIGHT - 140, 400, 100)

    if history_length == config.GAME.message_history_old_length:
        config.SURFACE_MAIN.blit(config.SURFACE_MESSAGES, rect)
        # nothing to draw here, just old stuff
        return

    config.SURFACE_MESSAGES.fill((0, 0, 0))
    config.SURFACE_MESSAGES.set_colorkey((0,0,0))
    map_helper.transition_reset()
    config.SURFACE_MAIN.blit(config.SURFACE_MAP, (0, 0), config.CAMERA.rect)
    if history_length <= constants.NUM_MESSAGES:
        to_draw = config.GAME.message_history
    else:
        to_draw = config.GAME.message_history[-constants.NUM_MESSAGES:]

    _, text_height = config.ASSETS.FONT_MESSAGE_TEXT.size("A")

    for i, (message, color) in enumerate(to_draw):
        draw_text(config.SURFACE_MESSAGES, message, (0, i * text_height), color)

    config.GAME.message_history_old_length = history_length
    config.SURFACE_MAIN.blit(config.SURFACE_MESSAGES, rect)


def draw_menu():
    # clear the surface
    config.SURFACE_INFO.fill(constants.COLOR_BLACK)
    pos = config.GAME.current_level.world.component_for_player(Position)
    config.CAMERA.update(pos.x, pos.y)
    # fill_surfaces()
    # draw the map
    config.GUI.update(None)
    config.GUI.draw()
    # print(CAMERA.rectangle)
    draw_debug()


def fill_surfaces():
    config.SURFACE_MAIN.fill(constants.COLOR_DARK_GREY)
    config.SURFACE_MAP.fill(constants.COLOR_DARK_GREY)
    config.SURFACE_MINI_MAP.fill(constants.COLOR_BLACK)
    config.SURFACE_INFO.fill(constants.COLOR_BLACK)
    if config.GAME:
        config.GAME.message_history_old_length = 0


def draw_debug():
    draw_text(config.SURFACE_MAIN, "FPS: " + str(int(config.CLOCK.get_fps())), (0, 0),
              constants.COLOR_WHITE,
              constants.COLOR_BLACK)

    draw_text(config.SURFACE_MAIN, "Turn: " + str(config.ROUND_COUNTER), (0, 20),
              constants.COLOR_WHITE,
              constants.COLOR_BLACK)


def helper_text_dimensions(font):
    return font.size("A")
