from threading import Event


class Phase:
    time = 0

    def __init__(self):
        self.event = Event()

    def start(self):
        self.event.wait(self.time)

    def stop(self):
        self.event.set()

    def get_next_phase(self, _):
        return Phase()
