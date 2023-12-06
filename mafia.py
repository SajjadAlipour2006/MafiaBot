from random import choice

from players import Player, VillagerPlayer, MafiaPlayer
from phases import Night

roles = [VillagerPlayer, MafiaPlayer]


class Mafia:

    def __init__(self):
        self.players = []
        self.phase = Night()

    def add_player(self, id, name):
        player = Player(id, name)
        if player in self.players:
            return False
        self.players.append(player)
        return True

    def remove_player(self, id):
        player = Player(id)
        if player in self.players:
            self.players.remove(player)
            return True
        return False

    def assign_roles(self):
        for i, player in enumerate(self.players):
            role = choice(roles)
            self.players[i] = role(player.id, player.name)

    def run(self, client, callback):
        while True:
            callback(client, self.phase)
            self.phase.start()
            self.phase = self.phase.get_next_phase(self.players)
