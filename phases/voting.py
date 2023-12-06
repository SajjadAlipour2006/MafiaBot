from .day import Day


class Voting(Day):

    def __init__(self):
        super().__init__()
        self.time = 40
        self.voters = []
        self.voteds = []
        self.voted_player = None

    def vote(self, players, voter, voted):
        if voter in self.voters:
            self.unvote(voter)
        self.voters.append(voter)
        self.voteds.append(voted)
        if self.voteds.count(voted) > (len(players)/2):
            self.voted_player = voted
            self.stop()

    def unvote(self, unvoter):
        index = self.voters.index(unvoter)
        self.voters.pop(index)
        self.voteds.pop(index)

    def get_next_phase(self, _):
        if self.voted_player is not None:
            from .defending import Defending
            return Defending(self.voted_player)
        from .night import Night
        return Night()
