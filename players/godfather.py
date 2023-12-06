from .mafia import MafiaPlayer
from .attacker import AttackerPlayer


class Godfather(MafiaPlayer, AttackerPlayer):
    attacking_power = 1
