from world import World

class Client(object):
    def __init__(self, model_step):
        self.id = None

        self.keys = {'w': False, 'a': False, 's': False, 'd': False}
        self.model_step = model_step
        self.world = None

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
        new_messages = self.receive()
        if len(new_messages):
            last_message = new_messages[-1]
            self.world = World.from_snapshot(last_message['data'])
        if self.world:
            self.send({
                'keys': self.keys,
                'client_time': self.world.time
            })

    def snapshot(self):
        if self.world:
            return self.world.snapshot()
        return None

    def __repr__(self):
        return 'Client %d' % self.id

