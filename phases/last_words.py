from .day import Day


class LastWords(Day):

    def __init__(self, player):
        super().__init__()
        self.time = 15
        self.player = player

    def get_next_phase(self, _):
        from .night import Night
        return Night()
