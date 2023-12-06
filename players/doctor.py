from .villager import VillagerPlayer
from .protector import ProtectorPlayer


class DoctorPlayer(VillagerPlayer, ProtectorPlayer):

    def protect(self, player):
        player.protection += 1
        return True
