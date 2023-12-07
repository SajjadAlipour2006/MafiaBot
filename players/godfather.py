from .mafia import Mafia
from .attacker import Attacker


class Godfather(Mafia, Attacker):
    emoji = "🤵‍♂️"
    attacking_power = 1
