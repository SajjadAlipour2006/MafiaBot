from .independent import IndependentPlayer


class JokerPlayer(IndependentPlayer):

    def get_shot(self):
        return False

    def get_executed(self):
        pass
