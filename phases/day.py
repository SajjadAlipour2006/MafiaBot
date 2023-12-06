from .phase import Phase


class Day(Phase):
    time = 100

    def __init__(self):
        super().__init__()

    def get_next_phase(self, _):
        return Day()
