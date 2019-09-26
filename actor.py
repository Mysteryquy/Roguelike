import math
import game_map
import config
import constants


class Actor:

    def __init__(self, x, y, name_object, animation_key, animation_speed=1.0, depth = 0, creature=None, ai=None, container=None,
                 item=None, equipment=None, stairs=None, state=None, exitportal=None, draw_explored=False, gold=0):
        self.x = round(x)
        self.y = round(y)
        self.name_object = name_object
        self.animation_key = animation_key
        self.animation = config.ASSETS.animation_dict[self.animation_key]  # number of images
        self.animation_speed = animation_speed / 1.0  # in seconds
        self.depth = depth

        self.draw_explored = draw_explored

        # animation flicker speed
        self.flicker_speed = self.animation_speed / len(self.animation)
        self.flicker_timer = 0.0
        self.sprite_image = 0  # s

        self.creature = creature
        if self.creature:
            self.creature.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:
            self.container.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

        self.stairs = stairs
        if self.stairs:
            self.stairs.owner = self

        self.state = state
        if self.state:
            self.state.owner = self

        self.exitportal = exitportal
        if self.exitportal:
            self.exitportal.owner = self

        self.gold = gold
        if self.gold:
            self.gold.owner = self



    @property
    def display_name(self):

        if self.creature:
            return self.creature.name_instance + " the " + self.name_object

        if self.item:
            if self.equipment and self.equipment.equipped:
                return self.name_object + "(equipped)"
            else:
                return self.name_object

    def draw(self):
        is_visible = config.FOV_MAP.fov[self.y, self.x]

        explored_draw = self.draw_explored and game_map.is_explored(self.x,self.y) and not is_visible
        special_flags = constants.EXPLORED_DRAW_FLAGS if explored_draw else 0

        if is_visible or explored_draw:
            if len(self.animation) == 1:
                config.SURFACE_MAP.blit(self.animation[0],
                                        (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT),
                                        special_flags=special_flags)

            elif len(self.animation) > 1:
                if config.CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1 / config.CLOCK.get_fps()

                if self.flicker_timer >= self.flicker_speed:
                    self.flicker_timer = 0.0

                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0

                    else:
                        self.sprite_image += 1

                config.SURFACE_MAP.blit(self.animation[self.sprite_image],
                                 (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT),
                                        special_flags=special_flags)


    def distance_to(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def move_towards(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx/distance))
        dy = int(round(dy/distance))



        self.creature.move(dx, dy)

    def move(self,dx,dy):
        self.creature.move(dx,dy)


    def move_away(self, other):

        dx = self.x - other.x
        dy = self.y - other.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)

    def animation_destroy(self):

        self.animation = None

    def animation_init(self):

        self.animation = config.ASSETS.animation_dict[self.animation_key]  # number of images

    def destroy(self):
        self.creature = None
        self.ai = None

    def set_animation(self,new_key):
        self.animation_key=new_key
        self.animation=config.ASSETS.animation_dict[self.animation_key]
