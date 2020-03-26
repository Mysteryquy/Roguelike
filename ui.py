import pygame
from src import config, constants

from render import draw_text


class UiElement:
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect, id: str, callback=None):
        self.surface = surface
        self.rect = rect
        self.id = id
        self.callback = callback

    def update(self, player_input) -> bool:
        pass

    def draw(self):
        pass

    def react(self, event: pygame.event.EventType) -> bool:
        pass

    def react_multiple(self, player_input):
        pass


class UiContainer(UiElement):
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect, id, elements, color: pygame.Color,
                 img=None, transparent=False, callback=None):
        super().__init__(surface, rect, id, callback)
        self.elements = elements
        self.color = color
        self.img = img
        self.transparent = transparent

    def add(self, element):
        self.elements.append(element)

    def update(self, player_input):
        return any(element.update(player_input) for element in self.elements)

    def draw(self):
        if not self.transparent:
            if self.img:
                print(str(self.rect))
                self.surface.blit(self.img, self.rect.topleft)
            else:
                pygame.draw.rect(self.surface, self.color, self.rect)
        for element in self.elements:
            element.draw()

    def react(self, event: pygame.event.EventType) -> bool:
        return any(element.react(event) for element in self.elements)

    def react_multiple(self, events) -> bool:
        return any(element.react_multiple(events) for element in self.elements)


class Button(UiElement):

    def __init__(self, surface, button_text, size, id, center_coords, color_box_mouseover=constants.COLOR_RED,
                 color_box_default=constants.COLOR_GREEN, color_text_mouseover=constants.COLOR_WHITE,
                 color_text_default=constants.COLOR_GREY, callback=None):

        super().__init__(surface, pygame.Rect((0, 0), size), id, callback)
        self.button_text = button_text
        self.center_coords = center_coords

        self.c_box_mo = color_box_mouseover
        self.c_box_default = color_box_default
        self.c_text_mo = color_text_mouseover
        self.c_text_default = color_text_default
        self.c_c_box = color_box_default
        self.c_c_text = color_text_default

        self.rect.center = center_coords

    def update(self, player_input: pygame.event):

        mouse_clicked = False

        local_events, local_mousepos = player_input
        mouse_x, mouse_y = local_mousepos

        mouse_over = (self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom)

        for event in local_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True

        if mouse_over:
            self.c_c_box = self.c_box_mo
            self.c_c_text = self.c_text_mo
        else:
            self.c_c_box = self.c_box_default
            self.c_c_text = self.c_text_default

        if mouse_over and mouse_clicked:
            if self.callback:
                self.callback(self.id)
            return True

    def react_multiple(self, player_input):
        return self.update(player_input)

    def draw(self):
        pygame.draw.rect(self.surface, self.c_c_box, self.rect)
        draw_text(self.surface, self.button_text, self.center_coords, self.c_c_text, center=True)


class Slider(UiElement):

    def __init__(self, surface, size, id, center_coords, bg_color, fg_color, parameter_value, string, callback=None):
        super().__init__(surface, pygame.Rect((0, 0), size), id, callback)
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

        self.string = string
        self.passed = 0

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
            self.passed = (self.passed + 1) % 4
            if self.callback and self.passed:
                self.callback(self.id, self.current_val)

    def draw(self):
        pygame.draw.rect(self.surface, self.bg_color, self.bg_rect)
        pygame.draw.rect(self.surface, self.fg_color, self.fg_rect)
        pygame.draw.rect(self.surface, constants.COLOR_BLACK, self.grip_tab)
        draw_text(self.surface, self.string, (self.bg_rect.x, self.bg_rect.y - 30), constants.COLOR_BLACK,
                  center=True)


