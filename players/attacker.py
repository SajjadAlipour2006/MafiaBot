from .player import Player


class AttackerPlayer(Player):

    def attack(self, player):
        raise NotImplementedError()
