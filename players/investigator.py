from .player import Player


class Investigator(Player):

    def investigate(self, player):
        raise NotImplementedError()
