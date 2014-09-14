
class Server(object):
    def __init__(self):
        self.clients = set()
        self.send = None
        self.receive = None
        self.get_time = None

    def mainloop(self):
        pass

    def snapshot(self):
        return None

