from .day import Day


class Defending(Day):
    time = 30

    def __init__(self, player):
        super().__init__()
        self.player = player

    def get_next_phase(self, _):
        from .judging import Judging
        return Judging(self.player)
