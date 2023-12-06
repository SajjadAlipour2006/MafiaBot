from .phase import Phase


class Night(Phase):
    time = 5

    def __init__(self):
        super().__init__()

    def get_next_phase(self, _):
        from .conversing import Conversing
        return Conversing()
