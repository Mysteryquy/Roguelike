import random

from src import esper
from src.components.action import MeleeAttackAction
from src.components.attacker import Attacker
from src.components.health import Health, TakeDamageEvent
from src.components.name import Name


class AttackProcessor(esper.Processor):
    def process(self):
        # process melee attacks
        for ent, (attacker, attack, health, name) in \
                self.level.world.get_components(Attacker, MeleeAttackAction, Health, Name):
            attacked = None
            if self.level.world.has_component(attack.target, Attacker):
                attacked = self.level.world.component_for_entity(attack.target, Attacker)
            evasion = attacked.evasion_chance if attacked else 0
            to_hit = attacker.hit_chance - evasion
            if to_hit + random.randint(1,100) >= 100:
                # hit
                # TODO make attack damage event here maybe?
                defense = attacked.defense if attacked else 0
                damage = max(0, attacker.attack - defense)
                self.level.world.add_component(attack.target, TakeDamageEvent(damage, source=ent))

            self.level.world.remove_component(ent, MeleeAttackAction)




