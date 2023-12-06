from .villager import VillagerPlayer
from .attacker import AttackerPlayer


class SniperPlayer(VillagerPlayer, AttackerPlayer):
    attacking_power = 1
