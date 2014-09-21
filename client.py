
class Client(object):
    def __init__(self, model_step):
        self.id = None

        self.keys = {'w': False, 'a': False, 's': False, 'd': False}
        self.model_step = model_step

    def connect(self):
        raise NotImplementedError()

    def send(self, message):
        raise NotImplementedError()

    def receive(self):
        raise NotImplementedError()

    def get_time(self):
        raise NotImplementedError()

    def key_down(self, char):
        if char in self.keys:
            self.keys[char] = True

    def key_up(self, char):
        if char in self.keys:
            self.keys[char] = False

    def mainloop(self):
        pass

    def snapshot(self):
        return None

    def __repr__(self):
        return 'Client %d' % self.id

