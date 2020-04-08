from dataclasses import dataclass

# xp related stuff
import math

XP_NEEDED = {
    1: 300,
    2: 400,
    3: 500,
    4: 600,
    5: 700,
    6: math.inf,
}

MAX_LEVEL = max(XP_NEEDED.keys())

TOTAL_EXP = {level: sum((XP_NEEDED[lvl] for lvl in range(1, level))) for level in XP_NEEDED.keys()}
print(TOTAL_EXP)


@dataclass
class Experience:
    current_experience: int = 0
    on_death: int = 0
