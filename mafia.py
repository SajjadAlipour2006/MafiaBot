from random import choice

from players import (
    Player,
    DetectivePlayer,
    DoctorPlayer,
    GodfatherPlayer,
    HitmanPlayer,
    JokerPlayer,
    MayorPlayer,
    SniperPlayer
)
from phases import Night


class Mafia:
    roles = [
        DetectivePlayer,
        DoctorPlayer,
        GodfatherPlayer,
        HitmanPlayer,
        JokerPlayer,
        MayorPlayer,
        SniperPlayer
    ]

    def __init__(self):
        self.players = []
        self.phase = Night()

    def __str__(self):
        return "\n".join(str(player) for player in self.players)

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
            role = choice(self.roles)
            self.roles.remove(role)
            self.players[i] = role(player.id, player.name)

    def run(self, client, callback):
        while True:
            callback(client, self.phase)
            self.phase.start()
            self.phase = self.phase.get_next_phase(self.players)
