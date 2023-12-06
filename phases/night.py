from .phase import Phase


class Night(Phase):

    def __init__(self):
        super().__init__()
        self.time = 5

    def get_next_phase(self, _):
        from .conversing import Conversing
        return Conversing()
