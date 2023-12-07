from .villager import Villager
from .attacker import Attacker


class Sniper(Villager, Attacker):
    emoji = "💂‍♂️"
    attacking_power = 1
