from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Usable:
    use_function: Callable[[int], Any]
