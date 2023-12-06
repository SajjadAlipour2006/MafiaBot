from .phase import Phase


class Day(Phase):
    time = 100

    def get_next_phase(self, _):
        return Day()
