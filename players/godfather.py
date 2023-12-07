from .mafia import Mafia
from .attacker import Attacker


class Godfather(Mafia, Attacker):
    attacking_power = 1
