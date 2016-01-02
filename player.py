
class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_abs = 0.1
        self.speed = {'x': 0, 'y': 0}

    def snapshot(self):
        return {
            'x': self.x,
            'y': self.y
        }

    def apply_input(self, keys):
        self.speed = {'x': 0, 'y': 0}
        if keys['w']:
            self.speed['y'] += 1
        if keys['s']:
            self.speed['y'] -= 1
        if keys['d']:
            self.speed['x'] += 1
        if keys['a']:
            self.speed['x'] -= 1

    def model(self, step):
        self.x += self.speed['x'] * self.speed_abs
        self.y += self.speed['y'] * self.speed_abs

    @staticmethod
    def from_snapshot(snapshot):
        return Player(snapshot['x'], snapshot['y'])
