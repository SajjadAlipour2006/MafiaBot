from .day import Day


class Execution(Day):
    time = 5

    def __init__(self, player):
        super().__init__()
        self.player = player

    def get_next_phase(self, _):
        from .night import Night
        return Night()
