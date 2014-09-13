
class Server(object):
    def __init__(self):
        self.clients = set()
        self.message_queue = []

    def queue_message(self, message):
        self.message_queue.append(message)


