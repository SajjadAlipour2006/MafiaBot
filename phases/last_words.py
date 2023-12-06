from .day import Day


class LastWords(Day):
    time = 15

    def __init__(self, player):
        super().__init__()
        self.player = player

    def get_next_phase(self, _):
        from .night import Night
        return Night()
