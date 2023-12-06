class Player:

    def __init__(self, id, name=None):
        self.id = id
        self.name = name
        self.is_alive = True
        self.protection = 0

    def get_shot(self):
        self.is_alive = False
        return True

    def get_executed(self):
        self.is_alive = False

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"[{self.name}](https://web.bale.ai/chat?uid={self.id})"
