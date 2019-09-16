import constants
import pygame
import config


def draw_text(display_surface, text_to_display, T_coords, text_color, back_color=None, center=False):
    # This function takes in some text and display

    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)
    if not center:
        text_rect.topleft = T_coords
    else:
        text_rect.center = T_coords

    display_surface.blit(text_surf, text_rect)


def draw_tile_rect(coords, color=None, tile_alpha=None, mark=None):
    x, y = coords

    if color:
        local_color = color
    else:
        local_color = constants.COLOR_WHITE

    if tile_alpha:
        local_alpha = tile_alpha
    else:
        local_alpha = 200

    new_x = x * constants.CELL_WIDTH
    new_y = y * constants.CELL_HEIGHT

    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))

    new_surface.fill(local_color)

    new_surface.set_alpha(local_alpha)

    if mark:
        draw_text(new_surface, "X", (constants.CELL_WIDTH / 2, constants.CELL_HEIGHT / 2), constants.COLOR_BLACK,
                  center=True)

    config.SURFACE_MAP.blit(new_surface, (int(new_x), int(new_y)))


def helper_text_objects(incoming_text, incoming_color, incoming_bg):
    if incoming_bg:
        Text_surface = config.ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        Text_surface = config.ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color)

    return Text_surface, Text_surface.get_rect()


def helper_text_height(font):
    (width, height) = font.size("A")
    # font_object = font.render("a", False, (0,0,0))
    # font_rect = font_object.get_rect
    return height


def helper_text_width(font):
    (width, height) = font.size("A")

    return width


def draw_game():
    # clear the surface
    config.SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    config.SURFACE_MAP.fill(constants.COLOR_BLACK)

    config.CAMERA.update()

    # draw the map
    draw_map(config.GAME.current_map)

    for obj in sorted(config.GAME.current_objects, key=lambda x: x.depth, reverse=True):
        obj.draw()

    config.SURFACE_MAIN.blit(config.SURFACE_MAP, (0, 0), config.CAMERA.rectangle)
    # print(CAMERA.rectangle)

    draw_debug()
    draw_messages()


def draw_map(map_to_draw):
    cam_x, cam_y = config.CAMERA.map_address
    display_map_w = constants.CAMERA_WIDTH / constants.CELL_WIDTH
    display_map_h = constants.CAMERA_HEIGHT / constants.CELL_HEIGHT

    render_w_min = int(cam_x - (display_map_w / 2))
    render_h_min = int(cam_y - (display_map_h / 2))
    render_w_max = int(cam_x + (display_map_w / 2))
    render_h_max = int(cam_y + (display_map_h / 2))

    if render_w_min < 0:
        render_w_min = 0
    if render_h_min < 0:
        render_h_min = 0
    if render_w_max > constants.MAP_WIDTH:
        render_w_max = constants.MAP_WIDTH
    if render_h_max > constants.MAP_HEIGHT:
        render_h_max = constants.MAP_HEIGHT

    for x in range(render_w_min, render_w_max):
        for y in range(render_h_min, render_h_max):

            is_visible = config.FOV_MAP.fov[y, x]
            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path:

                    config.SURFACE_MAP.blit(config.ASSETS.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    config.SURFACE_MAP.blit(config.ASSETS.S_FLOOR,
                                            (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            elif map_to_draw[x][y].explored:

                if map_to_draw[x][y].block_path:  # Bruh was will der von mir

                    config.SURFACE_MAP.blit(config.ASSETS.S_WALLEXPLORED,
                                            (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    config.SURFACE_MAP.blit(config.ASSETS.S_FLOOREXPLORED,
                                            (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def draw_debug():
    draw_text(config.SURFACE_MAIN, "fps: " + str(int(config.CLOCK.get_fps())), (0, 0), constants.COLOR_WHITE,
              constants.COLOR_BLACK)


def draw_messages():
    if len(config.GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = config.GAME.message_history
    else:
        to_draw = config.GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_height(config.ASSETS.FONT_MESSAGE_TEXT)

    # info = pygame.display.Info()
    # screen_height = info.current_h

    start_y = (constants.CAMERA_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 5

    i = 0

    for message, color in to_draw:
        draw_text(config.SURFACE_MAIN, message, (0, start_y + i * text_height), color, constants.COLOR_BLACK)

        i += 1


