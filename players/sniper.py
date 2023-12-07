from .villager import Villager
from .attacker import Attacker


class Sniper(Villager, Attacker):
    attacking_power = 1
