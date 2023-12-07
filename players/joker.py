from .independent import Independent


class Joker(Independent):
    emoji = "👨‍🎤"

    def get_shot(self):
        return False

    def get_executed(self):
        super().get_executed()
