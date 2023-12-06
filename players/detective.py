from .villager import VillagerPlayer
from .investigator import InvestigatorPlayer
from .godfather import Godfather


class DetectivePlayer(VillagerPlayer, InvestigatorPlayer):

    def investigate(self, player):
        if isinstance(player, Godfather):
            return None
        return type(player)
