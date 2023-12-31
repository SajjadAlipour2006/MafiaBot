from random import choice

from players import Player, Detective, Doctor, Godfather, Hitman, Joker, Mayor, Sniper
from phases import Night


class Mafia:
    roles = {Detective: 2, Doctor: 2, Godfather: 1, Hitman: 2, Joker: 1, Mayor: 2, Sniper: 2}

    def __init__(self):
        self.players = []
        self.phase = Night()

    def __str__(self):
        emojis = dict(enumerate(["💀", "❤️"]))
        return "\n".join(f"{i}. {player} {emojis[player.is_alive]}" for i, player in enumerate(self.players, start=1))

    @property
    def alive_players(self):
        return [player for player in self.players if player.is_alive]

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
            while True:
                role = choice(list(self.roles))
                role_count = sum(1 for p in self.players if isinstance(p, role))
                if role_count <= self.roles[role]:
                    break
            self.players[i] = role(player.id, player.name)

    def run(self, client, callback):
        while True:
            callback(client, self.phase)
            self.phase.start()
            self.phase = self.phase.get_next_phase(self.alive_players)