class Textfield(UiElement):

    def __init__(self, surface, rect, id, color_inactive, color_active, text_color, font=pygame.font.Font(None, 32),
                 auto_active=False, start_text=None, focus_key=None, callback=None):

        super().__init__(surface, rect, id, callback)
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.font = font
        self.text_color = text_color
        self._active = auto_active
        self.color = color_active if self.active else color_inactive
        self.start_text = start_text
        self.text = self.start_text if self.start_text else ""
        self.focus_key = focus_key
        self.previous_input = ""

    def update(self, player_input):
        return any(self.react(event) for event in player_input)

    def react(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            self.active = self.rect.collidepoint(x, y)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    if self.callback:
                        self.callback(self.id, self.text_ready)
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.active = False
                elif event.key == pygame.K_UP:
                    self.text = self.previous_input
                else:
                    if self.start_text and self.text == self.start_text:
                        self.text = ""
                    self.text += event.unicode
            elif self.focus_key and event.key == self.focus_key:
                self.active = True

        return False

    def update_activate(self, event):
        if self.focus_key and event.type == pygame.KEYDOWN and event.key == self.focus_key:
            self.active = True
            return True
        return False

    @property
    def text_ready(self):
        self.previous_input = self.text
        self.text = ""
        return self.previous_input

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self.color = self.color_active if self._active else self.color_inactive

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        draw_text(self.surface, self.text, (self.rect.x + 3, self.rect.y), self.text_color, font=self.font)


class FillBar(UiElement):

    def __init__(self, surface, rect, id, bg_color, fg_color, string, max_value, text_color, border_color = constants.COLOR_BLACK):
        super().__init__(surface, rect, id,)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self._max_value = max_value
        self._current_value = self.max_value
        self.text_color = text_color
        self.border_color = border_color

        self.fg_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height)

        #if self.border:
            #self.border  = pygame.transform.scale(self.border, (self.rect.width, self.rect.height))

        self.string = string

        self.print_text_format = "{0}: {1}/{2}"


        self.mini_rect_w = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 3)
        self.mini_rect_h = pygame.Rect(self.rect.left, self.rect.top, 3, self.rect.height)

        # The bar gets initialized as filled

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, new_val):
        self._max_value = new_val

    @property
    def current_value(self):
        return self._current_value


    @current_value.setter
    def current_value(self, new_val):
        self._current_value = min(new_val, self.max_value)
        #self.right = self.left  + self.width
        #self.fg_rect.width = int(round(self._current_value/self._max_value)) * self.rect.width

        self.fg_rect = pygame.Rect(self.rect.left, self.rect.top,
                                   int(round((self._current_value/self._max_value) * self.rect.width)), self.rect.height )




    def update(self, player_input):
        (self.current_value, self.max_value) = player_input




    def draw(self):
        pygame.draw.rect(self.surface, self.bg_color, self.rect)
        pygame.draw.rect(self.surface, self.fg_color, self.fg_rect)
        draw_text(self.surface, self.print_text_format.format(self.string, self.current_value, self.max_value)
                  , (self.rect.centerx, self.rect.centery), self.text_color,
                  center=True, font=config.ASSETS.FONT_FANTY)

        #if self.border:
        #    self.surface.blit(self.border, self.rect)
        self.mini_rect_w.top = self.rect.top
        pygame.draw.rect(self.surface, self.border_color, self.mini_rect_w)
        self.mini_rect_w.top = self.rect.bottom - self.mini_rect_w.height
        pygame.draw.rect(self.surface, self.border_color, self.mini_rect_w)
        self.mini_rect_h.left = self.rect.left
        pygame.draw.rect(self.surface, self.border_color, self.mini_rect_h)
        self.mini_rect_h.left = self.rect.right - self.mini_rect_h.width
        pygame.draw.rect(self.surface, self.border_color, self.mini_rect_h)

class TextPane(UiElement):
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect, id: str, text_color, text, bg_color=None):
        super().__init__(surface, rect, id)
        self.text_color = text_color
        self.bg_color = bg_color
        self.static_text = text
        self.value = 0

    def update(self, player_input):
        self.value = player_input

    def draw(self):
        if self.bg_color:
            pygame.draw.rect(self.surface, self.bg_color, self.rect)
        draw_text(self.surface, self.static_text + str(self.value), (self.rect.x, self.rect.y), self.text_color)






class GuiContainer(UiContainer):



    def __init__(self, surface: pygame.Surface, rect: pygame.Rect, id, health_bar, mana_bar, xp_bar, str_pane, dex_pane, int_pane):
        super().__init__(surface, rect, id, None, constants.COLOR_BLUE_LIGHT, transparent=True)
        self. items ={
            health_bar.id: health_bar,
            mana_bar.id: mana_bar,
            xp_bar.id: xp_bar,
            str_pane.id: str_pane,
            dex_pane.id: dex_pane,
            int_pane.id: int_pane
                    }


    def draw(self):
        for element in self.items.values():
            element.draw()

    def update(self, player_input):
        self.items["health_bar"].update(
            (config.PLAYER.creature.hp, config.PLAYER.creature.maxhp))
        self.items["mana_bar"].update(
            (config.PLAYER.creature.current_mana, config.PLAYER.creature.max_mana))
        if config.PLAYER.creature.level == constants.MAX_LEVEL:
            self.items["xp_bar"].print_string_format = "{0}"
            self.items["xp_bar"].string = "MAX LEVEL"
        else:
            self.items["xp_bar"].update(
                (config.PLAYER.creature.current_xp - (constants.XP_NEEDED[
                                                          config.PLAYER.creature.level - 1] if config.PLAYER.creature.level != 1 else 0),
                 constants.XP_NEEDED_FOR_NEXT[config.PLAYER.creature.level]))

        self.items["str"].update(config.PLAYER.creature.strength)
        self.items["dex"].update(config.PLAYER.creature.dexterity)
        self.items["int"].update(config.PLAYER.creature.intelligence)

