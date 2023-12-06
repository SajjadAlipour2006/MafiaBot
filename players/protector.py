from .player import Player


class ProtectorPlayer(Player):

    def protect(self, player):
        raise NotImplementedError()
