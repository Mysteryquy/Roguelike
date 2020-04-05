from dataclasses import dataclass


@dataclass
class Tile:
    block_path: bool
    texture: int
    draw_on_minimap: bool = False
    draw_on_screen: bool = False
    was_drawn: bool = False

    def __init__(self, block_path: bool, texture_code: int):
        self.block_path = block_path
        self.texture = texture_code
        self.explored = False
        self.draw_on_minimap = False
        self.draw_on_screen = False
        self.was_drawn = False
