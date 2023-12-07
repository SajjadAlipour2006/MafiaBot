from .villager import Villager
from .investigator import Investigator
from .godfather import Godfather


class Detective(Villager, Investigator):

    def investigate(self, player):
        if isinstance(player, Godfather):
            return None
        return type(player)
