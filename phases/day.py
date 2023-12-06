from .phase import Phase


class Day(Phase):

    def __init__(self):
        super().__init__()
        self.time = 100

    def get_next_phase(self, _):
        return Day()
