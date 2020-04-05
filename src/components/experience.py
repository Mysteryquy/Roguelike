from dataclasses import dataclass

# xp related stuff
import math

XP_NEEDED = {
    1: 300,
    2: 700,
    3: 1200,
    4: 1800,
    5: 2500,
}

MAX_LEVEL = max(XP_NEEDED.keys())

XP_NEEDED_FOR_NEXT = {}
for i in XP_NEEDED.keys():
    if i < MAX_LEVEL:
        XP_NEEDED_FOR_NEXT[i] = XP_NEEDED[i + 1] - XP_NEEDED[i]
    else:
        XP_NEEDED_FOR_NEXT[i] = math.inf


@dataclass
class Experience:
    current_experience: int = 0
    on_death: int = 0
