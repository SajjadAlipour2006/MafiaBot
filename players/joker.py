from .independent import Independent


class Joker(Independent):

    def get_shot(self):
        return False

    def get_executed(self):
        super().get_executed()
