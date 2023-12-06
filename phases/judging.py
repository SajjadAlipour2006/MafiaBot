from .day import Day


class Judging(Day):
    time = 30

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.voters = []
        self.votes = []

    def vote(self, voter, vote):
        if voter in self.voters:
            self.unvote(voter)
        self.voters.append(voter)
        self.votes.append(vote)

    def unvote(self, unvoter):
        index = self.voters.index(unvoter)
        self.voters.pop(index)
        self.votes.pop(index)

    def get_next_phase(self, _):
        approves = self.votes.count(True)
        disapproves = self.votes.count(False)
        if approves >= disapproves:
            from .last_words import LastWords
            return LastWords(self.player)
        from .night import Night
        return Night()
