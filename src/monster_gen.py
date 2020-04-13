import numpy

from src import constants
from src.components.ai import AiChase
from src.components.alignment import Alignment, CreatureAlignment
from src.components.attacker import Attacker
from src.components.block import BlocksMovement
from src.components.death import Death
from src.components.energy import Energy
from src.components.experience import Experience
from src.components.health import Health
from src.components.name import Name
from src.components.position import Position
from src.components.render import Renderable
from src.resources.levels import Levels


def gen_demon_avin(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y), Attacker(attack=8,
                                                                   defense=2, hit_chance=50, evasion_chance=3),
                              Name("Avin"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_AVIN"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_DEAD_DEMON")
                              )


def gen_aquatic_piranha(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y), Attacker(attack=5,
                                                                   defense=1, hit_chance=90, evasion_chance=30),
                              Name("Piranha"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_PIRANHA"),
                              Energy(120),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_jellyfish(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y), Attacker(attack=5,
                                                                   defense=1, hit_chance=90, evasion_chance=30),
                              Name("Jellyfish"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_JELLYFISH"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_jellyowar(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=5, defense=1, hit_chance=90, evasion_chance=30),
                              Name("Jelly-o-war"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_JELLYOWAR"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_shark(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=5, defense=1, hit_chance=90, evasion_chance=30),
                              Name("Shark"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_SHARK"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_shark_white(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=5, defense=1, hit_chance=90, evasion_chance=30),
                              Name("Great White Shark"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_SHARK_WHITE"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_shark_gold(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=5, defense=1, hit_chance=90, evasion_chance=30),
                              Name("Great White Shark"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_SHARK_GOLD"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_whale(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=5, defense=1, hit_chance=90, evasion_chance=30),
                              Name("Whale"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_WHALE"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_watersnake(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=5, defense=1, hit_chance=90, evasion_chance=30),
                              Name("Watersnake"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_WATERSNAKE"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_eel(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=5, defense=1, hit_chance=90, evasion_chance=30),
                              Name("Eel"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_EEL"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_kelpie(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=6, defense=3, hit_chance=80, evasion_chance=20),
                              Name("Kelpie"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_KEPLIE"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_sea_devil(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=6, defense=3, hit_chance=80, evasion_chance=20),
                              Name("Sea Devil"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_SEA_DEVIL"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_aquatic_frog_hypno(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(20), Position(x, y),
                              Attacker(attack=6, defense=3, hit_chance=80, evasion_chance=20),
                              Name("Hypno Frog"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_AQUATIC_FROG_HYPNO"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=100),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_boss_aquatic_kraken(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("The KRAKEN"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_BOSS_AQUATIC_KRAKEN"),
                              Energy(60),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=10000),
                              Death(animation_key="S_FLESH_FISH")
                              )


def gen_demon_gronk(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Gronk"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_GRONK"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )

def gen_demon_sloosh(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Sloosh"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_SLOOSH"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )

def gen_demon_kolak(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Kolak"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_KOLAK"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )

def gen_demon_absodusx(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Absodux"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_ABSODUX"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )

def gen_demon_nergal(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Nergal"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_NERGAL"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )

def gen_demon_boomi(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Boomi"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_BOOMI"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )


def gen_demon_flabsy(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Flabsi"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_FLABSY"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )


def gen_demon_hulk(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Hulk"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_HULK"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )


def gen_demon_pillus(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Pillus"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_PILLUS"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )

def gen_demon_buffla(level, coords):
    pos = level.world.component_for_player(Position)
    x, y = coords

    level.world.create_entity(Health(100), Position(x, y),
                              Attacker(attack=12, defense=4, hit_chance=75, evasion_chance=1),
                              Name("Buffla"), AiChase(pos),
                              Renderable(depth=constants.DEPTH_CREATURE, animation_key="A_DEMON_BUFFLA"),
                              Energy(100),
                              BlocksMovement(),
                              Alignment(CreatureAlignment.FOE),
                              Experience(on_death=1000),
                              Death(animation_key="S_DEAD_DEMON")
                              )

level_monster_dict = {
    Levels.DUNGEON1: [(gen_demon_avin, 100), (gen_aquatic_piranha, 100)],
    Levels.WATER1: [(gen_aquatic_eel, 100), (gen_aquatic_frog_hypno, 100), (gen_aquatic_jellyfish, 100),
                 (gen_aquatic_jellyowar, 100), (gen_aquatic_kelpie, 100), (gen_aquatic_piranha, 100),
                 (gen_aquatic_sea_devil, 100), (gen_aquatic_shark, 100), (gen_aquatic_shark_gold, 100),
                 (gen_aquatic_shark_white, 100), (gen_aquatic_watersnake, 100), (gen_aquatic_whale, 100),
                 (gen_boss_aquatic_kraken, 50)],
    Levels.HELL1: [(gen_demon_avin, 100), (gen_demon_gronk, 100), (gen_demon_sloosh, 100), (gen_demon_kolak, 100),
                      (gen_demon_absodusx, 100), (gen_demon_nergal, 100), (gen_demon_boomi, 100), (gen_demon_flabsy, 100),
                      (gen_demon_hulk, 100), (gen_demon_pillus, 100), (gen_demon_buffla, 100)]
}


def gen_and_append_enemy(level, coords):
    monsters_and_weight = level_monster_dict[level.name]
    monsters = [monster for monster, _ in monsters_and_weight]
    sum_weights = sum([weight for _, weight in monsters_and_weight])
    probabilities = [weight / sum_weights for _, weight in monsters_and_weight]
    monster_function = numpy.random.choice(monsters, 1, p=probabilities)[0]
    monster_function(level, coords)
