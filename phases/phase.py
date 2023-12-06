from threading import Event


class Phase:

    def __init__(self):
        self.time = 0
        self.event = Event()

    def start(self):
        self.event.wait(self.time)

    def stop(self):
        self.event.set()

    def get_next_phase(self, _):
        return Phase()
