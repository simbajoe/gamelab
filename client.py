
class Client(object):
    def __init__(self):
        self.id = None
        self.connect = None
        self.send = None
        self.receive = None
        self.get_time = None

        self.keys = {'w': False, 'a': False, 's': False, 'd': False}

    def keypress(self, char):
        if char in self.keys:
            self.keys[char] = True

    def keyup(self, char):
        if char in self.keys:
            self.keys[char] = False

    def mainloop(self):
        pass

    def snapshot(self):
        return None

    def __repr__(self):
        return 'Client %d' % self.id

