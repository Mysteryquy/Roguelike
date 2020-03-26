from dataclasses import dataclass


TILE_DICT = {

}

@dataclass
class Tile:
    block_path: bool
    texture: int
    texture_explored: int
    draw_on_minimap: bool = False
    draw_on_screen: bool = False
    was_drawn: bool = False

    def __init__(self, block_path, texture_code, texure_explored_code):
        self.block_path = block_path
        self.explored = False
        self._texture = texture_code
        self._texture_explored = self._texture + "_EXPLORED"
        self.draw_on_minimap = False
        self.draw_on_screen = False
        self.was_drawn = False

    @property
    def texture(self):
        return self._texture

    @property
    def texture_explored(self):
        return self._texture_explored

    @texture.setter
    def texture(self, value):
        self._texture = value
        self._texture_explored = value + "_EXPLORED"

