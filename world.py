
class World(object):

    def __init__(self, time):
        self.time = time

    def apply_messages(self, messages):
        pass

    def snapshot(self):
        return None

    @staticmethod
    def from_snapshot(snapshot):
        return World(snapshot.time)
