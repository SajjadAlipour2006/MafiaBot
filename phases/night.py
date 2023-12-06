from .phase import Phase


class Night(Phase):
    time = 50

    def get_next_phase(self, _):
        from .conversing import Conversing
        return Conversing()
