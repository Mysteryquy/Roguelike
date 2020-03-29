from dataclasses import dataclass

TILE_DICT = {
    # TODO decide if this should actually be here
}


@dataclass
class Tile:
    block_path: bool
    texture: int
    texture_explored: int
    draw_on_minimap: bool = False
    draw_on_screen: bool = False
    was_drawn: bool = False

    def __init__(self, block_path: bool, texture_code: int, texture_explored_code: int = None):
        self.block_path = block_path
        self.texture = texture_code
        self.texture_explored = texture_explored_code if texture_explored_code else texture_code
        self.explored = False
        self.draw_on_minimap = False
        self.draw_on_screen = False
        self.was_drawn = False


