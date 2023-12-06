from .mafia import MafiaPlayer
from .attacker import AttackerPlayer


class HitmanPlayer(MafiaPlayer, AttackerPlayer):

    def attack(self, player):
        if player.protection >= 1:
            player.protection -= 1
            return False
        return player.get_shot()
