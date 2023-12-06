from .player import Player


class InvestigatorPlayer(Player):

    def investigate(self, player):
        raise NotImplementedError()
