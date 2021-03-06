# coding=utf-8
from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from pygame.surface import Surface
from pygame.time import Clock
from tcod.map import Map

from src.menu import MainMenu
from src.ui import GuiContainer

if TYPE_CHECKING:
    from src.assets import Assets
    from src.camera import Camera
    from src.main_game import Preferences
    from src.object_game import Game

ASSETS: Optional["Assets"] = None
PREFERENCES: Optional["Preferences"] = None
GAME: Optional["Game"] = None
FOV_CALCULATE: bool = True
CAMERA: Optional["Camera"] = None
MINI_MAP_CAMERA: Optional["Camera"] = None
CLOCK: Optional["Clock"] = None
FOV_MAP: Optional["Map"] = None
SURFACE_MAP: Optional["Surface"] = None
SURFACE_MESSAGES: Optional["Surface"] = None
SURFACE_MAIN: Optional["Surface"] = None
SURFACE_MINI_MAP: Optional["Surface"] = None
CONSOLE = None
SURFACE_INFO: Optional["Surface"] = None
MAIN_MENU: Optional["MainMenu"] = None
GUI: Optional["GuiContainer"] = None
ROUND_COUNTER: int = 0
