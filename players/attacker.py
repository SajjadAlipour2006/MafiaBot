from .player import Player


class Attacker(Player):
    attacking_power = 0

    def attack(self, player):
        if player.protection >= self.attacking_power:
            player.protection -= self.attacking_power
            return False
        return player.get_shot()
