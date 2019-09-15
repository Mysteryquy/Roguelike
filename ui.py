import constants
import pygame
from render import draw_text


class Button:

    def __init__(self,
                 surface,
                 button_text,
                 size,
                 center_coords,
                 color_box_mouseover=constants.COLOR_RED,
                 color_box_default=constants.COLOR_GREEN,
                 color_text_mouseover=constants.COLOR_WHITE,
                 color_text_default=constants.COLOR_GREY):

        self.surface = surface
        self.button_text = button_text
        self.size = size
        self.center_coords = center_coords

        self.c_box_mo = color_box_mouseover
        self.c_box_default = color_box_default
        self.c_text_mo = color_text_mouseover
        self.c_text_default = color_text_default
        self.c_c_box = color_box_default
        self.c_c_text = color_text_default

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center_coords

    def update(self, player_input):

        mouse_clicked = False

        local_events, local_mousepos = player_input
        mouse_x, mouse_y = local_mousepos

        mouse_over = (self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom)

        for event in local_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True

        if mouse_over and mouse_clicked:
            return True

        if mouse_over:
            self.c_c_box = self.c_box_mo
            self.c_c_text = self.c_text_mo
        else:
            self.c_c_box = self.c_box_default
            self.c_c_text = self.c_text_default

    def draw(self):

        pygame.draw.rect(self.surface, self.c_c_box, self.rect)
        draw_text(self.surface, self.button_text, self.center_coords, self.c_c_text, center=True)




class Slider:

    def __init__(self, surface, size, center_coords, bg_color, fg_color, parameter_value):
        self.surface = surface
        self.size = size
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.current_val = parameter_value

        self.bg_rect = pygame.Rect((0, 0), size)
        self.bg_rect.center = center_coords

        self.fg_rect = pygame.Rect((0, 0), (self.bg_rect.width * self.current_val, self.bg_rect.height))
        self.fg_rect.topleft = self.bg_rect.topleft

        self.grip_tab = pygame.Rect((0, 0), (20, self.bg_rect.height + 5))
        self.grip_tab.center = (self.fg_rect.right, self.bg_rect.centery)

    def update(self, player_input):
        mouse_down = pygame.mouse.get_pressed()[0]

        local_events, local_mousepos = player_input
        mouse_x, mouse_y = local_mousepos

        mouse_over = (
                self.bg_rect.left <= mouse_x <= self.bg_rect.right and self.bg_rect.top <= mouse_y <= self.bg_rect.bottom)

        if mouse_down and mouse_over:
            self.current_val = (float(mouse_x) - float(self.bg_rect.left)) / self.bg_rect.width

            self.fg_rect.width = self.bg_rect.width * self.current_val
            self.grip_tab.center = (self.fg_rect.right, self.bg_rect.centery)

    def draw(self):
        pygame.draw.rect(self.surface, self.bg_color, self.bg_rect)
        pygame.draw.rect(self.surface, self.fg_color, self.fg_rect)
        pygame.draw.rect(self.surface, constants.COLOR_BLACK, self.grip_tab)

