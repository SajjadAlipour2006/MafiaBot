from .day import Day


class Conversing(Day):
    time = 7

    def get_next_phase(self, players):
        if len(players) <= 2:
            from .night import Night
            return Night()
        from .voting import Voting
        return Voting()
