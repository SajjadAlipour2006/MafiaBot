from .villager import VillagerPlayer
from .investigator import InvestigatorPlayer
from .godfather import GodfatherPlayer


class DetectivePlayer(VillagerPlayer, InvestigatorPlayer):

    def investigate(self, player):
        if isinstance(player, GodfatherPlayer):
            return None
        return type(player)
