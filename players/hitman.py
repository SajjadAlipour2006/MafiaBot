from .mafia import MafiaPlayer
from .attacker import AttackerPlayer


class HitmanPlayer(MafiaPlayer, AttackerPlayer):
    attacking_power = 1
