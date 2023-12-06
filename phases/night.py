from .phase import Phase


class Night(Phase):
    time = 5

    def get_next_phase(self, _):
        from .conversing import Conversing
        return Conversing()
