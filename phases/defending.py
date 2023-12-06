from .day import Day


class Defending(Day):

    def __init__(self, player):
        super().__init__()
        self.time = 30
        self.player = player

    def get_next_phase(self, _):
        from .judging import Judging
        return Judging(self.player)
