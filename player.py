
class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def snapshot(self):
        return {
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def from_snapshot(snapshot):
        return Player(snapshot['x'], snapshot['y'])
