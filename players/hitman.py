from .mafia import Mafia
from .attacker import Attacker


class Hitman(Mafia, Attacker):
    attacking_power = 1
