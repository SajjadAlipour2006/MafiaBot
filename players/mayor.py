from .villager import Villager


class Mayor(Villager):
    emoji = "👩‍💼"

    def __init__(self, id, name=None):
        super().__init__(id, name)
        self.extra_lives = 1

    def get_shot(self):
        if self.extra_lives > 0:
            self.extra_lives -= 1
            return False
        return super().get_shot()
