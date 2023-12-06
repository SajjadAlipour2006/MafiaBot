from .villager import VillagerPlayer
from .attacker import AttackerPlayer


class SniperPlayer(VillagerPlayer, AttackerPlayer):

    def attack(self, player):
        if player.protection >= 1:
            player.protection -= 1
            return False
        return player.get_shot()
