from .mafia import MafiaPlayer
from .attacker import AttackerPlayer


class GodfatherPlayer(MafiaPlayer, AttackerPlayer):
    attacking_power = 1
