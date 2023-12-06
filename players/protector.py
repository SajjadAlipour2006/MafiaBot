from .player import Player


class ProtectorPlayer(Player):
    protecting_power = 0

    def protect(self, player):
        player.protection += self.protecting_power
        return True
